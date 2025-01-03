import requests

def get_bitcoin_balance(address):
    """Fetches the Bitcoin balance for a given address using the Blockchair API."""
    url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance_satoshi = data["data"][address]["address"]["balance"]
        balance_btc = balance_satoshi / 100000000  # Convert satoshis to BTC
        return balance_btc
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin balance from Blockchair: {e}")
        return None