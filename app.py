import streamlit as st
from utils import format_balance, format_supply, format_nft_metadata
from moralis import evm_api
from cachetools import TTLCache, cached
import time
from moralis_api import get_api_key, get_native_balance, get_token_balances, \
    get_wallet_transactions, get_nft_transfers, get_nfts, \
    get_erc20_token_transfers, get_wallet_net_worth, get_wallet_pnl, get_wallet_pnl_breakdown
# Cache for Moralis API responses with a TTL of 1 minute (60 seconds)
moralis_cache = TTLCache(maxsize=100, ttl=60)

@cached(moralis_cache)
def get_cached_token_balances(address, chain, api_key):
    print("Fetching token balances from API (not cached)")
    return get_token_balances(address, chain, api_key)

@cached(moralis_cache)
def get_cached_wallet_transactions(address, chain, api_key, from_block=None, to_block=None, from_date=None, to_date=None):
    print("Fetching wallet transactions from API (not cached)")
    return get_wallet_transactions(address, chain, api_key, from_block, to_block, from_date, to_date)

@cached(moralis_cache)
def get_cached_nft_transfers(address, chain, api_key):
    print("Fetching NFT transfers from API (not cached)")
    return get_nft_transfers(address, chain, api_key)

@cached(moralis_cache)
def get_cached_nfts(address, chain, api_key):
    print("Fetching NFTs from API (not cached)")
    return get_nfts(address, chain, api_key)

@cached(moralis_cache)
def get_cached_erc20_token_transfers(address, chain, api_key):
    print("Fetching ERC20 token transfers from API (not cached)")
    return get_erc20_token_transfers(address, chain, api_key)

@cached(moralis_cache)
def get_cached_wallet_net_worth(address, chain, api_key, exclude_spam=True, exclude_unverified_contracts=True):
    print("Fetching wallet net worth from API (not cached)")
    return get_wallet_net_worth(address, chain, api_key, exclude_spam, exclude_unverified_contracts)

@cached(moralis_cache)
def get_cached_wallet_pnl(address, chain, api_key):
    print("Fetching wallet pnl from API (not cached)")
    return get_wallet_pnl(address, chain, api_key)

@cached(moralis_cache)
def get_cached_wallet_pnl_breakdown(address, chain, api_key):
    print("Fetching wallet pnl BREAKDOWN from API (not cached)")
    return get_wallet_pnl_breakdown(address, chain, api_key)

