from moralis import evm_api, sol_api
import configparser
import time
from cachetools import TTLCache, cached

# Cache for Moralis API responses with a TTL of 1 minute (60 seconds)
moralis_cache = TTLCache(maxsize=100, ttl=60)

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def get_api_key():
    config = load_config()
    try:
        api_key = config['moralis']['api_key']
    except KeyError:
        print("Error: API key not found in config.ini")
        api_key = None
    return api_key

def get_native_balance(address, chain, api_key):
    if not api_key:
        print("Error: API key not loaded from config.ini.")
        return None

    try:
        if chain == "solana":
            # Solana: Use the get_native_balance from sol_api
            result = sol_api.account.get_native_balance(
                api_key=api_key,
                params={
                    "network": "mainnet",
                    "address": address,
                },
            )
            balance = int(result["lamports"])
            balance_sol = balance / 1e9
            return balance_sol
        else:
            # EVM: Use the get_native_balance from evm_api
            result = evm_api.balance.get_native_balance(
                api_key=api_key,
                params={
                    "address": address,
                    "chain": chain,
                },
            )
            balance_wei = int(result["balance"])
            balance_eth = balance_wei / 1e18
            return balance_eth

    except Exception as e:
        print(f"Error getting native balance: {e}")
        return None

@cached(moralis_cache)
def get_token_balances(address, chain, api_key):
    print("Fetching token balances from API (not cached)")
    if not api_key:
        print("Error: API key not loaded from config.ini.")
        return None
    
    try:
        if chain == "solana":
            result = sol_api.account.get_spl(
                api_key=api_key,
                params={
                    "network": "mainnet",
                    "address": address
                }
            )

            token_balances = []
            for token in result:
                token_name = token.get("name", "N/A")
                token_symbol = token.get("symbol", "N/A")
                token_address = token["mint"]
                
                # Handle the amount as a float
                try:
                    amount = float(token.get("amount", "0"))
                except (ValueError, TypeError):
                    print(f"Warning: Invalid amount value for {token_symbol} ({token_address}). Skipping balance formatting.")
                    amount = 0
                
                balance = amount / (10 ** int(token.get("decimals", 0)))

                if balance > 0:
                    token_balances.append({
                        "name": token_name,
                        "symbol": token_symbol,
                        "address": token_address,
                        "balance": balance,
                        "decimals": token.get("decimals"),
                        "possible_spam": token.get("possible_spam"),
                        "verified_contract": "N/A",  # Not available in SPL response
                        "logo": token.get("thumbnail"),
                        "total_supply_formatted": token.get("total_supply"),  # Not available in SPL response
                    })
            return token_balances
        else:
            # EVM: Use the get_wallet_token_balances from evm_api
            result = evm_api.token.get_wallet_token_balances(
                api_key=api_key,
                params={
                    "address": address,
                    "chain": chain,
                },
            )

            token_balances = []
            for token in result:
                token_name = token.get("name", "N/A")
                token_symbol = token.get("symbol", "N/A")
                token_address = token["token_address"]
                balance_wei = int(token["balance"])
                
                # Handle missing or None decimals
                try:
                    decimals = int(token.get("decimals", 0))
                    balance = balance_wei / (10 ** decimals) if decimals > 0 else balance_wei
                except (ValueError, TypeError):
                    print(f"Warning: Invalid decimals value for {token_symbol} ({token_address}). Skipping balance formatting.")
                    balance = balance_wei

                if balance > 0:
                    token_balances.append({
                        "name": token_name,
                        "symbol": token_symbol,
                        "address": token_address,
                        "balance": balance,
                        "logo": token.get("thumbnail", None),
                        "decimals": token.get("decimals"),
                        "total_supply_formatted": token.get("total_supply_formatted"),
                        "percentage_relative_to_total_supply": token.get("percentage_relative_to_total_supply"),
                        "possible_spam": token.get("possible_spam"),
                        "verified_contract": token.get("verified_contract"),
                        "security_score": token.get("security_score")
                    })

            return token_balances

    except Exception as e:
        print(f"Error getting token balances: {e}")
        return None

