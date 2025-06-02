import json

# Define file paths
card_data_file = r"D:\Yu-Gi-Oh MD\Card Reader\Database\card_data.json"

# Define the mappings directly
attribute_mapping = {
    1: '0', 2: 'DARK', 3: 'DIVINE', 4: 'EARTH', 5: 'FIRE', 6: 'LIGHT', 7: 'WATER', 8: 'WIND'
}
race_mapping = {
    1: '', 2: 'Abidos the Th', 3: 'Adrian Gecko', 4: 'Alexis Rhodes', 5: 'Amnael', 6: 'Andrew',
    7: 'Aqua', 8: 'Arkana', 9: 'Aster Phoenix', 10: 'Axel Brodie', 11: 'Bastion Misaw', 12: 'Beast',
    13: 'Beast-Warrior', 14: 'Bonz', 15: 'Camula', 16: 'Chazz Princet', 17: 'Christine', 18: 'Chumley Huffi',
    19: 'Continuous', 20: 'Counter', 21: 'Creator-God', 22: 'Cyberse', 23: 'David', 24: 'Dinosaur',
    25: 'Divine-Beast', 26: 'Don Zaloog', 27: 'Dr. Vellian C', 28: 'Dragon', 29: 'Emma', 30: 'Equip',
    31: 'Espa Roba', 32: 'Fairy', 33: 'Field', 34: 'Fiend', 35: 'Fish', 36: 'Illusion', 37: 'Insect',
    38: 'Ishizu', 39: 'Ishizu Ishtar', 40: 'Jaden Yuki', 41: 'Jesse Anderso', 42: 'Joey', 43: 'Joey Wheeler',
    44: 'Kagemaru', 45: 'Kaiba', 46: 'Keith', 47: 'Lumis Umbra', 48: 'Lumis and Umb', 49: 'Machine',
    50: 'Mai', 51: 'Mai Valentine', 52: 'Mako', 53: 'Nightshroud', 54: 'Normal', 55: 'Odion',
    56: 'Paradox Broth', 57: 'Pegasus', 58: 'Plant', 59: 'Psychic', 60: 'Pyro', 61: 'Quick-Play',
    62: 'Reptile', 63: 'Rex', 64: 'Ritual', 65: 'Rock', 66: 'Sea Serpent', 67: 'Seto Kaiba',
    68: 'Spellcaster', 69: 'Syrus Truesda', 70: 'Tania', 71: 'Tea Gardner', 72: 'The Supreme K',
    73: 'Thelonious Vi', 74: 'Thunder', 75: 'Titan', 76: 'Tyranno Hassl', 77: 'Warrior', 78: 'Weevil',
    79: 'Winged Beast', 80: 'Wyrm', 81: 'Yami Bakura', 82: 'Yami Marik', 83: 'Yami Yugi', 84: 'Yubel',
    85: 'Yugi', 86: 'Zane Truesdal', 87: 'Zombie'
}
type_mapping = {
    1: 'Effect Monster', 2: 'Flip Effect Monster', 3: 'Fusion Monster', 4: 'Gemini Monster', 5: 'Link Monster',
    6: 'Normal Monster', 7: 'Normal Tuner Monster', 8: 'Pendulum Effect Fusion Monster', 9: 'Pendulum Effect Monster',
    10: 'Pendulum Effect Ritual Monster', 11: 'Pendulum Flip Effect Monster', 12: 'Pendulum Normal Monster',
    13: 'Pendulum Tuner Effect Monster', 14: 'Ritual Effect Monster', 15: 'Ritual Monster', 16: 'Skill Card',
    17: 'Spell Card', 18: 'Spirit Monster', 19: 'Synchro Monster', 20: 'Synchro Pendulum Effect Monster',
    21: 'Synchro Tuner Monster', 22: 'Token', 23: 'Toon Monster', 24: 'Trap Card', 25: 'Tuner Monster',
    26: 'Union Effect Monster', 27: 'XYZ Monster', 28: 'XYZ Pendulum Effect Monster'
}

# Load the card data
with open(card_data_file, 'r', encoding='utf-8') as file:
    card_data = json.load(file)

# Update the card data with the mappings
for card_id, card_info in card_data.items():
    card_info['data']['attribute'] = attribute_mapping.get(card_info['data']['attribute'], card_info['data']['attribute'])
    card_info['data']['type'] = type_mapping.get(card_info['data']['type'], card_info['data']['type'])
    card_info['data']['race'] = race_mapping.get(card_info['data']['race'], card_info['data']['race'])

# Save the updated card data
with open(card_data_file, 'w', encoding='utf-8') as file:
    json.dump(card_data, file, ensure_ascii=False, indent=4)

print("card_data.json has been updated successfully.")