def main():
    st.title("Whale Wallet Explorer")

    api_key = get_api_key()

    if not api_key:
        st.error("Error: Moralis API key not found in config.ini. Please set the API key and restart the application.")
        return

    # Input for wallet address
    wallet_address = st.text_input("Enter Wallet Address", "0x00000000219ab540356cbb839cbe05303d7705fa")

    # Select chain using hex chain IDs
    chain_options = {
        "Ethereum Mainnet": "0x1",
        "Goerli Testnet": "0x5",
        "Polygon Mainnet": "0x89",
        "Binance Smart Chain": "0x38",
        "Avalanche C-Chain": "0xa86a",
        "Solana Mainnet": "solana"
        # Add other chains as needed
    }
    selected_chain_name = st.selectbox("Select Chain", list(chain_options.keys()))
    chain = chain_options[selected_chain_name]

    # Add a button to clear the cache
    if st.button("Clear Cache"):
        moralis_cache.clear()
        st.success("Cache cleared!")

    # Native Balance
    if st.button("Get Native Balance"):
        with st.spinner("Fetching native balance..."):
            native_balance = get_native_balance(wallet_address, chain, api_key)
            if native_balance is not None:
                st.success(f"Native Balance ({selected_chain_name}): {format_balance(native_balance)}")
            else:
                st.error(f"Failed to retrieve native balance for {selected_chain_name}.")

    # ERC20 Token Balances
    if st.button("Get ERC20 Token Balances"):
        with st.spinner("Fetching ERC20 token balances..."):
            token_balances = get_cached_token_balances(wallet_address, chain, api_key)
            if token_balances:
                token_data = []
                for token in token_balances:
                    token_data.append({
                        "Logo": token.get("logo"),
                        "Name": token["name"],
                        "Symbol": token["symbol"],
                        "Address": token["address"],
                        "Balance": format_balance(token["balance"]),
                        "Decimals": token.get("decimals", "N/A"),
                        "Total Supply": format_supply(token.get("total_supply_formatted", "N/A")),
                        "Contract Verified": "✅" if token.get("verified_contract", "N/A") else "❌",
                        "Possible Spam": "✅" if token.get("possible_spam", "N/A") else "❌",
                        "Security Score": token.get("security_score", "N/A")
                    })

                st.write("Token Balances:")
                st.dataframe(token_data, hide_index=True, column_config={
                    "Logo": st.column_config.ImageColumn("Logo", width="small"),
                    "Name": st.column_config.TextColumn("Name"),
                    "Symbol": st.column_config.TextColumn("Symbol"),
                    "Address": st.column_config.TextColumn("Address"),
                    "Balance": st.column_config.NumberColumn("Balance", format="%.4f"),
                    "Decimals": st.column_config.NumberColumn("Decimals"),
                    "Total Supply": st.column_config.NumberColumn("Total Supply", format="%.4f"),
                    "Contract Verified": st.column_config.TextColumn("Contract Verified"),
                    "Possible Spam": st.column_config.TextColumn("Possible Spam"),
                    "Security Score": st.column_config.NumberColumn("Security Score")
                }, use_container_width=True)
            else:
                st.info("No ERC-20 tokens found for this wallet.")
    
    # Wallet Transactions
    if st.button("Get Wallet Transactions"):
        with st.spinner("Fetching wallet transactions..."):
            transactions = get_cached_wallet_transactions(wallet_address, chain, api_key, from_block=18000000)
            if transactions:
                st.write("Wallet Transactions:")
                st.dataframe(transactions, use_container_width=True)
            else:
                st.info("No wallet transactions found.")

    # NFT Transfers
    if st.button("Get NFT Transfers"):
        with st.spinner("Fetching NFT transfers..."):
            nft_transfers = get_cached_nft_transfers(wallet_address, chain, api_key)
            if nft_transfers:
                st.write("NFT Transfers:")
                st.dataframe(nft_transfers, use_container_width=True)
            else:
                st.info("No NFT transfers found for this wallet.")
    
    # NFTs
    if st.button("Get NFTs"):
        with st.spinner("Fetching NFTs..."):
            nfts = get_cached_nfts(wallet_address, chain, api_key)
            if nfts:
                st.write("NFTs:")
                nfts_data = []
                for nft in nfts:
                    nfts_data.append({
                        "Name": nft.get("name", "N/A"),
                        "Symbol": nft.get("symbol", "N/A"),
                        "Token Address": nft.get("token_address", "N/A"),
                        "Token ID": nft.get("token_id", "N/A"),
                        "Amount": nft.get("amount", "N/A"),
                        "Contract Type": nft.get("contract_type", "N/A"),
                        "Token URI": nft.get("token_uri", "N/A"),
                        "Metadata": format_nft_metadata(nft.get("metadata")),
                        "Possible Spam": "✅" if nft.get("possible_spam") else "❌",
                        "Verified Collection": "✅" if nft.get("verified_collection") else "❌",
                    })

                st.dataframe(nfts_data, use_container_width=True)
            else:
                st.info("No NFTs found for this wallet.")
    
    # ERC20 Token Transfers
    if st.button("Get ERC20 Token Transfers"):
        with st.spinner("Fetching ERC20 token transfers..."):
            erc20_transfers = get_cached_erc20_token_transfers(wallet_address, chain, api_key)
            if erc20_transfers:
                st.write("ERC20 Token Transfers:")
                st.dataframe(erc20_transfers, use_container_width=True)
            else:
                st.info("No ERC20 token transfers found for this wallet.")

    if st.button("Get Wallet Net Worth"):
        with st.spinner("Fetching wallet net worth..."):
            net_worth_data = get_cached_wallet_net_worth(wallet_address, chain, api_key)
            if net_worth_data:
                st.write("Wallet Net Worth:")
                st.dataframe(net_worth_data, use_container_width=True)
            else:
                st.info("Could not retrieve wallet net worth.")

    if st.button("Get Wallet PnL"):
            with st.spinner("Fetching wallet PnL..."):
                pnl_data = get_cached_wallet_pnl(wallet_address, chain, api_key)
                if pnl_data:
                    st.write("Wallet PnL:")
                    st.dataframe(pnl_data, use_container_width=True)
                else:
                    st.info("Could not retrieve wallet PnL.")

    if st.button("Get Wallet PnL Breakdown"):
            with st.spinner("Fetching wallet PnL Breakdown..."):
                pnl_data = get_cached_wallet_pnl_breakdown(wallet_address, chain, api_key)
                if pnl_data and isinstance(pnl_data, list):
                    for token_pnl in pnl_data:
                        st.write(f"Wallet PnL for Token: {token_pnl[0]['Value'] if token_pnl[0]['Metric'] == 'token_address' else 'Unknown'}:")
                        st.dataframe(token_pnl, use_container_width=True)
                else:
                    st.info("Could not retrieve wallet PnL or invalid response format.")

if __name__ == "__main__":
    main()