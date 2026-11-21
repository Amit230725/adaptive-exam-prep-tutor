"""core/db.py - SQLite Thread-Safe Normalized Data Store & State Engine

Blueprint References:
- Section 16: "Database specification" (Normalized schema, attempts, mastery events, adjudications, interventions)
- Section 17: "API contracts and scoring security" (Server-authoritative scoring, idempotency keys)
- Section 18: "Privacy, safety and AI governance" (Consent tracking, audit logs, data export/deletion)
- Section 21: "Backlog, tests and launch checklist" (Attempt replay deterministic verification)
"""

import os
import json
import sqlite3
import threading
import time
from typing import List, Dict, Any, Optional, Tuple

from core.concepts import CONCEPTS_51
from core.learner import update_bkt, get_mastery_state, DEFAULT_PRIOR

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "cp.db")
_LOCK = threading.Lock()

def get_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with check_same_thread=False."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initializes normalized tables and indexes if they do not exist, and runs safe migrations."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            
            # Helper to safely add column if missing
            def ensure_column(table: str, column: str, col_type: str):
                cur.execute(f"PRAGMA table_info({table})")
                cols = [c[1] for c in cur.fetchall()]
                if column not in cols:
                    try:
                        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
                    except Exception:
                        pass

            # Safe column additions if old tables exist
            ensure_column("students", "consent_given", "INTEGER DEFAULT 1")
            ensure_column("students", "accessibility_prefs", "TEXT DEFAULT '{}'")
            ensure_column("responses", "confidence", "TEXT DEFAULT 'medium'")
            ensure_column("responses", "client_elapsed_ms", "INTEGER DEFAULT 0")
            ensure_column("responses", "is_assisted", "INTEGER DEFAULT 0")
            ensure_column("responses", "idempotency_key", "TEXT")
            ensure_column("misconception_events", "evidence_span", "TEXT")
            ensure_column("misconception_events", "alternatives_json", "TEXT DEFAULT '[]'")
            ensure_column("misconception_events", "needs_probe", "INTEGER DEFAULT 0")
            ensure_column("misconception_events", "status", "TEXT DEFAULT 'suspected'")
            ensure_column("mastery", "evidence_count", "INTEGER DEFAULT 1")
            ensure_column("mastery", "state_label", "TEXT DEFAULT 'developing'")
            ensure_column("mastery", "updated_at", "REAL DEFAULT 0.0")

            cur.executescript("""
            -- Students & Users
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                nickname TEXT NOT NULL,
                class_code TEXT DEFAULT 'CBSE10-PHYS',
                consent_given INTEGER DEFAULT 1,
                accessibility_prefs TEXT DEFAULT '{}',
                created_at REAL NOT NULL
            );

            -- Immutable Attempts / Responses (Idempotency protected)
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                concept TEXT NOT NULL,
                chosen INTEGER NOT NULL,
                correct INTEGER NOT NULL,
                reasoning TEXT,
                confidence TEXT DEFAULT 'medium',
                client_elapsed_ms INTEGER DEFAULT 0,
                is_assisted INTEGER DEFAULT 0,
                attempt INTEGER NOT NULL,
                idempotency_key TEXT UNIQUE,
                ts REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            );

            -- Diagnostic Sessions (Autosave & Resume)
            CREATE TABLE IF NOT EXISTS diagnostic_sessions (
                student_id TEXT PRIMARY KEY,
                scope TEXT DEFAULT 'blueprint_30',
                current_index INTEGER DEFAULT 0,
                answers_json TEXT DEFAULT '{}',
                reasonings_json TEXT DEFAULT '{}',
                confidences_json TEXT DEFAULT '{}',
                is_completed INTEGER DEFAULT 0,
                updated_at REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            );

            -- Misconception Inferences
            CREATE TABLE IF NOT EXISTS misconception_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                response_id INTEGER,
                concept TEXT NOT NULL,
                misconception_id TEXT NOT NULL,
                confidence REAL NOT NULL,
                evidence_span TEXT,
                alternatives_json TEXT DEFAULT '[]',
                needs_probe INTEGER DEFAULT 0,
                status TEXT DEFAULT 'suspected',
                source TEXT DEFAULT 'ai',
                ts REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (response_id) REFERENCES responses(id)
            );

            -- Teacher Adjudications (Stored separately from AI predictions)
            CREATE TABLE IF NOT EXISTS teacher_adjudications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                teacher_id TEXT NOT NULL,
                adjudication_status TEXT NOT NULL,
                original_misconception_id TEXT NOT NULL,
                updated_misconception_id TEXT,
                teacher_notes TEXT,
                ts REAL NOT NULL,
                FOREIGN KEY (event_id) REFERENCES misconception_events(id),
                FOREIGN KEY (student_id) REFERENCES students(id)
            );

            -- Current Materialized Mastery
            CREATE TABLE IF NOT EXISTS mastery (
                student_id TEXT NOT NULL,
                concept TEXT NOT NULL,
                mastery REAL NOT NULL,
                stability REAL NOT NULL,
                due_day REAL NOT NULL,
                evidence_count INTEGER DEFAULT 1,
                state_label TEXT DEFAULT 'developing',
                updated_at REAL NOT NULL,
                PRIMARY KEY (student_id, concept),
                FOREIGN KEY (student_id) REFERENCES students(id)
            );

            -- Mastery Update Event Log (Audit trail for replay)
            CREATE TABLE IF NOT EXISTS mastery_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                concept TEXT NOT NULL,
                prior_mastery REAL NOT NULL,
                new_mastery REAL NOT NULL,
                is_correct INTEGER NOT NULL,
                has_misconception INTEGER NOT NULL,
                source_response_id INTEGER,
                ts REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (source_response_id) REFERENCES responses(id)
            );

            -- Question Calibration (Rasch IRT parameters)
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                concept TEXT NOT NULL,
                difficulty_b REAL NOT NULL,
                initial_label INTEGER NOT NULL,
                attempts_count INTEGER DEFAULT 0,
                correct_count INTEGER DEFAULT 0,
                updated_at REAL NOT NULL
            );

            -- Teacher Interventions & Group Remediation
            CREATE TABLE IF NOT EXISTS interventions (
                id TEXT PRIMARY KEY,
                teacher_id TEXT NOT NULL,
                class_code TEXT NOT NULL,
                target_misconception TEXT NOT NULL,
                title TEXT NOT NULL,
                mini_lesson_plan TEXT NOT NULL,
                assigned_probe_ids TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS intervention_students (
                intervention_id TEXT NOT NULL,
                student_id TEXT NOT NULL,
                pre_mastery REAL,
                post_mastery REAL,
                completed INTEGER DEFAULT 0,
                PRIMARY KEY (intervention_id, student_id),
                FOREIGN KEY (intervention_id) REFERENCES interventions(id),
                FOREIGN KEY (student_id) REFERENCES students(id)
            );

            -- Timed Mock Exams
            CREATE TABLE IF NOT EXISTS mock_exams (
                id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                time_allocated_seconds INTEGER NOT NULL,
                time_spent_seconds INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                score INTEGER NOT NULL,
                accuracy_pct REAL NOT NULL,
                speed_seconds_per_item REAL NOT NULL,
                chapter_breakdown_json TEXT NOT NULL,
                completed_at REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            );

            -- Audit Logs
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                details_json TEXT NOT NULL,
                ts REAL NOT NULL
            );

            -- Indices for high-frequency queries
            CREATE INDEX IF NOT EXISTS idx_responses_student ON responses(student_id);
            CREATE INDEX IF NOT EXISTS idx_mastery_student ON mastery(student_id);
            CREATE INDEX IF NOT EXISTS idx_misc_student ON misconception_events(student_id);
            CREATE INDEX IF NOT EXISTS idx_adj_event ON teacher_adjudications(event_id);
            """);

            # Ensure columns exist on pre-existing databases (migration resilience)
            for table, col, col_type in [
                ("misconception_events", "source", "TEXT DEFAULT 'ai'"),
                ("misconception_events", "evidence_span", "TEXT"),
                ("misconception_events", "alternatives_json", "TEXT DEFAULT '[]'"),
                ("misconception_events", "needs_probe", "INTEGER DEFAULT 0"),
                ("misconception_events", "status", "TEXT DEFAULT 'suspected'"),
                ("responses", "idempotency_key", "TEXT"),
                ("responses", "client_elapsed_ms", "INTEGER DEFAULT 0"),
                ("responses", "is_assisted", "INTEGER DEFAULT 0"),
                ("responses", "confidence", "TEXT DEFAULT 'medium'"),
            ]:
                try:
                    cur.execute(f"PRAGMA table_info({table})")
                    existing_cols = {r["name"] for r in cur.fetchall()}
                    if col not in existing_cols:
                        cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
                except Exception:
                    pass

            conn.commit()
        finally:
            conn.close()

