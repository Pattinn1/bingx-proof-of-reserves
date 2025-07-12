#!/usr/bin/env python3
"""
Bridge Configuration and Execution Script
Execute BNB to Ethereum bridge transaction for funding specific address
"""

import os
from bnb_bridge import BNBBridge

def setup_environment():
    """Setup environment variables and check configuration"""
    print("🔧 Setting up bridge environment...")
    
    # Check for required environment variables
    required_vars = ['PRIVATE_KEY', 'BSC_RPC_URL', 'ETH_RPC_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("\n📝 Please set the following environment variables:")
        print("export PRIVATE_KEY='your_private_key_here'")
        print("export BSC_RPC_URL='https://bsc-dataseed1.binance.org/'")
        print("export ETH_RPC_URL='https://mainnet.infura.io/v3/YOUR_PROJECT_ID'")
        return False
    
    return True

def execute_bridge_transaction():
    """Execute the bridge transaction"""
    
    if not setup_environment():
        return
    
    # Initialize bridge
    bridge = BNBBridge()
    
    # Configuration
    target_address = "0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D"
    amount_to_bridge = float(input("💰 Enter amount of BNB to bridge: ") or "0.1")
    
    print(f"\n🎯 Bridge Configuration:")
    print(f"📍 Target Address: {target_address}")
    print(f"💎 Amount: {amount_to_bridge} BNB")
    print(f"🌉 Bridge: BSC → Ethereum")
    
    # Get private key from environment
    private_key = os.getenv('PRIVATE_KEY')
    
    if not private_key or private_key == 'your_private_key_here':
        print("❌ Please set a valid PRIVATE_KEY environment variable")
        return
    
    # Check current balances
    print("\n💰 Checking current balances...")
    bridge.check_balances(target_address)
    
    # Estimate fees
    fees = bridge.estimate_bridge_fee(amount_to_bridge)
    
    # Confirm transaction
    print(f"\n⚠️  TRANSACTION CONFIRMATION")
    print(f"Amount to bridge: {amount_to_bridge} BNB")
    print(f"Estimated fees: {fees['total_fee']:.6f} BNB")
    print(f"Net amount after fees: {fees['net_amount']:.6f} BNB")
    print(f"Target address: {target_address}")
    
    confirm = input("\nDo you want to proceed? (yes/no): ").lower()
    
    if confirm != 'yes':
        print("❌ Transaction cancelled")
        return
    
    # Choose bridge method
    print(f"\n🌉 Available bridge methods:")
    print(f"1. Celer Bridge (Recommended - lower fees, faster)")
    print(f"2. Binance Bridge (Official, slower)")
    
    bridge_choice = input("Choose bridge method (1 or 2): ") or "1"
    
    # Build transaction
    if bridge_choice == "1":
        print("\n🚀 Using Celer Bridge...")
        tx = bridge.build_celer_bridge_tx(private_key, amount_to_bridge)
    else:
        print("\n🚀 Using Binance Bridge...")
        tx = bridge.build_binance_bridge_tx(private_key, amount_to_bridge)
    
    if not tx:
        print("❌ Failed to build transaction")
        return
    
    # Final confirmation for execution
    simulate_mode = input("\nExecute in simulation mode? (yes/no): ").lower() == 'yes'
    
    # Execute transaction
    tx_hash = bridge.sign_and_send_transaction(tx, private_key, simulate_only=simulate_mode)
    
    if tx_hash:
        print(f"\n✅ Transaction executed successfully!")
        
        if not simulate_mode:
            print(f"🔗 Transaction Hash: {tx_hash}")
            print(f"🔍 Track on BSCScan: https://bscscan.com/tx/{tx_hash}")
            
            # Monitor bridge status
            bridge.monitor_bridge_status(tx_hash)
            
            print(f"\n📧 Next steps:")
            print(f"1. Wait 5-15 minutes for bridge completion")
            print(f"2. Check ETH balance at {target_address}")
            print(f"3. Monitor bridge status on Celer or Binance Bridge")
        else:
            print(f"🧪 Simulation completed - no funds transferred")

def check_target_balance():
    """Check the current balance of the target address"""
    bridge = BNBBridge()
    target_address = "0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D"
    
    print(f"🔍 Checking balance for target address...")
    bridge.check_balances(target_address)

def main():
    """Main menu"""
    print("\n" + "="*60)
    print("🌉 BNB TO ETHEREUM BRIDGE EXECUTOR")
    print("="*60)
    
    print(f"\n🎯 Target Address: 0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D")
    print(f"🔄 Bridge Direction: BSC (BNB) → Ethereum (ETH)")
    
    print(f"\n📋 Menu:")
    print(f"1. Execute bridge transaction")
    print(f"2. Check target address balance")
    print(f"3. Exit")
    
    choice = input("\nSelect option (1-3): ") or "1"
    
    if choice == "1":
        execute_bridge_transaction()
    elif choice == "2":
        check_target_balance()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()