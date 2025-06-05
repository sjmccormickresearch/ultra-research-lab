# 🧠 Ultra Ecosystem Codebase Links

Ultra
├── Uses Vaulta
│   ├── For fiat ramps, RAM vaults, KYC/AML
│   └── Shared contract naming conventions (VaultManager, deposit logic)
├── Uses Cloak
│   ├── Optional privacy: zkProofs, ShieldedBalance, token_shielded_transfer
│   └── Likely via modular smart contracts with shield enable/disable logic
└── Uses ExSat
    ├── For bridging: exsat_bridge, wrappedToken, bridge_evm_assets
    └── Integrates Ultra identity and token formats in bridging logic

Cloak
├── Implements privacy layer for Ultra tokens (UOS)
└── Likely interoperable with Vaulta for shielded vault balances

Vaulta
├── Compliance/KYC onboarding, fiat handling
├── Provides vaults for UOS-based contracts
└── Shared logic with ExSat (VaultManager, KYCRegistry)

ExSat
├── EVM asset bridging to/from Ultra
├── Knows about Ultra identities, UOS tokens
└── May plug into Vaulta for regulated ramp features