# -----------------------------------------------------------------------------
# STUDENT OPERATIONS & CONSENT (Section 18)
# -----------------------------------------------------------------------------
def save_student(
    student_id: str,
    nickname: str,
    class_code: str = "CBSE10-PHYS",
    consent: bool = True,
    prefs: Optional[Dict[str, Any]] = None,
) -> None:
    """Creates or updates a student profile with consent and accessibility preferences."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            prefs_json = json.dumps(prefs or {"high_contrast": False, "language": "en"})
            cur.execute("""
            INSERT INTO students (id, nickname, class_code, consent_given, accessibility_prefs, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                nickname = excluded.nickname,
                class_code = excluded.class_code,
                accessibility_prefs = excluded.accessibility_prefs
            """, (student_id, nickname, class_code, 1 if consent else 0, prefs_json, time.time()))
            conn.commit()
        finally:
            conn.close()

def get_student(student_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves student profile."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

# -----------------------------------------------------------------------------
# DIAGNOSTIC SESSION AUTOSAVE & RESUME (Section 7 & 13)
# -----------------------------------------------------------------------------
def save_diagnostic_session(
    student_id: str,
    current_index: int,
    answers: Dict[str, int],
    reasonings: Dict[str, str],
    confidences: Dict[str, str],
    scope: str = "blueprint_30",
    is_completed: bool = False,
) -> None:
    """Autosaves active diagnostic state so students can resume seamlessly."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO diagnostic_sessions (student_id, scope, current_index, answers_json, reasonings_json, confidences_json, is_completed, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(student_id) DO UPDATE SET
                scope = excluded.scope,
                current_index = excluded.current_index,
                answers_json = excluded.answers_json,
                reasonings_json = excluded.reasonings_json,
                confidences_json = excluded.confidences_json,
                is_completed = excluded.is_completed,
                updated_at = excluded.updated_at
            """, (
                student_id,
                scope,
                current_index,
                json.dumps(answers),
                json.dumps(reasonings),
                json.dumps(confidences),
                1 if is_completed else 0,
                time.time(),
            ))
            conn.commit()
        finally:
            conn.close()

def get_diagnostic_session(student_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves saved diagnostic session for resumption."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM diagnostic_sessions WHERE student_id = ?", (student_id,))
        row = cur.fetchone()
        if not row:
            return None
        d = dict(row)
        d["answers"] = json.loads(d.get("answers_json") or "{}")
        d["reasonings"] = json.loads(d.get("reasonings_json") or "{}")
        d["confidences"] = json.loads(d.get("confidences_json") or "{}")
        return d
    finally:
        conn.close()

# -----------------------------------------------------------------------------
# ATTEMPT LOGGING WITH IDEMPOTENCY (Section 17)
# -----------------------------------------------------------------------------
class ResponseResult(int):
    """Integer response_id that can also be unpacked as (response_id, is_duplicate)."""
    def __new__(cls, val: int, is_duplicate: bool = False):
        obj = super().__new__(cls, val)
        obj.is_duplicate = is_duplicate
        return obj

    def __iter__(self):
        yield int(self)
        yield self.is_duplicate


def log_response(
    student_id: str,
    question_id: str,
    concept: str,
    chosen: int,
    correct: int,
    reasoning: Optional[str] = None,
    confidence: str = "medium",
    client_elapsed_ms: int = 0,
    is_assisted: bool = False,
    attempt_num: int = 1,
    idempotency_key: Optional[str] = None,
    attempt: Optional[int] = None,
    **kwargs: Any,
) -> ResponseResult:
    """
    Logs student attempt in the immutable responses table.
    Server Authoritative: Checks idempotency_key. If already submitted, returns
    existing response_id and was_duplicate=True without modifying state.
    """
    if attempt is not None:
        attempt_num = attempt
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            if idempotency_key:
                cur.execute("SELECT id FROM responses WHERE idempotency_key = ?", (idempotency_key,))
                existing = cur.fetchone()
                if existing:
                    return ResponseResult(int(existing["id"]), is_duplicate=True)

            cur.execute("""
            INSERT INTO responses (
                student_id, question_id, concept, chosen, correct,
                reasoning, confidence, client_elapsed_ms, is_assisted,
                attempt, idempotency_key, ts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id, question_id, concept, chosen, correct,
                reasoning or "", confidence, client_elapsed_ms,
                1 if is_assisted else 0, attempt_num, idempotency_key, time.time()
            ))
            conn.commit()
            return ResponseResult(int(cur.lastrowid), is_duplicate=False)
        finally:
            conn.close()

