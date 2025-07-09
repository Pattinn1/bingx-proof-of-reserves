# 🌉 BNB to Ethereum Bridge Transaction Builder

Bridge BNB from Binance Smart Chain to Ethereum and fund the target address `0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D`.

## 🎯 Overview

This tool allows you to:
- Bridge BNB from BSC to ETH on Ethereum mainnet
- Fund a specific target address automatically
- Choose between multiple bridge providers (Celer, Binance)
- Estimate fees and monitor transaction status
- Execute transactions safely with simulation mode

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export PRIVATE_KEY="your_wallet_private_key_here"
export BSC_RPC_URL="https://bsc-dataseed1.binance.org/"
export ETH_RPC_URL="https://mainnet.infura.io/v3/YOUR_PROJECT_ID"
```

### 3. Run the Bridge

```bash
python bridge_config.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PRIVATE_KEY` | Private key of your wallet (with BNB) | `0x1234...` |
| `BSC_RPC_URL` | BSC RPC endpoint | `https://bsc-dataseed1.binance.org/` |
| `ETH_RPC_URL` | Ethereum RPC endpoint | `https://mainnet.infura.io/v3/YOUR_ID` |

### Target Address

The bridge is pre-configured to fund: `0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D`

## 🌉 Bridge Options

### 1. Celer Bridge (Recommended)
- ✅ Lower fees (~0.1%)
- ✅ Faster execution (5-10 minutes)
- ✅ Better liquidity
- 🔗 [Celer Bridge](https://cbridge.celer.network/)

### 2. Binance Bridge (Official)
- ✅ Official Binance solution
- ⚠️ Higher fees
- ⚠️ Slower execution (10-15 minutes)
- 🔗 [Binance Bridge](https://www.binance.org/bridge)

## 💰 Fee Structure

### Estimated Fees (Celer Bridge)
- **Bridge Fee**: ~0.1% of amount
- **Gas Fee**: ~0.005 BNB
- **Total**: ~0.1% + 0.005 BNB

### Example for 1 BNB
- Amount: 1.0 BNB
- Bridge Fee: 0.001 BNB
- Gas Fee: 0.005 BNB
- **Net Amount**: 0.994 BNB → ETH

## 🛡️ Security Features

### Simulation Mode
- Test transactions without spending funds
- Verify all parameters before execution
- Safe for testing and validation

### Environment Variables
- Private keys stored securely as environment variables
- No hardcoded sensitive data
- Easy to rotate keys

### Transaction Verification
- Pre-flight balance checks
- Fee estimation
- User confirmation required
- Transaction hash tracking

## 📋 Usage Examples

### Basic Bridge Transaction

```bash
# Set environment variables
export PRIVATE_KEY="your_private_key"
export BSC_RPC_URL="https://bsc-dataseed1.binance.org/"
export ETH_RPC_URL="https://mainnet.infura.io/v3/YOUR_PROJECT_ID"

# Run bridge
python bridge_config.py

# Follow prompts:
# 1. Enter amount to bridge (e.g., 0.1)
# 2. Choose bridge method (1 for Celer)
# 3. Confirm transaction details
# 4. Choose execution mode (simulation/live)
```

### Check Target Balance Only

```python
from bnb_bridge import BNBBridge

bridge = BNBBridge()
bridge.check_balances("0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D")
```

### Direct Transaction Building

```python
from bnb_bridge import BNBBridge

bridge = BNBBridge()
tx = bridge.build_celer_bridge_tx(private_key, 0.1)  # 0.1 BNB
tx_hash = bridge.sign_and_send_transaction(tx, private_key, simulate_only=True)
```

## 🔍 Monitoring

### Transaction Tracking

After executing a bridge transaction, monitor status at:

- **BSCScan**: `https://bscscan.com/tx/{transaction_hash}`
- **Celer Bridge**: `https://cbridge.celer.network/`
- **Etherscan**: `https://etherscan.io/address/0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D`

### Status Timeline

1. **Transaction Submitted** (Immediate)
   - Transaction appears on BSCScan
   - Shows as pending

2. **Bridge Processing** (5-15 minutes)
   - Cross-chain validation
   - Liquidity confirmation

3. **Completion** (Final)
   - ETH appears in target address
   - Visible on Etherscan

## ⚠️ Important Notes

### Security
- **Never share your private key**
- Use environment variables for sensitive data
- Test with small amounts first
- Always use simulation mode for testing

### Requirements
- Sufficient BNB balance for amount + fees
- Valid BSC and Ethereum RPC endpoints
- Wallet private key with BNB

### Limitations
- Minimum bridge amount: ~0.01 BNB
- Maximum bridge amount: Depends on bridge liquidity
- Bridge completion time: 5-15 minutes
- Cross-chain transaction irreversible

## 🆘 Troubleshooting

### Common Issues

#### "Insufficient balance"
- Check BNB balance in your wallet
- Ensure balance covers amount + fees

#### "RPC connection failed"
- Verify RPC URLs are correct
- Check internet connection
- Try alternative RPC endpoints

#### "Bridge transaction pending"
- Normal for cross-chain transactions
- Wait 15-20 minutes before investigating
- Check bridge status on official sites

#### "Transaction reverted"
- Insufficient gas limit
- Bridge contract issues
- Try again with higher gas

### Getting Help

1. Check transaction on BSCScan/Etherscan
2. Verify bridge status on Celer/Binance Bridge
3. Ensure all environment variables are set
4. Test in simulation mode first

## 🔗 Useful Links

- [BSCScan](https://bscscan.com/)
- [Etherscan](https://etherscan.io/)
- [Celer Bridge](https://cbridge.celer.network/)
- [Binance Bridge](https://www.binance.org/bridge)
- [BSC RPC Endpoints](https://docs.binance.org/smart-chain/developer/rpc.html)
- [Ethereum RPC Providers](https://ethereumnodes.com/)

## 📄 License

This tool is provided as-is for educational purposes. Use at your own risk.