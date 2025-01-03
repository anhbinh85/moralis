def format_balance(balance):
    """Formats a balance with thousands separators."""
    if balance is None:
        return "N/A"
    return "{:,.4f}".format(balance)

def format_supply(supply):
    """Formats a supply number with thousands separators."""
    if supply is None or supply == "N/A":
        return "N/A"
    try:
        return "{:,.0f}".format(float(supply))
    except (ValueError, TypeError):
        print(f"Warning: Could not format supply value: {supply}")
        return "N/A"

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