# -----------------------------------------------------------------------------
# MISCONCEPTION LOGGING & TEACHER ADJUDICATION (Section 9 & 14)
# -----------------------------------------------------------------------------
def log_misconception_event(
    student_id: str,
    response_id: Optional[Any],
    concept: str,
    misconception_id: str,
    confidence: float,
    evidence_span: Optional[str] = None,
    alternatives: Optional[List[str]] = None,
    needs_probe: bool = False,
    status: str = "suspected",
    **kwargs: Any,
) -> int:
    """Logs a diagnosed misconception matching Blueprint Section 9 inference contract."""
    if isinstance(response_id, (tuple, list)):
        response_id = response_id[0] if len(response_id) > 0 else None
    if evidence_span is None and "evidence" in kwargs:
        evidence_span = kwargs["evidence"]
    source = kwargs.get("source", "ai")
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(misconception_events)")
            cols = {r["name"] for r in cur.fetchall()}

            insert_cols = ["student_id", "response_id", "concept", "misconception_id", "confidence", "ts"]
            insert_vals = [student_id, response_id, concept, misconception_id, confidence, time.time()]

            for c, val in [
                ("evidence_span", evidence_span or ""),
                ("evidence", evidence_span or ""),
                ("alternatives_json", json.dumps(alternatives or [])),
                ("needs_probe", 1 if needs_probe else 0),
                ("status", status),
                ("source", source),
            ]:
                if c in cols:
                    insert_cols.append(c)
                    insert_vals.append(val)

            placeholders = ", ".join(["?"] * len(insert_cols))
            col_names = ", ".join(insert_cols)
            cur.execute(f"INSERT INTO misconception_events ({col_names}) VALUES ({placeholders})", tuple(insert_vals))
            conn.commit()
            return int(cur.lastrowid)
        finally:
            conn.close()

