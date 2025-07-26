import sqlite3
import csv
import os

DB_FILE = "data/setcode_testnet.db"
EXPORT_CSV = "data/setcode_deployer_summary.csv"

def print_top_deployers(n=50):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT account, COUNT(*) as deployments
        FROM setcode
        GROUP BY account
        ORDER BY deployments DESC
        LIMIT ?
    """, (n,))
    rows = c.fetchall()

    print(f"\n🧠 Top {n} Contract Deployers on Testnet:\n")
    for acct, count in rows:
        print(f"{acct:<20} {count} deployments")
    conn.close()

def count_one_time_deployers():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM (
            SELECT account FROM setcode
            GROUP BY account
            HAVING COUNT(*) = 1
        )
    """)
    count = c.fetchone()[0]
    conn.close()
    print(f"\n📉 {count} accounts have only deployed once.\n")

def export_all_deployers_to_csv():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT account, COUNT(*) as deployments
        FROM setcode
        GROUP BY account
        ORDER BY deployments DESC
    """)
    rows = c.fetchall()
    conn.close()

    with open(EXPORT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["account", "deployments"])
        writer.writerows(rows)

    print(f"📁 Full deployer summary exported to: {EXPORT_CSV}")

if __name__ == "__main__":
    print_top_deployers(n=50)
    count_one_time_deployers()
    export_all_deployers_to_csv()
