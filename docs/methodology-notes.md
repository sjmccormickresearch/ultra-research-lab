# 🧪 Methodology Notes – Ultra Ecosystem Research

This document outlines the investigative steps and technical methods used to analyze the Ultra ($UOS) ecosystem, with a focus on real infrastructure activity, codebase exploration, and testnet dynamics.

---

## 1. Repository Cloning and Initial Recon

We began by cloning the core Ultra ecosystem repositories to a local working environment:

- [`ultra`](https://github.com/ultra-io/)
- [`vaulta`](https://github.com/VaultaHQ/)
- [`cloak`](https://github.com/mschoenebeck/zeos-caterpillar) – Zeos/Cloak privacy layer
- [`exsat`](https://github.com/ExSat-io/) – originally considered part of the stack, later discarded

This gave us direct access to smart contracts, protobuf definitions, infrastructure logic, and network configs.

---

## 2. Keyword + Structural Cross-Linking

We then performed:
- Grep-style recursive keyword searches (`AIRGRAB`, `POWER`, `RAM`, `eosio.token`, `bridge`, etc.)
- Analysis of inter-repo code overlaps, naming conventions, and module interdependence
- Discovery of shared architectural elements (e.g. use of `eosio` system contracts, transaction signing logic, staking mechanics)

This informed our view of vertical integration across Vaulta, Cloak, and Ultra.

---

## 3. Network Mapping (Crude but Directional)

We made informal maps of:
- Account interactions
- Token usage flows ($UOS, DUOS)
- Contract deployment chains
- Actor roles (e.g. oracle pushers, auction factories, quest initiators)

This clarified the difference between passive and active modules — and helped us distinguish real utility vs placeholder contracts.

---

### 4. Ultra Testnet Activity Scanner

We developed and refined a Python script to:

- Fetch the latest block from [`/v1/chain/get_info`](https://api.testnet.ultra.io/v1/chain/get_info)  
- Scan historical blocks using `/v1/chain/get_block`  
- Extract meaningful actions (e.g. `setcode`, `setabi`, `newaccount`, `pushrate`, `setevmblk.a`)  
- Track known accounts like `ultra.bridge`, `ultra.oracle`, `ultra.rng`, `ultra.unqstk`, and `ultra.val1`–`val3`  
- Log activity and write structured data to CSV

This revealed:

- **Consistent oracle updates** via `pushrate` from `ultra.oracle`  
- **Bridge-related anchoring** through `setevmblk.a` on `ultra.bridge`, validated by `ultra.val1`, `ultra.val2`, and `ultra.val3`  
- **RNG system tests** with `killjobs` and `setpubkey` from `ultra.rng`  
- **Staking or reward testing** from `ultra.unqstk` using `claimreward`  
- **Structured, timestamped action logs**, helping identify development surges and testnet readiness patterns


---

## 5. Infrastructure for Open Source Archiving

We created a `ultra-research` folder with the following structure:

ultra-research/
│
├── data/ ← CSVs from testnet scan
├── scripts/ ← Python tools (testnet scraper, analyzer, etc.)
├── docs/ ← Methodology, key takeaways, README