def log_teacher_adjudication(
    event_id: int,
    student_id: str,
    teacher_id: str,
    adjudication_status: str,  # 'confirmed', 'rejected', 'reclassified'
    original_misconception_id: str,
    updated_misconception_id: Optional[str] = None,
    teacher_notes: Optional[str] = None,
) -> int:
    """
    Stores teacher adjudication separately from original model prediction (Blueprint Section 9).
    Updates misconception_events status as well.
    """
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO teacher_adjudications (
                event_id, student_id, teacher_id, adjudication_status,
                original_misconception_id, updated_misconception_id,
                teacher_notes, ts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_id, student_id, teacher_id, adjudication_status,
                original_misconception_id, updated_misconception_id,
                teacher_notes or "", time.time()
            ))
            # Update target event status
            new_status = "confirmed" if adjudication_status == "confirmed" else (
                "rejected" if adjudication_status == "rejected" else "reclassified"
            )
            cur.execute("UPDATE misconception_events SET status = ? WHERE id = ?", (new_status, event_id))
            conn.commit()
            return int(cur.lastrowid)
        finally:
            conn.close()

def get_misconception_events_for_class(class_code: Optional[str] = "CBSE10-PHYS") -> List[Dict[str, Any]]:
    """Fetches all diagnosed misconception events for a class with teacher adjudications joined."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        if class_code and class_code != "ALL":
            cur.execute("""
            SELECT me.*, s.nickname, ta.adjudication_status, ta.teacher_notes, ta.updated_misconception_id
            FROM misconception_events me
            JOIN students s ON me.student_id = s.id
            LEFT JOIN teacher_adjudications ta ON me.id = ta.event_id
            WHERE s.class_code = ?
            ORDER BY me.ts DESC
            """, (class_code,))
        else:
            cur.execute("""
            SELECT me.*, s.nickname, ta.adjudication_status, ta.teacher_notes, ta.updated_misconception_id
            FROM misconception_events me
            JOIN students s ON me.student_id = s.id
            LEFT JOIN teacher_adjudications ta ON me.id = ta.event_id
            ORDER BY me.ts DESC
            """)
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

# -----------------------------------------------------------------------------
# MASTERY STATE PERSISTENCE & EVENT LOGGING (Section 8)
# -----------------------------------------------------------------------------
def save_mastery_state(
    student_id: str,
    concept: str,
    mastery_val: float,
    stability_val: float,
    due_day_val: float,
    prior_mastery: float = 0.30,
    is_correct: bool = True,
    has_misconception: bool = False,
    source_response_id: Optional[int] = None,
) -> None:
    """Updates materialized concept mastery and appends immutable mastery event log."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            now = time.time()

            # 1. Fetch existing evidence count
            cur.execute("SELECT evidence_count FROM mastery WHERE student_id = ? AND concept = ?", (student_id, concept))
            row = cur.fetchone()
            ev_count = (row["evidence_count"] + 1) if row else 1

            state_info = get_mastery_state(mastery_val, ev_count)

            # 2. Upsert materialized mastery
            cur.execute("""
            INSERT INTO mastery (student_id, concept, mastery, stability, due_day, evidence_count, state_label, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(student_id, concept) DO UPDATE SET
                mastery = excluded.mastery,
                stability = excluded.stability,
                due_day = excluded.due_day,
                evidence_count = excluded.evidence_count,
                state_label = excluded.state_label,
                updated_at = excluded.updated_at
            """, (
                student_id, concept, mastery_val, stability_val, due_day_val,
                ev_count, state_info["state"], now
            ))

            # 3. Append to immutable mastery event log
            cur.execute("""
            INSERT INTO mastery_events (
                student_id, concept, prior_mastery, new_mastery,
                is_correct, has_misconception, source_response_id, ts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id, concept, prior_mastery, mastery_val,
                1 if is_correct else 0, 1 if has_misconception else 0,
                source_response_id, now
            ))
            conn.commit()
        finally:
            conn.close()

def get_student_mastery(student_id: str) -> Dict[str, Dict[str, Any]]:
    """Retrieves materialized mastery state for all concepts for a student."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM mastery WHERE student_id = ?", (student_id,))
        rows = cur.fetchall()
        return {r["concept"]: dict(r) for r in rows}
    finally:
        conn.close()

