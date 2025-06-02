import os
import json

def read_ydk_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    main_deck = []
    extra_deck = []
    current_deck = main_deck
    for line in lines:
        line = line.strip()
        if line == '#main':
            current_deck = main_deck
        elif line == '#extra':
            current_deck = extra_deck
        elif line.isdigit():
            current_deck.append(int(line))
    return main_deck, extra_deck

def load_card_database(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        card_database = json.load(file)
    return card_database

def get_card_info(card_id, card_database):
    for cid, card_data in card_database.items():
        if card_data['id'] == card_id:
            return {
                'name': card_data['en_name'],
                'cid': int(cid)
            }
    return None

def process_ydk_file(file_path, card_database):
    main_deck, extra_deck = read_ydk_file(file_path)
    deck_info = {
        'main': [get_card_info(card_id, card_database) for card_id in main_deck],
        'extra': [get_card_info(card_id, card_database) for card_id in extra_deck],
    }
    return deck_info

def save_to_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
current_directory = os.path.dirname(os.path.abspath(__file__))
card_database_file = "D:\\Yu-Gi-Oh MD\\Card Reader\\Database\\card_data.json"
output_directory = "D:\\Yu-Gi-Oh MD\\Card Reader\\Database\\Deck"

card_database = load_card_database(card_database_file)

ydk_files = [file for file in os.listdir(current_directory) if file.endswith('.ydk')]

for ydk_file in ydk_files:
    file_path = os.path.join(current_directory, ydk_file)
    deck_info = process_ydk_file(file_path, card_database)
    
    json_file_name = os.path.splitext(ydk_file)[0] + '.json'
    json_file_path = os.path.join(output_directory, json_file_name)
    save_to_json(deck_info, json_file_path)
    print(f"Converted {ydk_file} to {json_file_name}")