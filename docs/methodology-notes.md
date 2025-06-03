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

## 4. Ultra Testnet Activity Scanner

We developed and refined a Python script to:
- Fetch the latest block from `https://api.testnet.ultra.io/v1/chain/get_info`
- Scan historical blocks via `/v1/chain/get_block`
- Extract meaningful actions (e.g. `setcode`, `setabi`, `newaccount`, `pushrate`)
- Track known accounts like `bridge.ultra`, `rng.ultra`, `vaulta`, `cloakcore`, etc.
- Log activity and save top contracts to CSV

This revealed:
- High-frequency data feeds from `eosio.oracle`
- Signs of Bridge, RNG, Vaulta, and GameHub testing
- Spikes in contract deployments and updates, suggesting pre-mainnet readiness

---

## 5. Infrastructure for Open Source Archiving

We created a `ultra-research` folder with the following structure:

ultra-research/
│
├── data/ ← CSVs from testnet scan
├── scripts/ ← Python tools (testnet scraper, analyzer, etc.)
├── docs/ ← Methodology, key takeaways, README



