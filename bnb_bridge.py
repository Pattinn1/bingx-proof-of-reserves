#!/usr/bin/env python3
"""
BNB to Ethereum Bridge Transaction Builder
Bridges BNB from Binance Smart Chain to Ethereum and funds specified address
"""

import json
import time
from web3 import Web3
from eth_account import Account
from decimal import Decimal
import requests

class BNBBridge:
    def __init__(self):
        # BSC Network Configuration
        self.bsc_rpc = "https://bsc-dataseed1.binance.org/"
        self.bsc_web3 = Web3(Web3.HTTPProvider(self.bsc_rpc))
        self.bsc_chain_id = 56
        
        # Ethereum Network Configuration  
        self.eth_rpc = "https://eth-mainnet.g.alchemy.com/v2/demo"  # Replace with your RPC
        self.eth_web3 = Web3(Web3.HTTPProvider(self.eth_rpc))
        self.eth_chain_id = 1
        
        # Target address to fund
        self.target_address = "0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D"
        
        # Bridge contract addresses (Binance Bridge)
        self.bsc_bridge_contract = "0x3ee18B2214AFF97000D974cf647E7C347E8fa585"  # BSC side
        self.eth_bridge_contract = "0x3ee18B2214AFF97000D974cf647E7C347E8fa585"  # ETH side
        
        # Alternative: Celer Bridge contracts
        self.celer_bsc_bridge = "0x841ce48F9446C8E281D3F1444cB859b4A6D0738C"
        self.celer_eth_bridge = "0x5427FEFA711Eff984124bFBB1AB6fbf5E3DA1820"
        
        print("🚀 BNB Bridge Initialized")
        print(f"📍 Target Address: {self.target_address}")
        print(f"🔗 BSC Connected: {self.bsc_web3.is_connected()}")
        print(f"🔗 ETH Connected: {self.eth_web3.is_connected()}")

    def check_balances(self, address):
        """Check BNB balance on BSC and ETH balance on Ethereum"""
        try:
            # BNB balance on BSC
            bnb_balance_wei = self.bsc_web3.eth.get_balance(address)
            bnb_balance = self.bsc_web3.from_wei(bnb_balance_wei, 'ether')
            
            # ETH balance on Ethereum  
            eth_balance_wei = self.eth_web3.eth.get_balance(address)
            eth_balance = self.eth_web3.from_wei(eth_balance_wei, 'ether')
            
            print(f"\n💰 Balance Check for {address}")
            print(f"🟡 BNB (BSC): {bnb_balance} BNB")
            print(f"🔵 ETH (Ethereum): {eth_balance} ETH")
            
            return {
                'bnb_balance': float(bnb_balance),
                'eth_balance': float(eth_balance),
                'address': address
            }
        except Exception as e:
            print(f"❌ Error checking balances: {e}")
            return None

    def estimate_bridge_fee(self, amount_bnb):
        """Estimate bridge fees for the transaction"""
        # Typical bridge fees (these are estimates)
        bridge_fee_percentage = 0.001  # 0.1%
        gas_fee_bnb = 0.005  # ~0.005 BNB for gas
        
        bridge_fee = amount_bnb * bridge_fee_percentage
        total_fee = bridge_fee + gas_fee_bnb
        
        print(f"\n💸 Bridge Fee Estimation")
        print(f"🔄 Bridge Fee ({bridge_fee_percentage*100}%): {bridge_fee:.6f} BNB")
        print(f"⛽ Gas Fee (estimated): {gas_fee_bnb:.6f} BNB")
        print(f"💰 Total Fees: {total_fee:.6f} BNB")
        print(f"📈 Amount after fees: {amount_bnb - total_fee:.6f} BNB → ETH")
        
        return {
            'bridge_fee': bridge_fee,
            'gas_fee': gas_fee_bnb,
            'total_fee': total_fee,
            'net_amount': amount_bnb - total_fee
        }

    def build_celer_bridge_tx(self, private_key, amount_bnb):
        """Build transaction using Celer Bridge (recommended for better rates)"""
        try:
            account = Account.from_key(private_key)
            sender_address = account.address
            
            print(f"\n🌉 Building Celer Bridge Transaction")
            print(f"📤 From: {sender_address} (BSC)")
            print(f"📥 To: {self.target_address} (Ethereum)")
            print(f"💎 Amount: {amount_bnb} BNB")
            
            # Convert amount to Wei
            amount_wei = self.bsc_web3.to_wei(amount_bnb, 'ether')
            
            # Celer Bridge ABI (simplified - you'd need the full ABI)
            celer_abi = [
                {
                    "inputs": [
                        {"name": "_receiver", "type": "address"},
                        {"name": "_amount", "type": "uint256"},
                        {"name": "_dstChainId", "type": "uint64"},
                        {"name": "_nonce", "type": "uint64"},
                        {"name": "_maxSlippage", "type": "uint32"}
                    ],
                    "name": "send",
                    "outputs": [],
                    "stateMutability": "payable",
                    "type": "function"
                }
            ]
            
            # Create contract instance
            contract = self.bsc_web3.eth.contract(
                address=self.celer_bsc_bridge,
                abi=celer_abi
            )
            
            # Get nonce
            nonce = self.bsc_web3.eth.get_transaction_count(sender_address)
            
            # Build transaction
            tx = contract.functions.send(
                self.target_address,  # receiver on Ethereum
                amount_wei,          # amount in wei
                1,                   # Ethereum chain ID
                int(time.time()),    # nonce
                3000                 # max slippage 0.3%
            ).build_transaction({
                'from': sender_address,
                'value': amount_wei,
                'gas': 300000,
                'gasPrice': self.bsc_web3.to_wei('5', 'gwei'),
                'nonce': nonce,
                'chainId': self.bsc_chain_id
            })
            
            print(f"✅ Transaction built successfully")
            print(f"⛽ Gas Limit: {tx['gas']}")
            print(f"💰 Gas Price: {self.bsc_web3.from_wei(tx['gasPrice'], 'gwei')} Gwei")
            
            return tx
            
        except Exception as e:
            print(f"❌ Error building Celer bridge transaction: {e}")
            return None

    def build_binance_bridge_tx(self, private_key, amount_bnb):
        """Build transaction using Binance official bridge"""
        try:
            account = Account.from_key(private_key)
            sender_address = account.address
            
            print(f"\n🌉 Building Binance Bridge Transaction")
            print(f"📤 From: {sender_address} (BSC)")
            print(f"📥 To: {self.target_address} (Ethereum)")
            print(f"💎 Amount: {amount_bnb} BNB")
            
            # Simple transfer to bridge contract (simplified approach)
            amount_wei = self.bsc_web3.to_wei(amount_bnb, 'ether')
            nonce = self.bsc_web3.eth.get_transaction_count(sender_address)
            
            tx = {
                'to': self.bsc_bridge_contract,
                'value': amount_wei,
                'gas': 21000,
                'gasPrice': self.bsc_web3.to_wei('5', 'gwei'),
                'nonce': nonce,
                'chainId': self.bsc_chain_id,
                'data': self.encode_bridge_data(self.target_address)
            }
            
            print(f"✅ Transaction built successfully")
            return tx
            
        except Exception as e:
            print(f"❌ Error building Binance bridge transaction: {e}")
            return None

    def encode_bridge_data(self, target_address):
        """Encode bridge data for cross-chain transfer"""
        # This would need to match the bridge contract's expected data format
        # Simplified version - actual implementation depends on bridge protocol
        from eth_abi import encode
        
        # Encode target address for Ethereum
        encoded_data = encode(['address'], [target_address])
        return '0x' + encoded_data.hex()

    def sign_and_send_transaction(self, tx, private_key, simulate_only=True):
        """Sign and send (or simulate) the transaction"""
        try:
            account = Account.from_key(private_key)
            
            # Sign transaction
            signed_tx = account.sign_transaction(tx)
            
            print(f"\n📝 Transaction signed by: {account.address}")
            print(f"🔐 Transaction hash: {signed_tx.hash.hex()}")
            
            if simulate_only:
                print(f"🧪 SIMULATION MODE - Transaction not sent")
                print(f"📋 Transaction details:")
                print(f"   To: {tx['to']}")
                print(f"   Value: {self.bsc_web3.from_wei(tx['value'], 'ether')} BNB")
                print(f"   Gas: {tx['gas']}")
                print(f"   Gas Price: {self.bsc_web3.from_wei(tx['gasPrice'], 'gwei')} Gwei")
                return signed_tx.hash.hex()
            else:
                # Send transaction
                tx_hash = self.bsc_web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"🚀 Transaction sent! Hash: {tx_hash.hex()}")
                
                # Wait for confirmation
                receipt = self.bsc_web3.eth.wait_for_transaction_receipt(tx_hash)
                print(f"✅ Transaction confirmed in block: {receipt.blockNumber}")
                
                return tx_hash.hex()
                
        except Exception as e:
            print(f"❌ Error signing/sending transaction: {e}")
            return None

    def monitor_bridge_status(self, tx_hash):
        """Monitor the bridge transaction status"""
        print(f"\n👀 Monitoring bridge status for tx: {tx_hash}")
        print(f"⏱️  Bridge typically takes 5-15 minutes")
        print(f"🔍 Check status at:")
        print(f"   - BSCScan: https://bscscan.com/tx/{tx_hash}")
        print(f"   - Celer Bridge: https://cbridge.celer.network/")
        
        # Check target address balance periodically
        initial_balance = self.check_balances(self.target_address)
        
        return initial_balance

