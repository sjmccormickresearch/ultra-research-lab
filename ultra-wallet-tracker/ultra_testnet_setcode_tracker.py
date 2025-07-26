import requests, sqlite3, os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# === CONFIG ===
HYPERION = "https://test.ultra.eosusa.io"
DB_FILE = os.path.join("data", "setcode_testnet.db")
EXPORT_DIR = "daily_exports/testnet"
os.makedirs(EXPORT_DIR, exist_ok=True)

# === LABELS ===
from labels import KNOWN_ACCOUNTS



# === DB ===
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS setcode (
            account TEXT,
            timestamp TEXT,
            trx_id TEXT PRIMARY KEY,
            first_seen INTEGER,
            label TEXT,
            category TEXT
        )
    """)
    conn.commit()
    return conn

def has_seen_before(conn, account):
    c = conn.cursor()
    result = c.execute("SELECT 1 FROM setcode WHERE account = ? LIMIT 1", (account,)).fetchone()
    return result is not None

def insert_setcodes(conn, deployments):
    c = conn.cursor()
    count = 0
    for d in deployments:
        try:
            c.execute("""
                INSERT INTO setcode (account, timestamp, trx_id, first_seen, label, category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (d["account"], d["timestamp"], d["trx_id"],
                  d["first_seen"], d["label"], d["category"]))
            count += 1
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    return count

def get_latest_timestamp(conn):
    c = conn.cursor()
    result = c.execute("SELECT MAX(timestamp) FROM setcode").fetchone()
    return result[0] if result and result[0] else "2018-01-01T00:00:00Z"

def fetch_setcode_actions(after_iso):
    url = f"{HYPERION}/v2/history/get_actions"
    params = {
        "account": "eosio",
        "filter": "eosio:setcode",
        "sort": "asc",
        "after": after_iso,
        "limit": 100
    }
    print(f"🔍 Fetching setcode after {after_iso}")
    r = requests.get(url, params=params)
    return r.json().get("actions", [])

def sync_setcode():
    conn = init_db()

    # 🚀 Preload all known accounts once into memory
    c = conn.cursor()
    c.execute("SELECT DISTINCT account FROM setcode")
    known_accounts = set(row[0] for row in c.fetchall())

    cursor = get_latest_timestamp(conn)
    total_inserted = 0
    page = 0

    while True:
        page += 1
        print(f"📦 Page {page} | After: {cursor}")
        actions = fetch_setcode_actions(cursor)

        if not actions:
            print("✅ No new setcode actions. Sync complete.")
            break

        deployments = []
        for act in actions:
            acct = act["act"]["data"]["account"]
            timestamp = act["timestamp"]
            first = acct not in known_accounts
            if first:
                known_accounts.add(acct)

            meta = KNOWN_ACCOUNTS.get(acct, {})
            deployments.append({
                "account": acct,
                "timestamp": timestamp,
                "trx_id": act["trx_id"],
                "first_seen": 1 if first else 0,
                "label": meta.get("label"),
                "category": meta.get("category")
            })

        inserted = insert_setcodes(conn, deployments)
        total_inserted += inserted
        print(f"  ↳ Inserted {inserted} enriched deployment(s)")

        new_cursor = deployments[-1]["timestamp"]
        if new_cursor == cursor:
            print("⚠️ Cursor did not advance — stopping to avoid infinite loop.")
            break
        cursor = new_cursor

    conn.close()
    print(f"\n🎉 Sync complete. Total inserted: {total_inserted}")


# === PLOT BY CATEGORY ===
def plot_by_category():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT timestamp, category FROM setcode", conn)
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    df["category"] = df["category"].fillna("unknown")

    grouped = df.groupby(["date", "category"]).size().reset_index(name="count")
    pivot = grouped.pivot(index="date", columns="category", values="count").fillna(0)

    out_csv = os.path.join("data", "setcode_testnet_by_category.csv")
    out_png = os.path.join("exports", "setcode_testnet_by_category.png")
    pivot.to_csv(out_csv)

    plt.figure(figsize=(12, 6))
    pivot.plot.area(stacked=True, ax=plt.gca())
    plt.title("Testnet Contract Deployments by Category")
    plt.xlabel("Date")
    plt.ylabel("Deployments")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    print(f"📊 Saved grouped category chart to {out_png}")

# === MAIN ===
if __name__ == "__main__":
    print("🔄 Ultra Testnet Contract Tracker (Enriched)")
    sync_setcode()
    plot_by_category()
