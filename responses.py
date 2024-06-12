from random import choice, randint
from discord import Message
from wallet import add_wallet, remove_wallet, wallet_list, track_wallet, untrack_wallet, tracked_wallets_list
from sol_balance import track_transactions, get_solana_balance

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'
    elif lowered.startswith('/add_wallet'):
        parts = user_input.split()
        if len(parts) != 2 or parts[0] != '/add_wallet':
            return 'Invalid command format. Please use /add_wallet <wallet_address>.'
        else:
            result = add_wallet(user_input)
            if "successfully" in result:
                wallet_address = parts[1]
                track_transactions(wallet_address)  # Start tracking transactions
            return result
    elif lowered.startswith('/remove_wallet'):
        return remove_wallet(user_input)


    elif lowered.startswith('/track_wallet'):
        parts = user_input.split()
        if len(parts) != 2 or parts[0] != '/track_wallet':
            return 'Invalid command format. Please use /track_wallet <wallet_address>.'
        else:
            return "Wallet tracking command received. Check the designated channel for updates."
    elif lowered.startswith('/untrack_wallet'):
        parts = user_input.split()
        if len(parts) != 2 or parts[0] != '/untrack_wallet':
            return 'Invalid command format. Please use /untrack_wallet <wallet_address>.'
        else:
            wallet_address = parts[1]
            return untrack_wallet(wallet_address)

    elif lowered == '/tracked_wallets':
        return tracked_wallets_list()
    elif lowered == '/wallet_list':
        return wallet_list()
    elif lowered.startswith('/balance'):
        wallet_address = user_input.split()[1]
        balance = get_solana_balance(wallet_address)
        if balance is not None:
            return f"Balance of {wallet_address}: {balance} SOL"
        else:
            return "Failed to retrieve balance."
    else:
        return choice(['I do not understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])
