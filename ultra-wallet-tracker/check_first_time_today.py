# check_first_time_today.py
import sqlite3
import pandas as pd
from datetime import datetime

def check_first_time_deployers(db_path, label):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("""
        SELECT account, timestamp, label, category
        FROM setcode
        WHERE first_seen = 1
        AND DATE(timestamp) = DATE('now', 'localtime')
    """, conn)
    conn.close()

    if df.empty:
        print(f"✅ {label}: No new first-time contract deployers today.")
        return 0
    else:
        print(f"🚨 {label}: {len(df)} new first-time deployments today:")
        print(df.to_string(index=False))
        output_file = f"data/first_time_{label.lower()}_{datetime.today().date()}.csv"
        df.to_csv(output_file, index=False)
        print(f"📁 Saved to: {output_file}")
        return len(df)

if __name__ == "__main__":
    print("🔍 Checking for first-time deployers...\n")
    testnet_count = check_first_time_deployers("data/setcode_testnet.db", "Testnet")
    mainnet_count = check_first_time_deployers("data/setcode_mainnet.db", "Mainnet")

    total = testnet_count + mainnet_count
    print(f"\n📊 Total new first-time deployers today: {total}")