# -----------------------------------------------------------------------------
# REPLAY ENGINE: DETERMINISTIC VERIFICATION (Blueprint Section 8 & 21)
# -----------------------------------------------------------------------------
def replay_student_attempts(student_id: str) -> Dict[str, Any]:
    """
    Blueprint Requirement: 'Replaying attempts reproduces identical state.'
    Reads immutable responses from the responses table, recomputes BKT from scratch,
    and compares recalculated mastery against materialized mastery.
    Returns:
      {
        'match': bool,
        'total_attempts': int,
        'replayed_mastery': dict,
        'stored_mastery': dict,
        'max_discrepancy': float
      }
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
        SELECT * FROM responses
        WHERE student_id = ?
        ORDER BY id ASC
        """, (student_id,))
        attempts = cur.fetchall()

        cur.execute("SELECT * FROM mastery WHERE student_id = ?", (student_id,))
        stored_rows = cur.fetchall()
        stored_mastery = {r["concept"]: round(r["mastery"], 4) for r in stored_rows}

        # Recompute from scratch using BKT
        recalculated: Dict[str, float] = {}
        for att in attempts:
            cid = att["concept"]
            prior = recalculated.get(cid, 0.30)
            is_corr = bool(att["correct"])

            # Check if misconception event occurred on this response
            cur.execute("SELECT confidence FROM misconception_events WHERE response_id = ?", (att["id"],))
            misc_row = cur.fetchone()
            has_m = misc_row is not None
            m_conf = float(misc_row["confidence"]) if has_m else 0.0

            p_next = update_bkt(
                prior_mastery=prior,
                is_correct=is_corr,
                has_misconception=has_m,
                misconception_confidence=m_conf,
            )
            recalculated[cid] = round(p_next, 4)

        max_disc = 0.0
        for cid, val in recalculated.items():
            st_val = stored_mastery.get(cid, 0.30)
            diff = abs(val - st_val)
            if diff > max_disc:
                max_disc = diff

        is_identical = (max_disc < 0.005)
        return {
            "match": is_identical,
            "total_attempts": len(attempts),
            "replayed_mastery": recalculated,
            "stored_mastery": stored_mastery,
            "max_discrepancy": round(max_disc, 5),
        }
    finally:
        conn.close()

