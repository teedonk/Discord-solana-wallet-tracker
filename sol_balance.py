import requests
import time
from typing import Dict
import asyncio
from wallet import wallets
from discord import Message
from solana.rpc.api import Client
import json
import os
from dotenv import load_dotenv

SOLANA_RPC_URL = 'https://api.mainnet-beta.solana.com'
SOLSCAN_API_URL = 'https://api.solscan.io'
load_dotenv()
SOLSCAN_API_KEY = os.getenv("SOLSCAN_API_KEY")

# Initialize Solana client
solana_client = Client(SOLANA_RPC_URL)

# Function to get token details from Solscan API
def get_token_details(token_address):
    api_url = f"{SOLSCAN_API_URL}/account?address={token_address}"  # Query parameter
    headers = {"Authorization": f"Bearer {SOLSCAN_API_KEY}"}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        token_info = response.json()
        if 'data' in token_info and 'tokenName' in token_info['data']:
            return token_info['data']['tokenName'], token_address
        else:
            print("Error: Unexpected JSON response structure from Solscan")
            return None, None

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        print("Response content:", response.content)  # Print the raw response
        return None, None


def get_solana_balance(wallet_address):
    # URL of the Solana RPC endpoint
    rpc_url = 'https://api.mainnet-beta.solana.com'

    # Construct the JSON-RPC request payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [wallet_address]
    }

    try:
        # Send the request to the Solana RPC endpoint
        response = requests.post(rpc_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Check if account exists
        if 'result' not in data:
            print("Account not found.")
            return None

        # Extract balance from the response
        balance = data['result']['value']['lamports'] / 10 ** 9  # Convert lamports to SOL

        return balance
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def get_transaction_info(transaction_signature: str) -> Dict:
    # URL of the Solana RPC endpoint
    rpc_url = 'https://api.mainnet-beta.solana.com'

    # Construct the JSON-RPC request payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedTransaction",
        "params": [transaction_signature]
    }

    try:
        # Send the request to the Solana RPC endpoint
        response = requests.post(rpc_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Extract relevant transaction information
        amount = data['result']['meta']['postBalances'][0] - data['result']['meta']['preBalances'][0]
        sender = data['result']['transaction']['message']['accountKeys'][0]
        receiver = data['result']['transaction']['message']['accountKeys'][1]
        contract = data['result']['transaction']['message']['accountKeys'][2]

        transaction_info = {
            "Amount": amount,
            "Sender": sender,
            "Receiver": receiver,
            "Contract": contract
        }

        return transaction_info
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
