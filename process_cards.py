import json
import random
# json.loads(line.decode("utf-8"))

def is_vintage_legal( card ):
    if 'vintage' not in card['legalities']:
        return False
    if card['legalities']['vintage'] != 'Legal':
        return False
    return True

################################################
# cards.json and stub.json
with open('input/cards.json', encoding='utf8') as f:
    data = json.load(f)

new_cards = {}
for x in range(17):
    new_cards[x] = {}

new_card = {}
for _, card in data.items():
    if 'Creature' in card['types']:
        if is_vintage_legal(card) and 'manaCost' in card and 'X' not in card['manaCost']:
            cmc = card['convertedManaCost']
            if card['name'] not in new_cards[cmc]:
                new_card = {
                    'name':card['name'],
                    'manaCost':card['manaCost'],
                    'type':card['type'],
                    'text':card['text'],
                    'power':card['power'],
                    'toughness':card['toughness']
                }
                new_cards[cmc][card['name']] = new_card


with open('output/ncards.json', 'w') as outfile:
    json.dump(new_cards, outfile)