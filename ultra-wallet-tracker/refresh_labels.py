import sqlite3
from labels import KNOWN_ACCOUNTS

DB_FILE = "data/setcode_testnet.db"

def relabel_existing_deployments():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    updated = 0
    for account, meta in KNOWN_ACCOUNTS.items():
        c.execute("""
            UPDATE setcode
            SET label = ?, category = ?
            WHERE account = ? AND (label IS NULL OR category IS NULL)
        """, (meta.get("label"), meta.get("category"), account))
        updated += c.rowcount

    conn.commit()
    conn.close()
    print(f"✅ Updated {updated} existing deployments with fresh labels.")

if __name__ == "__main__":
    relabel_existing_deployments()
