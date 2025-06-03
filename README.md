# 🧪 Ultra Testnet Research Toolkit
> A lightweight, script-based framework for tracking smart contract activity and ecosystem development on Ultra’s testnet.

This project tracks real on-chain activity and code-level infrastructure across the Ultra ($UOS) testnet. Our goal is to evaluate **developer momentum**, **contract deployment**, and **ecosystem readiness** by combining live testnet analysis with deep repo exploration.

---

## 🔍 What This Includes

- `ultra-testnet-explore.py`: Scans recent blocks from Ultra's testnet and logs meaningful smart contract actions to CSV (e.g. `setcode`, `pushrate`, `newaccount`).

- Additional tools:
  - Keyword mapping across Ultra, Vaulta, and Cloak repos (e.g. AIRGRAB, RAM, bridge)
  - Crude network mapping (accounts, actors, token flow)
  - Contract-to-repo linking and architecture clues (e.g. RAM/POWER enforcement, bridge logic)
  - Repo cloning for reproducible offline analysis

---

## 📁 Folder Structure

```bash
ultra-research/
├── data/        # CSV logs of contract activity, key account usage
├── scripts/     # Python tools for scanning, parsing, and analyzing
├── docs/        # Methodology, system notes, and research insights
└── notebooks/   # (Optional) For Jupyter or Colab-based exploration
```
--- 

## 🔧 Setup & Usage

```bash
# Clone this repo
cd ultra-research

# Run testnet activity scanner
python scripts/ultra-testnet-explore.py
```
The scanner will connect to https://api.testnet.ultra.io, loop through recent blocks, extract action traces, and save a CSV summary in data/.


## 🧠 Repo Exploration
This research also explores key open-source repositories powering the Ultra ecosystem:

- [ultra](https://github.com/ultra-io)
- [vaulta](https://github.com/VaultaHQ)
- [cloak](https://github.com/mschoenebeck/zeos-caterpillar) – Zeos/Cloak privacy layer
- [exsat](https://github.com/ExSat-io) – *explored, but later discarded*


We used recursive keyword searches (`AIRGRAB`, `bridge`, `RAM`, etc.) and architectural mapping to surface integration points and testnet activation signals.
