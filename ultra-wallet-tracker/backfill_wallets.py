# run once to populate the chart

import os
import time
import sqlite3
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

DB_FILE = "wallets.db"
HYPERION = "https://ultra.eosusa.io"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS wallets (
        name TEXT PRIMARY KEY,
        timestamp TEXT,
        creator TEXT,
        trx_id TEXT
    )""")
    conn.commit()
    return conn

def insert_wallets(conn, wallets):
    c = conn.cursor()
    count = 0
    for w in wallets:
        try:
            c.execute("INSERT INTO wallets VALUES (?, ?, ?, ?)",
                      (w["name"], w["timestamp"], w["creator"], w["trx_id"]))
            count += 1
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    return count

def backfill_wallets(start_time="2019-01-01T00:00:00Z", max_pages=99999, delay=0.5):
    print("🚀 Starting backfill from:", start_time)
    conn = init_db()
    cursor = start_time
    total_inserted = 0

    for page in range(max_pages):
        params = {
            "account": "eosio",
            "filter": "eosio:newaccount",
            "sort": "asc",
            "after": cursor,
            "limit": 100
        }
        print(f"📦 Page {page+1} | After: {cursor}")
        r = requests.get(f"{HYPERION}/v2/history/get_actions", params=params)
        data = r.json()
        actions = data.get("actions", [])

        if not actions:
            print("✅ No more actions. Backfill complete.")
            break

        wallets = []
        for action in actions:
            act = action["act"]["data"]
            wallets.append({
                "name": act["newact"],
                "timestamp": action["timestamp"],
                "creator": act["creator"],
                "trx_id": action["trx_id"]
            })

        inserted = insert_wallets(conn, wallets)
        total_inserted += inserted
        print(f"  ↳ Inserted {inserted} new wallet(s)")

        cursor = actions[-1]["timestamp"]
        time.sleep(delay)

    conn.close()
    print(f"\n🎉 Backfill finished. Total inserted: {total_inserted}")

    return total_inserted

def plot_wallet_growth():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT timestamp FROM wallets", conn)
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    daily_counts = df.groupby("date").size().reset_index(name="wallets_created")
    daily_counts.to_csv("wallet_growth_timeseries.csv", index=False)

    plt.figure(figsize=(10, 5))
    plt.plot(daily_counts["date"], daily_counts["wallets_created"], marker="o")
    plt.title("New Ultra Wallets Created Per Day")
    plt.xlabel("Date")
    plt.ylabel("Wallets Created")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("wallets_growth.png")
    plt.close()
    print("📊 Saved graph to wallets_growth.png")

if __name__ == "__main__":
    backfill_wallets()
    plot_wallet_growth()
