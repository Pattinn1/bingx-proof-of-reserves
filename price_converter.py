#!/usr/bin/env python3
"""
Cryptocurrency Price Converter - EUR Values
Fetches current BNB and ETH prices and converts bridge amounts to EUR
"""

import requests
import json
from decimal import Decimal

class PriceConverter:
    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"
        self.prices = {}
        
    def fetch_prices(self):
        """Fetch current BNB and ETH prices in EUR"""
        try:
            params = {
                'ids': 'binancecoin,ethereum',
                'vs_currencies': 'eur,usd',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            self.prices = {
                'bnb': {
                    'eur': data['binancecoin']['eur'],
                    'usd': data['binancecoin']['usd'],
                    'change_24h': data['binancecoin'].get('eur_24h_change', 0)
                },
                'eth': {
                    'eur': data['ethereum']['eur'],
                    'usd': data['ethereum']['usd'],
                    'change_24h': data['ethereum'].get('eur_24h_change', 0)
                }
            }
            
            return True
            
        except Exception as e:
            print(f"❌ Error fetching prices: {e}")
            # Fallback prices (approximate)
            self.prices = {
                'bnb': {'eur': 650, 'usd': 700, 'change_24h': 0},
                'eth': {'eur': 3200, 'usd': 3500, 'change_24h': 0}
            }
            return False
    
    def get_bnb_price_eur(self):
        """Get BNB price in EUR"""
        return self.prices.get('bnb', {}).get('eur', 0)
    
    def get_eth_price_eur(self):
        """Get ETH price in EUR"""
        return self.prices.get('eth', {}).get('eur', 0)
    
    def bnb_to_eur(self, bnb_amount):
        """Convert BNB amount to EUR"""
        bnb_price = self.get_bnb_price_eur()
        return float(bnb_amount) * bnb_price
    
    def eth_to_eur(self, eth_amount):
        """Convert ETH amount to EUR"""
        eth_price = self.get_eth_price_eur()
        return float(eth_amount) * eth_price
    
    def display_prices(self):
        """Display current prices with 24h change"""
        print(f"\n💰 Current Cryptocurrency Prices")
        print(f"=" * 50)
        
        bnb_data = self.prices.get('bnb', {})
        eth_data = self.prices.get('eth', {})
        
        # BNB Price
        bnb_change = bnb_data.get('change_24h', 0)
        bnb_arrow = "📈" if bnb_change > 0 else "📉" if bnb_change < 0 else "➡️"
        print(f"🟡 BNB: €{bnb_data.get('eur', 0):.2f} | ${bnb_data.get('usd', 0):.2f}")
        print(f"   24h: {bnb_arrow} {bnb_change:+.2f}%")
        
        # ETH Price  
        eth_change = eth_data.get('change_24h', 0)
        eth_arrow = "📈" if eth_change > 0 else "📉" if eth_change < 0 else "➡️"
        print(f"🔵 ETH: €{eth_data.get('eur', 0):.2f} | ${eth_data.get('usd', 0):.2f}")
        print(f"   24h: {eth_arrow} {eth_change:+.2f}%")
    
    def calculate_bridge_value_eur(self, bnb_amount):
        """Calculate EUR values for bridge transaction"""
        # Bridge fees (from bnb_bridge.py)
        bridge_fee_percentage = 0.001  # 0.1%
        gas_fee_bnb = 0.005  # 0.005 BNB
        
        bridge_fee = bnb_amount * bridge_fee_percentage
        total_fee = bridge_fee + gas_fee_bnb
        net_amount = bnb_amount - total_fee
        
        # Convert to EUR
        input_eur = self.bnb_to_eur(bnb_amount)
        bridge_fee_eur = self.bnb_to_eur(bridge_fee)
        gas_fee_eur = self.bnb_to_eur(gas_fee_bnb)
        total_fee_eur = self.bnb_to_eur(total_fee)
        net_eur = self.eth_to_eur(net_amount)  # Output is ETH
        
        return {
            'input_bnb': bnb_amount,
            'input_eur': input_eur,
            'bridge_fee_bnb': bridge_fee,
            'bridge_fee_eur': bridge_fee_eur,
            'gas_fee_bnb': gas_fee_bnb,
            'gas_fee_eur': gas_fee_eur,
            'total_fee_bnb': total_fee,
            'total_fee_eur': total_fee_eur,
            'net_amount_eth': net_amount,
            'net_eur': net_eur
        }
    
    def display_bridge_calculation(self, bnb_amount):
        """Display detailed bridge calculation in EUR"""
        calc = self.calculate_bridge_value_eur(bnb_amount)
        
        print(f"\n🌉 Bridge Transaction Analysis (EUR Values)")
        print(f"=" * 60)
        print(f"🎯 Target: 0x47B63163b0ea6F0D8a186Db7CCb2E065F95aD79D")
        print(f"🔄 Direction: BSC (BNB) → Ethereum (ETH)")
        
        print(f"\n💎 Input Amount:")
        print(f"   {calc['input_bnb']:.6f} BNB = €{calc['input_eur']:.2f}")
        
        print(f"\n💸 Fees Breakdown:")
        print(f"   Bridge Fee (0.1%): {calc['bridge_fee_bnb']:.6f} BNB = €{calc['bridge_fee_eur']:.2f}")
        print(f"   Gas Fee: {calc['gas_fee_bnb']:.6f} BNB = €{calc['gas_fee_eur']:.2f}")
        print(f"   Total Fees: {calc['total_fee_bnb']:.6f} BNB = €{calc['total_fee_eur']:.2f}")
        
        print(f"\n🎁 Output Amount:")
        print(f"   {calc['net_amount_eth']:.6f} ETH = €{calc['net_eur']:.2f}")
        
        # Calculate fee percentage of total
        fee_percentage = (calc['total_fee_eur'] / calc['input_eur']) * 100
        print(f"\n📊 Summary:")
        print(f"   Fee Rate: {fee_percentage:.2f}% of transaction")
        print(f"   Value Transferred: €{calc['net_eur']:.2f}")
        print(f"   Cost: €{calc['total_fee_eur']:.2f}")

def main():
    print("\n" + "="*60)
    print("💱 BNB BRIDGE EUR VALUE CALCULATOR")
    print("="*60)
    
    converter = PriceConverter()
    
    print("\n🔄 Fetching current prices...")
    success = converter.fetch_prices()
    
    if success:
        print("✅ Prices fetched successfully")
    else:
        print("⚠️  Using fallback prices (may not be current)")
    
    # Display current prices
    converter.display_prices()
    
    # Example calculations for common amounts
    example_amounts = [0.01, 0.1, 0.5, 1.0, 5.0]
    
    print(f"\n📋 Bridge Value Examples:")
    print(f"=" * 60)
    
    for amount in example_amounts:
        print(f"\n{'─' * 40}")
        converter.display_bridge_calculation(amount)
    
    print(f"\n🔧 Usage:")
    print(f"To calculate custom amounts, modify the script or integrate with bridge_config.py")
    
    print(f"\n📈 Real-time Integration:")
    print(f"This converter can be imported into the bridge system for live EUR values")

if __name__ == "__main__":
    main()