@cached(moralis_cache)
def get_wallet_transactions(address, chain, api_key, from_block=None, to_block=None, from_date=None, to_date=None):
    print("Fetching wallet transactions from API (not cached)")
    if not api_key:
        print("Error: API key not loaded from config.ini.")
        return None

    try:
        params = {
            "address": address,
            "chain": chain,
        }
        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        
        result = evm_api.transaction.get_wallet_transactions(
            api_key=api_key,
            params=params,
        )
        
        transactions = []
        for tx in result.get('result', []):
            transactions.append({
                "hash": tx.get("hash"),
                "from_address": tx.get("from_address"),
                "to_address": tx.get("to_address"),
                "value": int(tx.get("value", 0)) / 1e18,
                "gas": tx.get("gas"),
                "gas_price": int(tx.get("gas_price", 0)) / 1e9,
                "block_timestamp": tx.get("block_timestamp")
            })

        return transactions
    except Exception as e:
        print(f"Error getting wallet transactions: {e}")
        return None

@cached(moralis_cache)
def get_nft_transfers(address, chain, api_key):
    print("Fetching NFT transfers from API (not cached)")
    if not api_key:
        print("Error: API key not loaded from config.ini.")
        return None

    try:
        result = evm_api.nft.get_wallet_nft_transfers(
            api_key=api_key,
            params={
                "address": address,
                "chain": chain,
            },
        )

        transfers = []
        for transfer in result.get('result', []):
            transfers.append({
                "block_number": transfer.get("block_number"),
                "transaction_hash": transfer.get("transaction_hash"),
                "from_address": transfer.get("from_address"),
                "to_address": transfer.get("to_address"),
                "token_address": transfer.get("token_address"),
                "token_id": transfer.get("token_id"),
                "amount": transfer.get("amount"),
                "possible_spam": transfer.get("possible_spam"),
                "verified_contract": transfer.get("verified_contract"),
                "block_timestamp": transfer.get("block_timestamp")
            })

        return transfers
    except Exception as e:
        print(f"Error getting NFT transfers: {e}")
        return None

@cached(moralis_cache)
def get_nfts(address, chain, api_key):
    print("Fetching NFTs from API (not cached)")
    if not api_key:
        print("Error: API key not loaded from config.ini.")
        return None

    try:
        result = evm_api.nft.get_wallet_nfts(
            api_key=api_key,
            params={
                "address": address,
                "chain": chain,
            },
        )

        nfts = []
        for nft in result.get('result', []):
            nfts.append({
                "name": nft.get("name"),
                "symbol": nft.get("symbol"),
                "token_address": nft.get("token_address"),
                "token_id": nft.get("token_id"),
                "amount": nft.get("amount"),
                "contract_type": nft.get("contract_type"),
                "token_uri": nft.get("token_uri"),
                "metadata": format_nft_metadata(nft.get("metadata")),
                "possible_spam": nft.get("possible_spam"),
                "verified_collection": nft.get("verified_collection")
            })

        return nfts
    except Exception as e:
        print(f"Error getting NFTs: {e}")
        return None

@cached(moralis_cache)
def get_erc20_token_transfers(address, chain, api_key):
    print("Fetching ERC20 token transfers from API (not cached)")
    if not api_key:
        print("Error: API key not loaded from config.ini.")
        return None

    try:
        result = evm_api.token.get_wallet_token_transfers(
            api_key=api_key,
            params={
                "address": address,
                "chain": chain,
            },
        )

        erc20_transfers = []
        for transfer in result.get('result', []):
            erc20_transfers.append({
                "transaction_hash": transfer.get("transaction_hash"),
                "token_name":transfer.get("token_name"),
                "token_symbol":transfer.get("token_symbol"),
                "address": transfer.get("address"),
                "possible_spam":"✅" if transfer.get("possible_spam") else "❌",
                "to_address": transfer.get("to_address"),
                "from_address": transfer.get("from_address"),
                "value": int(transfer.get("value", 0)) / 1e18,
                "value_with_decimals": transfer.get("value_with_decimals"),
                "block_timestamp": transfer.get("block_timestamp")
            })

        return erc20_transfers
        
    except Exception as e:
        print(f"Error getting ERC20 token transfers: {e}")
        return None

