# Change wallet_name to the name of your wallet you made, make sure RPC creds have been set already

import os
import sys
from bitcoinlib.wallets import Wallet
from bitcoinlib.transactions import Transaction, Output
from bitcoinlib.services.bitcoind import BitcoindClient

# Configuration for your Bitcoin node RPC using environment variables
rpc_user = os.getenv('BITCOIN_RPC_USER')
rpc_password = os.getenv('BITCOIN_RPC_PASSWORD')
rpc_host = os.getenv('BITCOIN_RPC_HOST')
rpc_port = os.getenv('BITCOIN_RPC_PORT')

# The only thing that needs to be updated is TestWallet below to your wallet name
wallet_name = 'TestWallet'

# Attempt to create a BitcoindClient instance (assuming you have set environment variables)
try:
   client = BitcoindClient()
except Exception as e:
   print(f"Error connecting to Bitcoin node: {e}")
   sys.exit(1)

try:
    wallet = Wallet(wallet_name)
    wallet.scan()
    print("Wallet Information:")
    print("================================================")

    # Update UTXOs for the wallet
    wallet.utxos_update()

    # Check if there are UTXOs available
    utxos = wallet.utxos()

    # Get wallet information
    wallet_info = wallet.info()

    # Print each piece of information with error handling
except Exception as e:
    print(f"Error loading wallet '{wallet_name}': {e}")
    sys.exit(1)