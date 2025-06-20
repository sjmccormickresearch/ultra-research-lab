# 🧪 Ultra Research Toolkit
> A lightweight, script-based framework for tracking smart contract activity and analyzing ecosystem development across Ultra’s **testnet** and **public code repositories**.

This toolkit captures real on-chain activity from Ultra’s ($UOS) testnet alongside code-level signals from its open-source infrastructure. The goal is to evaluate **developer momentum**, **contract deployment patterns**, and **ecosystem readiness** by combining live testnet block analysis with deep repo exploration.

---

## 🔍 What This Includes

- `ultra-testnet-explore.py`: Scans recent blocks from Ultra's testnet and logs meaningful smart contract actions to CSV (e.g. `setcode`, `pushrate`, `newaccount`).

- Additional tools:
  - Keyword mapping across Ultra, Vaulta, and Cloak repos (e.g. AIRGRAB, RAM, bridge)
  - Crude network mapping (accounts, actors, token flow)
  - Contract-to-repo linking and architecture clues (e.g. RAM/POWER enforcement, bridge logic)
  - Repo cloning for reproducible offline analysis
  - Transcription tool for MP3/MP4 files - ideal for dev calls, AMAs, or ecosystem updates

---

## 📁 Folder Structure

```bash
ultra-research/
├── data/      # CSV logs of contract activity and key account usage
├── scripts/   # Python tools for scanning and parsing testnet + repo data
└── docs/      # Notes, maps, and research insights
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
