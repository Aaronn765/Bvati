import re
import sys

def find_emojis(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Emojis are generally in the range \U00010000-\U0010ffff 
    # and some in \u2600-\u27bf
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u27bf]')
    
    for i, line in enumerate(lines):
        if emoji_pattern.search(line):
            print(f"Line {i+1}: {line.strip()}")

find_emojis('c:/Users/touvo/Desktop/Site/Bvati/index3.html')
