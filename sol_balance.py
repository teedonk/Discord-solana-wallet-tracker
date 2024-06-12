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


async def send_transaction_updates(transaction_info: Dict, client) -> None:
    try:
        print("Transaction info received:", transaction_info)  # Debugging statement

        # Extract the contract address from the transaction info
        contract_address = transaction_info['Contract']

        # Get token details from Solscan API
        token_ticker, token_contract_address = get_token_details(contract_address)

        # Construct Solscan link for the transaction
        transaction_link = f"{SOLSCAN_API_URL}/transaction/{transaction_info['signature']}"

        # Format the transaction information including token details
        formatted_transaction_info = f"Transaction Info:\nToken: {token_ticker}\nTransaction Link: {transaction_link}\n{json.dumps(transaction_info)}"

        # Send transaction information to a channel or log it
        channel = client.get_channel(1237353384164724738)
        await channel.send(formatted_transaction_info)

    except Exception as e:
        print("Error:", e)


async def track_transactions(wallet_address: str, client) -> None:
    if wallet_address not in wallets:
        wallets[wallet_address] = ''  # Initialize wallet_address if not present

    while True:
        try:
            # URL of the Solana RPC endpoint
            rpc_url = 'https://api.mainnet-beta.solana.com'

            # Construct the JSON-RPC request payload
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getConfirmedSignaturesForAddress2",
                "params": [wallet_address, {"limit": 1}]
            }

            # Send the request to the Solana RPC endpoint
            response = requests.post(rpc_url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the JSON response
            data = response.json()

            # Extract the most recent transaction signature
            latest_signature = data['result'][-1]['signature']

            # Check if the transaction signature has changed since the last check
            if wallets[wallet_address] != latest_signature:
                # Update the transaction signature for the wallet
                wallets[wallet_address] = latest_signature

                # Retrieve transaction information
                transaction_info = get_transaction_info(latest_signature)

                # Send transaction information to a channel or log it
                await send_transaction_updates(transaction_info, client)
        except Exception as e:
            print("Error:", e)

        # Wait for some time before polling again
        await asyncio.sleep(60)