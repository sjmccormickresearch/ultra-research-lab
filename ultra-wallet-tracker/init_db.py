import sqlite3

conn = sqlite3.connect("wallets.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS wallets (
    name TEXT PRIMARY KEY,
    timestamp TEXT,
    creator TEXT,
    trx_id TEXT
)
""")

conn.commit()
conn.close()
