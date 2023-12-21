import requests
import argparse
from collections import defaultdict
import locale

def get_tron_data(wallet_address, token_type, contract_address):
    url = f"https://api.trongrid.io/v1/accounts/{wallet_address}/transactions/{token_type}?&contract_address={contract_address}&only_confirmed=true&limit=100"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def process_tron_data(tron_data, searched_wallet_address):
    if not tron_data:
        return None
    
    transactions = tron_data.get('data', [])

    sent_from = defaultdict(float)
    sent_to = defaultdict(float)

    for transaction in transactions:
        from_address = transaction.get('from')
        to_address = transaction.get('to')
        amount = float(transaction.get('value', 0)) / 10**6  # Assuming TRX value is in Sun, convert to TRX

        # Exclude the searched wallet address from the results
        if from_address and from_address != searched_wallet_address:
            sent_from[from_address] += amount

        if to_address and to_address != searched_wallet_address:
            sent_to[to_address] += amount

    # Sort the results in descending order based on the total amount
    sent_from = dict(sorted(sent_from.items(), key=lambda item: item[1], reverse=True))
    sent_to = dict(sorted(sent_to.items(), key=lambda item: item[1], reverse=True))

    return sent_from, sent_to

def display_results(wallet_address, contract_address, token_type, sent_from, sent_to, start_number):
    # Set the locale for formatting currency
    locale.setlocale(locale.LC_ALL, '')

    print("\nEntered parameters:")
    print(f"Wallet Address:\t\t{wallet_address}")
    print(f"Contract Address:\t{contract_address}")
    print(f"Token Type:\t\t{token_type}")

    print("\nResults:")
    
    print("FROM:")
    print("| # | Address | Unique Total |")
    print("|---|---------|--------------|")
    for i, (address, total_amount) in enumerate(sent_from.items(), start=start_number):
        formatted_address = f"\033[91m{address}\033[0m" if address == wallet_address else address
        formatted_amount = locale.currency(total_amount, grouping=True)
        print(f"| {i} | {formatted_address} | {formatted_amount} |")

    start_number += len(sent_from)

    print("\nTO:")
    print("| # | Address | Unique Total |")
    print("|---|---------|--------------|")
    for i, (address, total_amount) in enumerate(sent_to.items(), start=start_number):
        formatted_address = f"\033[91m{address}\033[0m" if address == wallet_address else address
        formatted_amount = locale.currency(total_amount, grouping=True)
        print(f"| {i} | {formatted_address} | {formatted_amount} |")

def get_user_input():
    user_input = input("\nEnter the number to rerun the search (or 'exit' to quit): ")
    return user_input.strip()

def parse_arguments():
    parser = argparse.ArgumentParser(description="TRON Wallet Address Search")
    parser.add_argument("-a", "--address", help="Wallet address to start the search", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    wallet_address = args.address
    token_type = "trc20"
    contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

    start_number = 1

    while True:
        tron_data = get_tron_data(wallet_address, token_type, contract_address)

        if tron_data:
            sent_from, sent_to = process_tron_data(tron_data, wallet_address)

            # Display results without balance information
            display_results(wallet_address, contract_address, token_type, sent_from, sent_to, start_number)

            user_choice = get_user_input()

            if user_choice.lower() == 'exit':
                break
            elif user_choice.isdigit():
                user_choice = int(user_choice)
                if 1 <= user_choice <= len(sent_from) + len(sent_to) - (wallet_address in sent_from):
                    selected_address = list(sent_from.keys())[user_choice - 1] if user_choice <= len(sent_from) else list(sent_to.keys())[user_choice - len(sent_from) - 1]
                    print(f"\nRerunning search with selected address: {selected_address}")
                    wallet_address = selected_address
                else:
                    print("Invalid selection. Please enter a valid number.")
            else:
                print("Invalid input. Please enter a number or 'exit'.")
