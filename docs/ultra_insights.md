
# Ultra Infrastructure & Economic Insights

Ultra ($UOS) is building a vertically integrated Web3 gaming stack, comprising its own Layer 1 chain, developer tools, NFT standards, staking systems, and a native DEX with privacy features. This document summarizes technical, architectural, and token-economic insights drawn from source code, smart contracts, and audit reports across Ultra, Vaulta, Cloak, and related repos.

---

## 🔗 Chain Setup & Control

Ultra is built on an EOSIO-based blockchain. The chain's core settings are defined in `genesis.json`, including:

- `initial_key`: Controls initial block producer and contract permissions
- `ultra_veto_enabled`: Indicates governance veto power
- `max_block_cpu_usage`, `free_cpu_basis_point`: Sets computational limits and free access rates
- Configures fee-free thresholds and block size

This confirms that Ultra retains **protocol-level control** and can shape bandwidth and transaction costs.

---

## 🔐 Native Staking & POWER Generation

Ultra’s staking system, implemented on the EOSIO chain, issues **POWER**, a resource that governs transaction bandwidth and prioritization.

Although full native staking source files are pending, indirect evidence shows:
- POWER is generated via $UOS staking
- Bandwidth on Ultra is enforced and abstracted via this mechanism
- Refundable vaults (e.g., for NFT RAM) and staking logic suggest deep vertical integration

---

## 🏗 Developer Tooling

Ultra provides its own VSCode extension (`ultra-cpp`) to scaffold and deploy smart contracts, featuring:

- One-click contract creation and compilation
- Wallet management (create, unlock, add keys)
- Transaction and deployment helpers

This demonstrates strong focus on **developer UX and adoption**.

---

## 🌉 EOS ↔ EVM Trustless Bridge

Ultra runs its own **dual-layer bridge** architecture:

- EOSIO (Antelope) contract: Governs token mint/burn
- EVM-side ERC20 contracts: Manage bridged tokens
- `bridgeMsgV0` format supports atomic, structured message passing
- On-chain validation with no custodians = **trustless & secure**

This enables seamless integration with Ethereum-based assets, without relying on 3rd-party bridges.

---

## 💸 EVM-Side LP Staking: `Unipool`

Ultra rewards liquidity providers for the ETH/UOS Uniswap pair using a customized and audited `Unipool` contract.

### Contract Highlights:
- Users stake LP tokens to earn $UOS
- Rewards distributed linearly over 30-day `DURATION`
- Emissions controlled via `notifyRewardAmount()` (central authority)
- Public functions like `earned()`, `rewardRate`, and `totalSupply` provide transparency

### Sigma Prime Audit:
- Identified and resolved 7 issues (1 Critical, 2 High)
- Covered front-running, staking order, reward overflows
- Tools used: Mythril, Slither, Surya, Rattle
- Audit confirms production readiness

---

## 🧪 Staking Logic Test Coverage

The `Unipool.js` test file simulates:
- Equal and staggered staking
- Early exits
- Mid-cycle reward updates

Confirms:
- Rewards are proportionate to stake × time
- The contract gracefully handles updates and edge cases

---

## 🌐 `liquidity.ultra.io`: Frontend Portal

- React-based frontend for staking ETH/UOS LP tokens
- Uses `@uniswap/sdk`, `ethers.js`, `use-wallet`
- Deployable to Rinkeby or Mainnet
- Interfaces with `Unipool` and shows reward balances

**Note**: This is **not a DEX**. It’s a rewards UI.

---

## 🕵️ Cloak: Ultra’s Native DEX

Cloak is poised to become **Ultra’s internal DEX and privacy layer**, featuring:

- ZK circuits for `mint`, `burn`, `transfer`, `spend`
- Shielded balances and optional privacy
- Built natively for EOSIO (via `eosio.rs`)
- Composable assets and Ultra integration hooks

Cloak is designed for:
- In-game trading
- Private swaps
- Composable smart assets
- Fully on-chain, EOSIO-native execution

---

## 🧬 Dual-Layer DEX Strategy

| Layer                  | Stack         | Purpose                         |
|------------------------|---------------|----------------------------------|
| **Unipool + Uniswap** | EVM + Uniswap | Bootstraps ETH-side liquidity    |
| **Cloak**             | EOSIO + ZK    | Ultra’s native DEX for games     |

Unipool is a **temporary external incentive tool**, while Cloak is Ultra’s **long-term sovereign DEX**.

---



### Key Findings:
- `ultraproscan`, `uniultra.xyz`, and similar domains belong to **U2U**, not Ultra.io


---

## ✅ Conclusion

Ultra's infrastructure is mature, modular, and deeply integrated:

- ⚙️ Runs its own L1 chain + dev environment
- 🛠 Offers custom dev tools and smart contract scaffolding
- 💸 Incentivizes external liquidity via Unipool (audited)
- 🔐 Building an internal, private, composable DEX via Cloak
- 🌉 Connects seamlessly to Ethereum via a trustless EOS ↔ EVM bridge

This positions Ultra as not just a gaming platform, but a **full-stack digital economy**, with enforced token sinks, liquidity control, and developer-friendly tools.