# -----------------------------------------------------------------------------
# INTERVENTIONS (Blueprint Section 14 & 15)
# -----------------------------------------------------------------------------
def save_intervention(
    intervention_id: str,
    teacher_id: str,
    class_code: str,
    target_misconception: str,
    title: str,
    mini_lesson_plan: str,
    assigned_probe_ids: List[str],
    student_ids: List[str],
) -> None:
    """Saves a teacher intervention assignment for a targeted student group."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO interventions (
                id, teacher_id, class_code, target_misconception,
                title, mini_lesson_plan, assigned_probe_ids, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                mini_lesson_plan = excluded.mini_lesson_plan,
                assigned_probe_ids = excluded.assigned_probe_ids
            """, (
                intervention_id, teacher_id, class_code, target_misconception,
                title, mini_lesson_plan, json.dumps(assigned_probe_ids), time.time()
            ))

            for sid in student_ids:
                # Read current student mastery for pre-measure
                cur.execute("SELECT AVG(mastery) as avg_m FROM mastery WHERE student_id = ?", (sid,))
                row = cur.fetchone()
                pre_m = row["avg_m"] if (row and row["avg_m"] is not None) else 0.30
                cur.execute("""
                INSERT INTO intervention_students (intervention_id, student_id, pre_mastery, completed)
                VALUES (?, ?, ?, 0)
                ON CONFLICT(intervention_id, student_id) DO NOTHING
                """, (intervention_id, sid, pre_m))

            conn.commit()
        finally:
            conn.close()

