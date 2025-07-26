import sqlite3, pandas as pd, os
import matplotlib.pyplot as plt

def export_first_time_contracts(network="testnet"):
    assert network in ["testnet", "mainnet"], "Invalid network"

    DB_FILE = f"data/setcode_{network}.db"
    EXPORT_DIR = f"exports/first_time_{network}"
    os.makedirs(EXPORT_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(
        "SELECT account, timestamp, label, category FROM setcode WHERE first_seen = 1",
        conn
    )
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    df = df.sort_values("date")

    # CSV Export
    csv_path = f"data/first_time_contracts_{network}.csv"
    df.to_csv(csv_path, index=False)

    # Plotting
    count_by_day = df.groupby("date").size()
    plt.figure(figsize=(10, 5))
    count_by_day.plot(marker="o")
    plt.title(f"First-Time Contract Deployments on Ultra {network.capitalize()}")
    plt.xlabel("Date")
    plt.ylabel("New Projects / Accounts")
    plt.tight_layout()
    out_png = f"{EXPORT_DIR}/first_time_contracts_{network}.png"
    plt.savefig(out_png)
    plt.close()

    print(f"📁 Exported {len(df)} first-time deployments to {csv_path}")
    print(f"📊 Saved chart to {out_png}")

# === MAIN ===
if __name__ == "__main__":
    export_first_time_contracts("testnet")
    export_first_time_contracts("mainnet")
