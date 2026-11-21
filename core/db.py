"""core/db.py - SQLite Thread-Safe Data Store

Implements schema and persistence for:
- students
- responses
- misconception_events
- mastery
- items (difficulty calibration)
- generated_questions
"""

import os
import sqlite3
import threading
import time
from typing import List, Dict, Any, Optional

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
    """Initializes tables and indexes if they do not exist."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.executescript("""
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                nickname TEXT NOT NULL,
                class_code TEXT DEFAULT 'DEFAULT',
                created_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                concept TEXT NOT NULL,
                chosen INTEGER NOT NULL,
                correct INTEGER NOT NULL,
                reasoning TEXT,
                attempt INTEGER NOT NULL,
                ts REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            );

            CREATE TABLE IF NOT EXISTS misconception_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                response_id INTEGER,
                concept TEXT NOT NULL,
                misconception_id TEXT NOT NULL,
                confidence REAL NOT NULL,
                evidence TEXT,
                source TEXT NOT NULL, -- 'ai' or 'option'
                ts REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (response_id) REFERENCES responses(id)
            );

            CREATE TABLE IF NOT EXISTS mastery (
                student_id TEXT NOT NULL,
                concept TEXT NOT NULL,
                mastery REAL NOT NULL,
                stability REAL NOT NULL,
                due_day REAL NOT NULL,
                streak INTEGER DEFAULT 0,
                updated_at REAL NOT NULL,
                PRIMARY KEY (student_id, concept)
            );

            CREATE TABLE IF NOT EXISTS items (
                question_id TEXT PRIMARY KEY,
                difficulty_label INTEGER NOT NULL,
                calibrated_b REAL NOT NULL,
                n_answers INTEGER DEFAULT 0,
                n_correct INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS generated_questions (
                id TEXT PRIMARY KEY,
                concept TEXT NOT NULL,
                json_data TEXT NOT NULL,
                verified INTEGER NOT NULL,
                created_at REAL NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_responses_student ON responses(student_id);
            CREATE INDEX IF NOT EXISTS idx_responses_concept ON responses(concept);
            CREATE INDEX IF NOT EXISTS idx_misc_events_student ON misconception_events(student_id);
            CREATE INDEX IF NOT EXISTS idx_misc_events_mid ON misconception_events(misconception_id);
            """)
            conn.commit()
        finally:
            conn.close()

def save_student(student_id: str, nickname: str, class_code: str = "DEFAULT") -> None:
    """Inserts or updates a student profile."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT OR REPLACE INTO students (id, nickname, class_code, created_at)
            VALUES (?, ?, ?, ?)
            """, (student_id, nickname, class_code, time.time()))
            conn.commit()
        finally:
            conn.close()

def log_response(
    student_id: str,
    question_id: str,
    concept: str,
    chosen: int,
    correct: bool,
    reasoning: str,
    attempt: int,
) -> int:
    """Logs an attempt and returns the response row ID."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO responses (student_id, question_id, concept, chosen, correct, reasoning, attempt, ts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, question_id, concept, chosen, 1 if correct else 0, reasoning, attempt, time.time()))
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

def log_misconception_event(
    student_id: str,
    response_id: Optional[int],
    concept: str,
    misconception_id: str,
    confidence: float,
    evidence: str,
    source: str = "ai",
) -> None:
    """Records an identified misconception event."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO misconception_events
            (student_id, response_id, concept, misconception_id, confidence, evidence, source, ts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, response_id, concept, misconception_id, confidence, evidence, source, time.time()))
            conn.commit()
        finally:
            conn.close()

def save_mastery_state(
    student_id: str,
    concept: str,
    mastery_val: float,
    stability: float,
    due_day: float,
    streak: int,
) -> None:
    """Persists current concept mastery and spaced repetition state."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT OR REPLACE INTO mastery (student_id, concept, mastery, stability, due_day, streak, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (student_id, concept, mastery_val, stability, due_day, streak, time.time()))
            conn.commit()
        finally:
            conn.close()

def get_item_calibration(question_id: str, default_label: int) -> Tuple[float, int, int]:
    """Retrieves (calibrated_b, n_answers, n_correct) for an item."""
    from core.calibration import LABEL_TO_B0
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT calibrated_b, n_answers, n_correct FROM items WHERE question_id = ?", (question_id,))
            row = cur.fetchone()
            if row:
                return float(row["calibrated_b"]), int(row["n_answers"]), int(row["n_correct"])
            else:
                default_b = LABEL_TO_B0.get(default_label, 0.0)
                return default_b, 0, 0
        finally:
            conn.close()

def save_item_calibration(
    question_id: str,
    difficulty_label: int,
    calibrated_b: float,
    is_correct: bool,
) -> None:
    """Updates item calibration stats in SQLite."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO items (question_id, difficulty_label, calibrated_b, n_answers, n_correct)
            VALUES (?, ?, ?, 1, ?)
            ON CONFLICT(question_id) DO UPDATE SET
                calibrated_b = excluded.calibrated_b,
                n_answers = items.n_answers + 1,
                n_correct = items.n_correct + excluded.n_correct
            """, (question_id, difficulty_label, calibrated_b, 1 if is_correct else 0))
            conn.commit()
        finally:
            conn.close()

def delete_student_data(student_id: str) -> None:
    """GDPR / Privacy compliance: removes student responses and mastery records."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM misconception_events WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM responses WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM mastery WHERE student_id = ?", (student_id,))
            cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
        finally:
            conn.close()

def get_available_classes() -> List[str]:
    """Returns distinct class codes present in the database."""
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT class_code FROM students ORDER BY class_code")
            rows = cur.fetchall()
            return [r["class_code"] for r in rows if r["class_code"]]
        finally:
            conn.close()

def get_real_students_mastery(class_code: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns real students and their concept mastery scores.
    Joined with students table to preserve class grouping.
    """
    from core.concepts import CONCEPTS
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            if class_code and class_code != "ALL":
                cur.execute("SELECT id, nickname, class_code FROM students WHERE class_code = ? ORDER BY nickname", (class_code,))
            else:
                cur.execute("SELECT id, nickname, class_code FROM students ORDER BY nickname")
            students = cur.fetchall()

            result = []
            for stu in students:
                cur.execute("SELECT concept, mastery FROM mastery WHERE student_id = ?", (stu["id"],))
                m_rows = cur.fetchall()
                m_dict = {r["concept"]: round(float(r["mastery"]), 2) for r in m_rows}
                
                # Only include students who have recorded at least one concept mastery
                if m_dict:
                    record = {
                        "Student": stu["nickname"],
                        "ID": stu["id"],
                        "Class": stu["class_code"],
                        "Is_Simulated": False,
                    }
                    for cid in CONCEPTS:
                        record[cid] = m_dict.get(cid, 0.30)
                    result.append(record)

            return result
        finally:
            conn.close()

def get_real_misconception_stats(class_code: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns aggregated frequency counts of detected misconceptions from real students."""
    from core.concepts import MISCONCEPTIONS
    with _LOCK:
        conn = get_connection()
        try:
            cur = conn.cursor()
            query = """
            SELECT m.misconception_id, COUNT(DISTINCT m.student_id) as student_count
            FROM misconception_events m
            JOIN students s ON m.student_id = s.id
            """
            params = []
            if class_code and class_code != "ALL":
                query += " WHERE s.class_code = ? "
                params.append(class_code)
            query += " GROUP BY m.misconception_id"

            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            counts = {r["misconception_id"]: r["student_count"] for r in rows}

            stats = []
            for mid, m_info in MISCONCEPTIONS.items():
                cnt = counts.get(mid, 0)
                stats.append({
                    "Misconception_ID": mid,
                    "Misconception": m_info["label"],
                    "Affected_Students": cnt,
                    "Teacher_Action": m_info["reteach_action"],
                    "Correction": m_info["correction"],
                    "Source": "REAL",
                })

            return sorted(stats, key=lambda x: x["Affected_Students"], reverse=True)
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

