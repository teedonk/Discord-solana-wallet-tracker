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

def add_wallet(user_input: str) -> str:
    parts = user_input.split()
    if len(parts) != 2 or parts[0] != '/add_wallet':
        return 'Invalid command. Please use /add_wallet <wallet_address>.'

    wallet_address = parts[1]
    # Add wallet to memory
    wallets[wallet_address] = wallet_address
    # Save wallets to file
    save_wallets(wallets)
    return f'Wallet {wallet_address} saved.'

def remove_wallet(user_input: str) -> str:
    parts = user_input.split()
    if len(parts) != 2 or parts[0] != '/remove_wallet':
        return 'Invalid command. Please use /remove_wallet <wallet_address>.'

    wallet_address = parts[1]
    # Check if wallet exists
    if wallet_address in wallets:
        del wallets[wallet_address]
        # Save wallets to file
        save_wallets(wallets)
        return f'Wallet {wallet_address} deleted.'
    else:
        return f'Wallet {wallet_address} not found.'

def wallet_list() -> str:
    if wallets:
        return f'Wallets saved: {", ".join(wallets.keys())}'
    else:
        return 'No wallets saved.'


TRACKED_WALLETS_FILE = "tracked_wallets.txt"

def load_tracked_wallets() -> Dict[str, str]:
    try:
        with open(TRACKED_WALLETS_FILE, "r") as file:
            tracked_wallets = {line.strip(): line.strip() for line in file}
    except FileNotFoundError:
        tracked_wallets = {}
    return tracked_wallets

def save_tracked_wallets(tracked_wallets: Dict[str, str]) -> None:
    with open(TRACKED_WALLETS_FILE, "w") as file:
        for wallet_address in tracked_wallets:
            file.write(wallet_address + "\n")

tracked_wallets = load_tracked_wallets()


def track_wallet(wallet_address: str) -> str:
    # Add wallet to memory
    tracked_wallets[wallet_address] = wallet_address
    # Save tracked wallets to file
    save_tracked_wallets(tracked_wallets)
    return f'Wallet {wallet_address} is now being tracked.'

def untrack_wallet(wallet_address: str) -> str:
    # Check if wallet exists
    if wallet_address in tracked_wallets:
        del tracked_wallets[wallet_address]
        # Save tracked wallets to file
        save_tracked_wallets(tracked_wallets)
        return f'Wallet {wallet_address} is no longer being tracked.'
    else:
        return f'Wallet {wallet_address} is not being tracked.'
