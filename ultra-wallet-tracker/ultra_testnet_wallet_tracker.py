import requests, sqlite3, os
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
import pandas as pd

# === CONFIG ===
HYPERION = "https://test.ultra.eosusa.io"
DB_FILE = os.path.join("data", "wallets_testnet.db")
EXPORT_DIR = "daily_exports/testnet"
os.makedirs(EXPORT_DIR, exist_ok=True)

# === DB ===
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

def get_latest_timestamp(conn):
    c = conn.cursor()
    result = c.execute("SELECT MAX(timestamp) FROM wallets").fetchone()
    if result and result[0]:
        return result[0]
    else:
        # If DB is empty, start from earliest possible date
        return "2018-01-01T00:00:00Z"

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

def fetch_new_accounts(after_iso):
    url = f"{HYPERION}/v2/history/get_actions"
    params = {
        "account": "eosio",
        "filter": "eosio:newaccount",
        "sort": "asc",
        "after": after_iso,
        "limit": 100
    }
    print(f"🔗 Querying Testnet: {url} (after: {after_iso})")
    r = requests.get(url, params=params)
    data = r.json()

    results = []
    for action in data.get("actions", []):
        act_data = action["act"]["data"]
        results.append({
            "name": act_data["newact"],
            "timestamp": action["timestamp"],
            "creator": act_data["creator"],
            "trx_id": action["trx_id"]
        })
    return results

def sync_wallets():
    conn = init_db()
    latest = get_latest_timestamp(conn)
    total_inserted = 0
    page = 0
    previous_cursor = None

    while True:
        page += 1
        print(f"📦 Page {page} | After: {latest}")
        wallets = fetch_new_accounts(latest)

        if not wallets:
            print("✅ No new actions. Sync complete.")
            break

        inserted = insert_wallets(conn, wallets)
        total_inserted += inserted
        print(f"  ↳ Inserted {inserted} wallet(s)")

        new_cursor = wallets[-1]["timestamp"]

        if new_cursor == previous_cursor:
            print("⚠️ Cursor did not advance — stopping to prevent infinite loop.")
            break

        previous_cursor = latest
        latest = new_cursor

    conn.close()
    print(f"\n🎉 Sync complete. Total inserted: {total_inserted}")


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
    print("🔄 Ultra Testnet Wallet Tracker (Auto-Catchup Mode)")
    sync_wallets()
    plot_wallet_growth()
