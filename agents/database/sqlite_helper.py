# sqlite_helper.py
import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class SQLiteHelper:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.join(os.getenv('DATA_DIR', 'data'), 'wisdomwealth.db')
        
        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.init_tables()
    
    def init_tables(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                -- Incidents table for logging all security events
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    input_text TEXT NOT NULL,
                    risk_level TEXT NOT NULL,
                    response TEXT NOT NULL,
                    agent_traces TEXT, -- JSON array of agent names
                    actions TEXT, -- JSON array of actions
                    confidence_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
                
                -- Family preferences table
                CREATE TABLE IF NOT EXISTS family_prefs (
                    user_id TEXT PRIMARY KEY,
                    allow_alerts BOOLEAN DEFAULT TRUE,
                    alert_threshold TEXT DEFAULT 'MEDIUM', -- LOW, MEDIUM, HIGH
                    contacts TEXT, -- JSON array of contacts
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Users table for basic user info
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Pending alerts table
                CREATE TABLE IF NOT EXISTS pending_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    incident_id INTEGER NOT NULL,
                    alert_type TEXT NOT NULL, -- FAMILY, FRAUD, HEALTHCARE, ESTATE
                    alert_message TEXT NOT NULL,
                    status TEXT DEFAULT 'PENDING', -- PENDING, SENT, FAILED
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (incident_id) REFERENCES incidents(id)
                );
                
                -- Create indexes for better performance
                CREATE INDEX IF NOT EXISTS idx_incidents_user_id ON incidents(user_id);
                CREATE INDEX IF NOT EXISTS idx_incidents_created_at ON incidents(created_at);
                CREATE INDEX IF NOT EXISTS idx_incidents_risk_level ON incidents(risk_level);
                CREATE INDEX IF NOT EXISTS idx_pending_alerts_user_id ON pending_alerts(user_id);
                CREATE INDEX IF NOT EXISTS idx_pending_alerts_status ON pending_alerts(status);
            """)
    
    def insert_incident(self, user_id: str, input_text: str, risk_level: str, 
                       response: str, agent_traces: List[str] = None, 
                       actions: List[str] = None, confidence_score: float = None) -> int:
        """Insert new incident and return incident ID"""
        agent_traces_json = json.dumps(agent_traces or [])
        actions_json = json.dumps(actions or [])
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO incidents (user_id, input_text, risk_level, response, 
                                     agent_traces, actions, confidence_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, input_text, risk_level, response, 
                  agent_traces_json, actions_json, confidence_score))
            
            return cursor.lastrowid
    
    def select_recent_incidents(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Get recent incidents for a user"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM incidents 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (user_id, limit))
            
            incidents = []
            for row in cursor.fetchall():
                incident = dict(row)
                incident['agent_traces'] = json.loads(incident['agent_traces'] or '[]')
                incident['actions'] = json.loads(incident['actions'] or '[]')
                incidents.append(incident)
            
            return incidents
    
    def get_incident_by_id(self, incident_id: int) -> Optional[Dict]:
        """Get incident by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,))
            row = cursor.fetchone()
            
            if row:
                incident = dict(row)
                incident['agent_traces'] = json.loads(incident['agent_traces'] or '[]')
                incident['actions'] = json.loads(incident['actions'] or '[]')
                return incident
            
            return None
    
    def upsert_family_prefs(self, user_id: str, allow_alerts: bool = True, 
                           alert_threshold: str = 'MEDIUM', contacts: List[Dict] = None) -> bool:
        """Insert or update family preferences"""
        contacts_json = json.dumps(contacts or [])
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO family_prefs 
                (user_id, allow_alerts, alert_threshold, contacts, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (user_id, allow_alerts, alert_threshold, contacts_json))
            
            return cursor.rowcount > 0
    
    def get_family_prefs(self, user_id: str) -> Optional[Dict]:
        """Get family preferences for user"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM family_prefs WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                prefs = dict(row)
                prefs['contacts'] = json.loads(prefs['contacts'] or '[]')
                return prefs
            
            return None
    
    def insert_pending_alert(self, user_id: str, incident_id: int, 
                            alert_type: str, alert_message: str) -> int:
        """Insert pending family alert"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pending_alerts (user_id, incident_id, alert_type, alert_message)
                VALUES (?, ?, ?, ?)
            """, (user_id, incident_id, alert_type, alert_message))
            
            return cursor.lastrowid
    
    def get_pending_alerts(self, user_id: str = None) -> List[Dict]:
        """Get pending alerts, optionally filtered by user"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute("""
                    SELECT * FROM pending_alerts 
                    WHERE user_id = ? AND status = 'PENDING'
                    ORDER BY created_at DESC
                """, (user_id,))
            else:
                cursor.execute("""
                    SELECT * FROM pending_alerts 
                    WHERE status = 'PENDING'
                    ORDER BY created_at DESC
                """)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def update_alert_status(self, alert_id: int, status: str) -> bool:
        """Update alert status (PENDING -> SENT/FAILED)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pending_alerts 
                SET status = ?
                WHERE id = ?
            """, (status, alert_id))
            
            return cursor.rowcount > 0
    
    def upsert_user(self, user_id: str, name: str = None, age: int = None) -> bool:
        """Insert or update user info"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO users 
                (user_id, name, age, last_seen)
                VALUES (?, COALESCE(?, (SELECT name FROM users WHERE user_id = ?)), 
                        COALESCE(?, (SELECT age FROM users WHERE user_id = ?)), 
                        CURRENT_TIMESTAMP)
            """, (user_id, name, user_id, age, user_id))
            
            return cursor.rowcount > 0
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user info"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            
            return dict(row) if row else None
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Total incidents by risk level
            cursor.execute("""
                SELECT risk_level, COUNT(*) as count 
                FROM incidents 
                GROUP BY risk_level
            """)
            stats['incidents_by_risk'] = dict(cursor.fetchall())
            
            # Total users
            cursor.execute("SELECT COUNT(*) FROM users")
            stats['total_users'] = cursor.fetchone()[0]
            
            # Recent incidents (last 24 hours)
            cursor.execute("""
                SELECT COUNT(*) FROM incidents 
                WHERE created_at > datetime('now', '-1 day')
            """)
            stats['recent_incidents'] = cursor.fetchone()[0]
            
            # Pending alerts
            cursor.execute("SELECT COUNT(*) FROM pending_alerts WHERE status = 'PENDING'")
            stats['pending_alerts'] = cursor.fetchone()[0]
            
            return stats
    
    def cleanup_old_data(self, days: int = 90) -> int:
        """Clean up old incidents (keep only last N days)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM incidents 
                WHERE created_at < datetime('now', '-{} days')
            """.format(days))
            
            deleted_count = cursor.rowcount
            
            # Clean up orphaned pending alerts
            cursor.execute("""
                DELETE FROM pending_alerts 
                WHERE incident_id NOT IN (SELECT id FROM incidents)
            """)
            
            return deleted_count