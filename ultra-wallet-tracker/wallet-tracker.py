import requests, sqlite3, csv, os
from datetime import datetime, timedelta

DB_FILE = "wallets.db"
EXPORT_DIR = "daily_exports"
HYPERION = "https://ultra.eosusa.io"

os.makedirs(EXPORT_DIR, exist_ok=True)

def fetch_new_accounts(after_iso):
    url = f"{HYPERION}/v2/history/get_actions"
    params = {
        "account": "eosio",
        "filter": "eosio:newaccount",
        "sort": "desc",
        "after": after_iso,
        "limit": 100
    }
    print(f"🔗 Querying: {url} (after: {after_iso})")
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

def insert_new_wallets(conn, wallets):
    c = conn.cursor()
    new_wallets = []
    for w in wallets:
        try:
            c.execute("INSERT INTO wallets VALUES (?, ?, ?, ?)",
                      (w["name"], w["timestamp"], w["creator"], w["trx_id"]))
            new_wallets.append(w)
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    return new_wallets

def export_to_csv(wallets):
    if not wallets:
        return
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    filename = os.path.join(EXPORT_DIR, f"wallets_{date_str}.csv")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "name", "creator", "trx_id"])
        for w in wallets:
            writer.writerow([w["timestamp"], w["name"], w["creator"], w["trx_id"]])
    print(f"📁 Exported {len(wallets)} wallets to {filename}")

# === MAIN ===
if __name__ == "__main__":
    print("🔍 Ultra Wallet Tracker started.")
    after_time = datetime.utcnow() - timedelta(days=1)
    after_iso = after_time.isoformat()

    conn = init_db()
    new_wallets = fetch_new_accounts(after_iso)
    saved = insert_new_wallets(conn, new_wallets)
    export_to_csv(saved)

    if saved:
        print(f"✅ Stored {len(saved)} new wallet(s).")
        for w in saved:
            print(f"🆕 {w['name']} | created by {w['creator']} at {w['timestamp']}")
    else:
        print("ℹ️ No new wallets found.")
