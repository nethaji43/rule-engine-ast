import sqlite3
import json

def get_connection():
    conn = sqlite3.connect('rules.db')
    return conn

def store_rule(rule_string, ast):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rules (rule_string, ast)
        VALUES (?, ?)
    ''', (rule_string, json.dumps(ast, default=lambda o: o.__dict__)))
    conn.commit()
    conn.close()

def get_all_rules():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT ast FROM rules')
    rows = cursor.fetchall()
    conn.close()
    return [json.loads(row[0]) for row in rows]

# DB schema creation
def create_schema():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_string TEXT NOT NULL,
            ast TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB schema on first run
create_schema()
