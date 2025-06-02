import json

# Function to load card data
def load_card_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Load card data
card_data = load_card_data("D:/Yu-Gi-Oh MD/Card Reader/Database/card_data.json")

# Function to load hash data
def load_hash_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Function to format card details
def format_card_details(cid, card_data):
    card = card_data.get(str(cid))
    if not card:
        return "Card details not found.", ""
    
    details = []
    details.append(f"Card ID: {card.get('cid')}")
    if card.get('en_name'):
        details.append(f"Name: {card.get('en_name')}")
    if card.get('text', {}).get('types'):
        details.append(f"Type: {card['text']['types']}")
    if card.get('data', {}).get('type') is not None:
        details.append(f"Card Type: {card['data']['type']}")
    if card.get('data', {}).get('atk') != "null":
        details.append(f"ATK: {card['data']['atk']}")
    if card.get('data', {}).get('def') != "null":
        details.append(f"DEF: {card['data']['def']}")
    if card.get('data', {}).get('level') != "null":
        details.append(f"Level: {card['data']['level']}")
    if card.get('data', {}).get('race') != "null":
        details.append(f"Race: {card['data']['race']}")
    if card.get('data', {}).get('attribute') != "null":
        details.append(f"Attribute: {card['data']['attribute']}")
    
    return "\n".join(details), card.get('text', {}).get('desc', "")
