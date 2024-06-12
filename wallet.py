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
