import json
from datetime import datetime
import os

files = [
    'scrapedItems/threedboxItems.json',
    'scrapedItems/mintictItems.json', 
    'scrapedItems/deltapcItems.json', 
    'scrapedItems/technoshopItems.json', 
    'scrapedItems/itshopItems.json',
    'scrapedItems/mediamarketItems.json',
    ]

def merge_json_files(input_files, output_filename):
    result = []
    for file in input_files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as infile:
                result.extend(json.load(infile))
        else:
            print(f"Warning: {file} does not exist.")
    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        json.dump(result, output_file, indent=4, ensure_ascii=False)

# Generate a new file name based on the current timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_filename = f'scrapedItems/merged_items_{timestamp}.json'

merge_json_files(files, output_filename)

# python combineItems.py