def get_class_interventions(class_code: Optional[str] = "CBSE10-PHYS") -> List[Dict[str, Any]]:
    """Retrieves all interventions for a class (or all classes if None/'ALL')."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        if class_code and class_code != "ALL":
            cur.execute("SELECT * FROM interventions WHERE class_code = ? ORDER BY created_at DESC", (class_code,))
        else:
            cur.execute("SELECT * FROM interventions ORDER BY created_at DESC")
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["assigned_probe_ids"] = json.loads(d.get("assigned_probe_ids") or "[]")
            cur.execute("SELECT COUNT(*) as cnt, SUM(completed) as comp FROM intervention_students WHERE intervention_id = ?", (d["id"],))
            sc = cur.fetchone()
            d["assigned_students_count"] = sc["cnt"] if sc else 0
            d["completed_count"] = sc["comp"] if sc else 0
            result.append(d)
        return result
    finally:
        conn.close()

# -----------------------------------------------------------------------------
# TIMED MOCK EXAM PERSISTENCE (Blueprint Section 12 & 13)
# -----------------------------------------------------------------------------
def record_mock_exam(
    exam_id: str,
    student_id: str,
    allocated_seconds: int,
    spent_seconds: int,
    total_q: int,
    score: int,
    chapter_breakdown: Dict[str, Any],
) -> None:
    """Stores timed mock exam performance separate from ongoing practice mastery."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            acc = round((score / max(1, total_q)) * 100.0, 1)
            speed = round(spent_seconds / max(1, total_q), 1)
            cur.execute("""
            INSERT INTO mock_exams (
                id, student_id, time_allocated_seconds, time_spent_seconds,
                total_questions, score, accuracy_pct, speed_seconds_per_item,
                chapter_breakdown_json, completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                exam_id, student_id, allocated_seconds, spent_seconds,
                total_q, score, acc, speed, json.dumps(chapter_breakdown), time.time()
            ))
            conn.commit()
        finally:
            conn.close()

def get_student_mock_exams(student_id: str) -> List[Dict[str, Any]]:
    """Retrieves mock exam history for a student."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM mock_exams WHERE student_id = ? ORDER BY completed_at DESC", (student_id,))
        rows = cur.fetchall()
        res = []
        for r in rows:
            d = dict(r)
            d["chapter_breakdown"] = json.loads(d.get("chapter_breakdown_json") or "{}")
            res.append(d)
        return res
    finally:
        conn.close()

# -----------------------------------------------------------------------------
# PRIVACY & DATA EXPORT / DELETION (Blueprint Section 18)
# -----------------------------------------------------------------------------
def export_student_data_json(student_id: str) -> str:
    """Exports all student records in portable JSON format for GDPR/data transparency."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        st_row = cur.fetchone()
        cur.execute("SELECT * FROM responses WHERE student_id = ? ORDER BY ts ASC", (student_id,))
        resp_rows = cur.fetchall()
        cur.execute("SELECT * FROM mastery WHERE student_id = ?", (student_id,))
        mast_rows = cur.fetchall()
        cur.execute("SELECT * FROM misconception_events WHERE student_id = ?", (student_id,))
        misc_rows = cur.fetchall()
        cur.execute("SELECT * FROM mock_exams WHERE student_id = ?", (student_id,))
        mock_rows = cur.fetchall()

        payload = {
            "student_profile": dict(st_row) if st_row else {},
            "responses": [dict(r) for r in resp_rows],
            "mastery": [dict(r) for r in mast_rows],
            "misconception_events": [dict(r) for r in misc_rows],
            "mock_exams": [dict(r) for r in mock_rows],
            "exported_at": time.time(),
        }
        return json.dumps(payload, indent=2)
    finally:
        conn.close()

def delete_student_data(student_id: str) -> None:
    """Permanently deletes student records upon verified deletion request (Section 18)."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM misconception_events WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM responses WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM mastery WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM mastery_events WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM diagnostic_sessions WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM mock_exams WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM intervention_students WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
        finally:
            conn.close()

# -----------------------------------------------------------------------------
# RASCH ITEM CALIBRATION STORE (Section 10)
# -----------------------------------------------------------------------------
def get_item_calibration(question_id: str, default_label: int = 2) -> Tuple[float, int, int]:
    """Fetches calibrated difficulty b, n_answers, and n_correct for an item."""
    from core.calibration import LABEL_TO_B0
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT calibrated_b, n_answers, n_correct FROM items WHERE question_id = ?", (question_id,))
        row = cur.fetchone()
        if row:
            return float(row["calibrated_b"]), int(row["n_answers"]), int(row["n_correct"])
        return LABEL_TO_B0.get(default_label, 0.0), 0, 0
    finally:
        conn.close()

