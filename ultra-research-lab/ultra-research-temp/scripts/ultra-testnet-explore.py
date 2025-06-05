import requests
import csv
import time
import os
from datetime import datetime

## Explore Ultra's testnet — script set to scan March 2025 blocks

# === SETTINGS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FILE = os.path.join(BASE_DIR, "data", "ultra_testnet_log_march.csv")
BLOCKS_TO_SCAN = 10000  # Approx. 1 month

# === FILTERS ===
interesting_names = {"setcode", "setabi", "newaccount"}
watched_accounts = {
    "bridge.ultra", "dex.ultra", "rng.ultra", "aomempires", "vaulta", "cloakcore",
    "gamehub", "ugame", "ultrabridge", "ultragames", "eosio.oracle", "ultra.oracle"
}

# === API FUNCTIONS ===
def get_latest_block_num():
    r = requests.get("https://api.testnet.ultra.io/v1/chain/get_info")
    return r.json()["head_block_num"]

def get_block(block_num):
    r = requests.post("https://api.testnet.ultra.io/v1/chain/get_block", json={"block_num_or_id": block_num})
    if r.status_code != 200 or not r.content:
        raise ValueError("Empty or bad response")
    return r.json()

# === MAIN LOGIC ===
def scan_blocks(start_block, num_blocks):
    print("⏳ Fetching blocks starting from:", start_block)
    rows = []

    for b in range(start_block, start_block - num_blocks, -1):
        try:
            block = get_block(b)
            txs = block.get("transactions", [])
            if not txs:
                print(f"⚠️ Skipped block {b}: No transactions")
                continue

            action_count = 0
            for tx in txs:
                trx = tx.get("trx")
                if isinstance(trx, dict):
                    actions = trx.get("transaction", {}).get("actions", [])
                    for act in actions:
                        action_count += 1
                        name = act.get("name", "")
                        account = act.get("account", "")
                        auth = act.get("authorization", [])
                        actor = auth[0]["actor"] if auth else ""
                        tag = "known" if name in interesting_names or account in watched_accounts or actor in watched_accounts else "unknown"

                        rows.append({
                            "block_num": b,
                            "timestamp": block["timestamp"],
                            "action_name": name,
                            "account": account,
                            "actor": actor,
                            "multi_action": action_count > 1,
                            "tag": tag
                        })

            if action_count == 0:
                print(f"⚠️ Skipped block {b}: No actions")
        except Exception as e:
            print(f"⚠️ Skipped block {b}: {e}")

    return rows

# === CSV WRITING ===
def write_to_csv(rows, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["block_num", "timestamp", "action_name", "account", "actor", "multi_action", "tag"])
        if f.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)

# === RUN ===
if __name__ == "__main__":
    latest_block = get_latest_block_num()
    start_block = latest_block - (2 * BLOCKS_TO_SCAN)  # Jump back ~2 months (start of March)
    rows = scan_blocks(start_block, BLOCKS_TO_SCAN)

    print(f"📁 Writing to: {CSV_FILE}")
    write_to_csv(rows, CSV_FILE)

    print(f"\n✅ Logged {len(rows)} actions to {CSV_FILE}")
