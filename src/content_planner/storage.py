import json
import sqlite3
from pathlib import Path


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class Storage:
    def __init__(self, path: str | Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY, request_id TEXT NOT NULL UNIQUE,
                input_hash TEXT NOT NULL, state_json TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS steps (
                call_id TEXT PRIMARY KEY, task_id TEXT NOT NULL REFERENCES tasks(task_id),
                tool TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS tool_receipts (
                call_id TEXT PRIMARY KEY REFERENCES steps(call_id), payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS ledger (
                charge_id TEXT PRIMARY KEY, task_id TEXT NOT NULL REFERENCES tasks(task_id),
                call_id TEXT NOT NULL UNIQUE, milliunits INTEGER NOT NULL CHECK(milliunits>=0));
            CREATE TABLE IF NOT EXISTS solutions (
                solution_id TEXT PRIMARY KEY, task_id TEXT NOT NULL UNIQUE REFERENCES tasks(task_id),
                payload TEXT NOT NULL);
        """)

    def close(self):
        self.connection.close()

    def get(self, request_id):
        row = self.connection.execute("SELECT state_json FROM tasks WHERE request_id=?", (request_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def claim(self, state):
        try:
            with self.connection:
                self.connection.execute("INSERT INTO tasks VALUES (?,?,?,?)", (
                    state["task_id"], state["input"]["request_id"], state["input_hash"], encode(state)))
            return True
        except sqlite3.IntegrityError:
            return False

    def commit(self, state, receipt=None, solution=None):
        """Persist a complete action atomically, including save receipt and ledger."""
        with self.connection:
            if receipt:
                self.connection.execute("INSERT INTO steps VALUES (?,?,?,?,?)", (
                    receipt["call_id"], state["task_id"], receipt["tool"],
                    "succeeded" if receipt["ok"] else "failed", encode(receipt)))
                self.connection.execute("INSERT INTO tool_receipts VALUES (?,?)", (receipt["call_id"], encode(receipt)))
            for charge in state["ledger"]:
                self.connection.execute("INSERT OR IGNORE INTO ledger VALUES (?,?,?,?)", (
                    charge["id"], state["task_id"], charge["call_id"], charge["milliunits"]))
            if solution:
                self.connection.execute("INSERT INTO solutions VALUES (?,?,?)", (
                    solution["id"], state["task_id"], encode(solution)))
            self.connection.execute("UPDATE tasks SET state_json=? WHERE task_id=?", (encode(state), state["task_id"]))

    def solution(self, task_id):
        row = self.connection.execute("SELECT payload FROM solutions WHERE task_id=?", (task_id,)).fetchone()
        return json.loads(row[0]) if row else None