def save_item_calibration(
    question_id: str,
    difficulty_label: int,
    new_b: float,
    is_correct: bool,
    *args, **kwargs
) -> None:
    """Saves updated Rasch calibrated difficulty b."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO items (question_id, difficulty_label, calibrated_b, n_answers, n_correct)
            VALUES (?, ?, ?, 1, ?)
            ON CONFLICT(question_id) DO UPDATE SET
                calibrated_b = excluded.calibrated_b,
                n_answers = n_answers + 1,
                n_correct = n_correct + excluded.n_correct
            """, (question_id, difficulty_label, new_b, 1 if is_correct else 0))
            conn.commit()
        finally:
            conn.close()

def get_all_calibrated_items() -> List[Dict[str, Any]]:
    """Returns calibration statistics for all questions in the bank."""
    from core.bank import QUESTION_BANK
    from core.calibration import LABEL_TO_B0, format_calibration_summary
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT question_id, difficulty_label, calibrated_b, n_answers, n_correct FROM items")
            db_items = {r["question_id"]: r for r in cur.fetchall()}

            result = []
            for q in QUESTION_BANK:
                qid = q["id"]
                label_d = q["difficulty_label"]
                if qid in db_items:
                    row = db_items[qid]
                    cal_b = float(row["calibrated_b"])
                    n_ans = int(row["n_answers"])
                    n_cor = int(row["n_correct"])
                else:
                    cal_b = LABEL_TO_B0.get(label_d, 0.0)
                    n_ans = 0
                    n_cor = 0

                summary = format_calibration_summary(label_d, cal_b, n_ans)
                result.append({
                    "Question_ID": qid,
                    "Concept": q["concept"],
                    "Label_Level": label_d,
                    "Labelled_b0": summary["labelled_b"],
                    "Calibrated_b": summary["calibrated_b"],
                    "Responses_Seen": n_ans,
                    "Success_Rate": f"{int((n_cor / n_ans) * 100)}%" if n_ans > 0 else "N/A",
                    "Calibration_Status": summary["status"],
                })

            return result
        finally:
            conn.close()

def save_item_calibration(
    item_id: str,
    concept: str,
    difficulty_b: float,
    initial_label: int,
    attempts: int,
    correct: int,
) -> None:
    """Saves calibrated difficulty b."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO items (question_id, difficulty_label, calibrated_b, n_answers, n_correct)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(question_id) DO UPDATE SET
                calibrated_b = excluded.calibrated_b,
                n_answers = excluded.n_answers,
                n_correct = excluded.n_correct
            """, (item_id, initial_label, difficulty_b, attempts, correct))
            conn.commit()
        finally:
            conn.close()

def get_real_students_mastery(class_code: str = "CBSE10-PHYS") -> List[Dict[str, Any]]:
    """Returns a list of real student mastery records formatted for teacher dashboard/heatmaps."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, nickname FROM students WHERE class_code = ?", (class_code,))
        students = cur.fetchall()
        result = []
        for s in students:
            sid = s["id"]
            nick = s["nickname"]
            cur.execute("SELECT concept, mastery FROM mastery WHERE student_id = ?", (sid,))
            m_rows = cur.fetchall()
            rec = {
                "Student": nick,
                "ID": sid,
                "Class": class_code,
                "Is_Simulated": False,
            }
            for m in m_rows:
                rec[m["concept"]] = m["mastery"]
            result.append(rec)
        return result
    finally:
        conn.close()

def get_available_classes() -> List[str]:
    """Returns distinct class codes from students table."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT class_code FROM students")
        rows = cur.fetchall()
        classes = [r["class_code"] for r in rows if r["class_code"]]
        return classes if classes else ["CBSE10-PHYS", "CLASS-10A"]
    finally:
        conn.close()

def get_real_misconception_stats(class_code: str = "CBSE10-PHYS") -> Dict[str, int]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
        SELECT me.misconception_id, COUNT(*) as cnt
        FROM misconception_events me
        JOIN students s ON me.student_id = s.id
        WHERE s.class_code = ?
        GROUP BY me.misconception_id
        """, (class_code,))
        rows = cur.fetchall()
        return {r["misconception_id"]: r["cnt"] for r in rows}
    finally:
        conn.close()
