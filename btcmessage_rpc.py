# export BITCOIN_NODE_HOST='your_node_ip'
# export BITCOIN_NODE_PORT='your_node_port'
# export BITCOIN_RPC_USERNAME='your_rpc_username'
# export BITCOIN_RPC_PASSWORD='your_rpc_password'
# export MY_BTC_PRIVATE_KEY='your_private_key_here'

# add the above first in your terminal or add to .bashrc, only change whats in Configuration block


import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from bitcoinlib.wallets import Wallet
from bitcoinlib.transactions import Output
from bitcoinlib.encoding import varstr

# Configuration  to figure out fee amount see  https://coinmarketcap.com/converter/
private_key = os.getenv('MY_BTC_PRIVATE_KEY')
wallet_name = 'YOUR_WALLETS_NAME'
sender_address = 'YOUR_BTC_ADDRESS'
recipient_address = 'BTC_ADDRESS_YOUR_SENDING_TO'
amount_to_send_satoshis = int(0.0001 * 100000000)
fee_satoshis = int(0.00014 * 100000000)
message = 'YOUR_MESSAGE'

# RPC configuration
rpc_user = os.getenv('BITCOIN_RPC_USERNAME')
rpc_password = os.getenv('BITCOIN_RPC_PASSWORD')
rpc_url = f"http://{os.getenv('BITCOIN_NODE_HOST')}:{os.getenv('BITCOIN_NODE_PORT')}"

# Load the existing wallet and update UTXOs
try:
    wallet = Wallet(wallet_name)
    wallet.utxos_update()
    utxos = wallet.utxos()
    if not utxos:
        print("No unspent transaction outputs available.")
        sys.exit(1)
except Exception as e:
    print(f"Error loading wallet or updating UTXOs: {e}")
    sys.exit(1)

# Prepare inputs and outputs for the transaction
try:
    inputs = [{'txid': utxo['txid'], 'output_n': utxo['output_n'], 'value': utxo['value']} for utxo in utxos]
    print("Inputs prepared for the transaction:", inputs)

    standard_output = Output(amount_to_send_satoshis, address=recipient_address)
    lock_script = b'j' + varstr(message.encode('utf-8'))
    op_return_output = Output(0, lock_script=lock_script)
    outputs = [standard_output, op_return_output]
    print("Outputs prepared for the transaction:", outputs)

except Exception as e:
    print(f"Error preparing inputs or outputs: {e}")
    sys.exit(1)

# Create and sign the transaction
try:
    tx = wallet.send(outputs, fee=fee_satoshis)
    print("\nTransaction created.")
    print(f"TXID: {tx.txid}\n")
    raw_tx_hex = tx.raw_hex()
    print(f"Raw Transaction Hex: {raw_tx_hex}")

    # Broadcast the transaction via RPC
    headers = {'content-type': 'application/json'}
    payload = {
        "method": "sendrawtransaction",
        "params": [raw_tx_hex],
        "jsonrpc": "2.0",
        "id": 0,
    }

    response = requests.post(rpc_url, json=payload, headers=headers, auth=HTTPBasicAuth(rpc_user, rpc_password))
    response_json = response.json()

    if 'error' in response_json and response_json['error']:
        print("Error broadcasting transaction:", response_json['error'])
    else:
        txid = response_json['result']
        print("Transaction broadcasted successfully. TXID:", txid)

except Exception as e:
    print(f"\nAn error occurred during transaction creation or broadcast: {e}")