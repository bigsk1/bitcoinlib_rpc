# Change wallet name to what you want at bottom of script only

from bitcoinlib.wallets import Wallet

def create_wallet_and_save_details(wallet_name):
    try:
        # Create a new wallet
        wallet = Wallet.create(wallet_name)

        # Get the first key from the wallet
        key = wallet.get_key()

        # Get address, public key in hex, and private key in WIF format
        address = key.address
        private_key_wif = key.wif

        # Prepare data to save
        data_to_save = (
            f"Wallet Name: {wallet_name}\n"
            f"Address: {address}\n"
            f"Private Key: {private_key_wif}\n"
        )

        # Save to a .txt file
        file_name = f"{wallet_name}_details.txt"
        with open(file_name, 'w') as file:
            file.write(data_to_save)

        print(f"Wallet details saved to {file_name}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage
wallet_name = 'TestWallet'
create_wallet_and_save_details(wallet_name)