@cached(moralis_cache)
def format_nft_metadata(metadata):
    """Formats NFT metadata for display."""
    if metadata:
        try:
            # Assuming metadata is a JSON string
            import json
            metadata_dict = json.loads(metadata)
            # Customize how you want to display the metadata
            # This is just a basic example
            return ", ".join(f"{k}: {v}" for k, v in metadata_dict.items())
        except json.JSONDecodeError:
            return metadata  # Return as is if not a valid JSON
    return "N/A"

@cached(moralis_cache)
def get_wallet_net_worth(address, chain, api_key, exclude_spam=True, exclude_unverified_contracts=True):
    if not api_key:
        print("Error: API key not loaded from config.ini.")
        return None

    try:
        # EVM: Use the get_wallet_net_worth from evm_api
        result = evm_api.wallets.get_wallet_net_worth(
            api_key=api_key,
            params={
                "address": address,
                "chain": chain,
                "exclude_spam": exclude_spam,
                "exclude_unverified_contracts": exclude_unverified_contracts
            },
        )

        # Check if the result is a dictionary before accessing keys
        if isinstance(result, dict):
            # Format the result for display in a table
            net_worth_data = []
            total_net_worth = 0

            for chain_data in result.get('chains', []):
                native_balance_usd = float(chain_data.get('native_balance_usd', 0))
                token_balance_usd = float(chain_data.get('token_balance_usd', 0))
                total_net_worth += float(chain_data.get('networth_usd', 0))

                net_worth_data.append({
                    "Category": "Native Balance",
                    "Chain": chain_data.get('chain'),
                    "Symbol": "Native",
                    "Balance (USD)": native_balance_usd,
                    "Percentage of Net Worth": chain_data.get('percentage')
                })

                if token_balance_usd > 0:
                    net_worth_data.append({
                        "Category": "Token Balance",
                        "Chain": chain_data.get('chain'),
                        "Symbol": "",  # Token symbol not available in this endpoint
                        "Balance (USD)": token_balance_usd,
                        "Percentage of Net Worth": ""  # Calculate if needed
                    })

            # Add a total row
            net_worth_data.append({
                "Category": "Total Net Worth",
                "Chain": "",
                "Symbol": "",
                "Balance (USD)": total_net_worth,
                "Percentage of Net Worth": ""
            })

            return net_worth_data
        else:
            print("Error: Unexpected response format from get_wallet_net_worth()")
            return None

    except Exception as e:
        print(f"Error getting wallet net worth: {e}")
        return None
    
@cached(moralis_cache)
def get_wallet_pnl(address, chain, api_key):
    print("Fetching wallet PnL from API (not cached)")
    if not api_key:
        print("Error: API key not loaded from config.ini.")
        return None

    try:
        # EVM: Use the get_wallet_pnl from evm_api
        result = evm_api.wallets.get_wallet_profitability_summary(
            api_key=api_key,
            params={
                "address": address,
                "chain": chain,
            },
        )

        pnl_data = [
                {
                    "Metric": "total_count_of_trades",
                    "Value": f"{float(result['total_count_of_trades']):,.2f}"
                },
                {
                    "Metric": "total_trade_volume",
                    "Value": f"{float(result.get('total_trade_volume', 0)):,.2f}"
                },
                {
                    "Metric": "total_realized_profit_usd",
                    "Value": f"{float(result.get('total_realized_profit_usd', 0)):,.2f}"
                },
                {
                    "Metric": "Total Realized Profit (%)",
                    "Value": f"{float(result.get('total_realized_profit_percentage', 0)):,.2f}%" if result.get('total_realized_profit_percentage') is not None else "N/A"
                },
                {
                    "Metric": "total_sold_volume_usd",
                    "Value": f"{float(result.get('total_sold_volume_usd', 0)):,.2f}"
                },
                                {
                    "Metric": "total_bought_volume_usd",
                    "Value": f"{float(result.get('total_bought_volume_usd', 0)):,.2f}"
                }
            ]
        
        return pnl_data

    except Exception as e:
        print(f"Error getting wallet PnL: {e}")
        return None