from solana.rpc.api import Client
from typing import List, Dict
from discord import Message

# Solana RPC endpoint
rpc_endpoint = "https://api.mainnet-beta.solana.com"

# Function to connect to Solana RPC
def connect_rpc() -> Client:
    return Client(rpc_endpoint)


# Function to fetch transactions for a given wallet
def fetch_transactions(wallet_address: str) -> List[Dict]:
    client = connect_rpc()
    return client.get_confirmed_signatures_for_address2(wallet_address)


# Function to send transaction updates as messages through the bot
async def send_transaction_updates(message: Message, wallet_address: str) -> None:
    transactions = fetch_transactions(wallet_address)
    if transactions:
        for transaction in transactions:
            await message.channel.send(f"New transaction for wallet {wallet_address}: {transaction['signature']}")
    else:
        await message.channel.send(f"No new transactions for wallet {wallet_address}")
