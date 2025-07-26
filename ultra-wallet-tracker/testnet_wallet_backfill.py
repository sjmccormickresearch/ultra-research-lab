import requests, sqlite3, os, time
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# === CONFIG ===
HYPERION = "https://test.ultra.eosusa.io"
DB_FILE = os.path.join("data", "wallets_testnet.db")
EXPORT_DIR = "daily_exports/testnet"
os.makedirs(EXPORT_DIR, exist_ok=True)

# === DB SETUP ===
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

# === BACKFILL LOOP ===
def backfill_wallets(start_time="2018-01-01T00:00:00Z", max_pages=9999, delay=0.5):
    print("🚀 Starting TESTNET backfill from:", start_time)
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
        try:
            r = requests.get(f"{HYPERION}/v2/history/get_actions", params=params, timeout=10)
            data = r.json()
        except Exception as e:
            print("❌ Request failed:", e)
            break

        actions = data.get("actions", [])
        if not actions:
            print("✅ No more actions. Testnet backfill complete.")
            break

        wallets = [{
            "name": act["act"]["data"]["newact"],
            "timestamp": act["timestamp"],
            "creator": act["act"]["data"]["creator"],
            "trx_id": act["trx_id"]
        } for act in actions]

        inserted = insert_wallets(conn, wallets)
        total_inserted += inserted
        print(f"  ↳ Inserted {inserted} new wallet(s)")

        # Update cursor to last timestamp (for next page)
        cursor = actions[-1]["timestamp"]
        time.sleep(delay)

    conn.close()
    print(f"\n🎉 Testnet backfill finished. Total inserted: {total_inserted}")

# === PLOT RESULTS ===
def plot_wallet_growth():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT timestamp FROM wallets", conn)
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    daily_counts = df.groupby("date").size().reset_index(name="wallets_created")

    out_csv = os.path.join("data", "wallet_growth_testnet.csv")
    out_png = os.path.join("exports", "wallets_growth_testnet.png")
    daily_counts.to_csv(out_csv, index=False)

    plt.figure(figsize=(10, 5))
    plt.plot(daily_counts["date"], daily_counts["wallets_created"], marker="o")
    plt.title("New Testnet Wallets Created Per Day")
    plt.xlabel("Date")
    plt.ylabel("Wallets Created")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    print(f"📊 Saved graph to {out_png}")

# === MAIN ===
if __name__ == "__main__":
    backfill_wallets(start_time="2018-01-01T00:00:00Z")
    plot_wallet_growth()
