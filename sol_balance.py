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


