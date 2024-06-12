from typing import Dict
from discord import Message


WALLETS_FILE = "wallets.txt"

# Function to load wallets from the file into memory
def load_wallets() -> Dict[str, str]:
    try:
        with open(WALLETS_FILE, "r") as file:
            wallets = {line.strip(): line.strip() for line in file}
    except FileNotFoundError:
        wallets = {}
    return wallets

# Function to save wallets from memory to the file
def save_wallets(wallets: Dict[str, str]) -> None:
    with open(WALLETS_FILE, "w") as file:
        for wallet_address in wallets:
            file.write(wallet_address + "\n")

wallets = load_wallets()