def main():
    """Main function to demonstrate bridge usage"""
    bridge = BNBBridge()
    
    print("\n" + "="*60)
    print("🌉 BNB TO ETHEREUM BRIDGE TRANSACTION BUILDER")
    print("="*60)
    
    # Example usage (replace with actual values)
    example_private_key = "0x1234...your_private_key_here"  # NEVER commit real keys!
    amount_to_bridge = 0.1  # 0.1 BNB
    
    print(f"\n📋 Transaction Summary:")
    print(f"🎯 Target Address: {bridge.target_address}")
    print(f"💰 Amount to Bridge: {amount_to_bridge} BNB")
    print(f"🔄 Bridge Type: Celer Bridge (Recommended)")
    
    # Check current balances
    bridge.check_balances(bridge.target_address)
    
    # Estimate fees
    fees = bridge.estimate_bridge_fee(amount_to_bridge)
    
    # Build transaction (choose one method)
    print(f"\n🔧 Choose bridge method:")
    print(f"1. Celer Bridge (Recommended - lower fees)")
    print(f"2. Binance Bridge (Official)")
    
    # For demonstration, we'll use Celer Bridge
    bridge_method = "celer"
    
    if bridge_method == "celer":
        tx = bridge.build_celer_bridge_tx(example_private_key, amount_to_bridge)
    else:
        tx = bridge.build_binance_bridge_tx(example_private_key, amount_to_bridge)
    
    if tx:
        # Sign and simulate transaction
        tx_hash = bridge.sign_and_send_transaction(tx, example_private_key, simulate_only=True)
        
        if tx_hash:
            print(f"\n✅ Bridge transaction prepared successfully!")
            print(f"🔐 Transaction Hash: {tx_hash}")
            
            # Monitor status
            bridge.monitor_bridge_status(tx_hash)
            
            print(f"\n⚠️  IMPORTANT NOTES:")
            print(f"1. Replace 'example_private_key' with your actual private key")
            print(f"2. Set simulate_only=False to execute the transaction")
            print(f"3. Ensure sufficient BNB balance for amount + fees")
            print(f"4. Bridge may take 5-15 minutes to complete")
            print(f"5. Check target address balance on Ethereum after completion")

if __name__ == "__main__":
    main()