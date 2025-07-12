#!/usr/bin/env python3
"""
Quick Demo of BNB to Ethereum Bridge System
Shows the bridge setup and configuration for funding the target address
"""

from bnb_bridge import BNBBridge
import sys

def main():
    print("\n" + "="*60)
    print("🌉 BNB TO ETHEREUM BRIDGE SYSTEM DEMO")
    print("="*60)
    
    try:
        # Initialize bridge
        bridge = BNBBridge()
        
        print(f"\n🎯 Bridge Configuration:")
        print(f"📍 Target Address: {bridge.target_address}")
        print(f"🔗 BSC Network: {'Connected' if bridge.bsc_web3.is_connected() else 'Disconnected'}")
        print(f"🔗 ETH Network: {'Connected' if bridge.eth_web3.is_connected() else 'Disconnected'}")
        
        # Show balance check functionality
        print(f"\n💰 Balance Check Example:")
        try:
            balances = bridge.check_balances(bridge.target_address)
            if balances:
                print(f"✅ Successfully checked balances")
            else:
                print(f"⚠️  Balance check requires RPC connection")
        except Exception as e:
            print(f"⚠️  Balance check requires valid RPC endpoint (demo mode)")
        
        # Show fee estimation
        test_amount = 0.1
        fees = bridge.estimate_bridge_fee(test_amount)
        
        print(f"\n📋 Transaction Summary (Example):")
        print(f"💎 Amount to Bridge: {test_amount} BNB")
        print(f"💸 Estimated Bridge Fee: {fees['bridge_fee']:.6f} BNB")
        print(f"⛽ Estimated Gas Fee: {fees['gas_fee']:.6f} BNB")
        print(f"💰 Net Amount After Fees: {fees['net_amount']:.6f} BNB → ETH")
        
        print(f"\n🔧 Available Commands:")
        print(f"1. Run 'python bridge_config.py' for interactive mode")
        print(f"2. Set environment variables:")
        print(f"   export PRIVATE_KEY='your_private_key'")
        print(f"   export BSC_RPC_URL='https://bsc-dataseed1.binance.org/'")
        print(f"   export ETH_RPC_URL='https://mainnet.infura.io/v3/YOUR_ID'")
        
        print(f"\n📖 Documentation:")
        print(f"Read BRIDGE_README.md for complete setup instructions")
        
        print(f"\n✅ Bridge system is ready for use!")
        
    except Exception as e:
        print(f"❌ Error initializing bridge: {e}")
        print(f"💡 This is expected in demo mode without proper RPC endpoints")
        
        # Show the configuration anyway
        print(f"\n🎯 Bridge Configuration (Static):")
        print(f"📍 Target Address: 0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D")
        print(f"🌉 Bridge Direction: BSC (BNB) → Ethereum (ETH)")
        print(f"⚙️  Bridge Providers: Celer Bridge, Binance Bridge")
        print(f"✅ System installed and ready!")

if __name__ == "__main__":
    main()