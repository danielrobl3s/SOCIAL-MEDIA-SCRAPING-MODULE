import re
import csv

reactions_pattern = '\d'
reactions = []

with open('postsFB.txt', 'r', encoding='utf-8') as file:
    lines =file.readlines()

    for i, line in enumerate(lines):
        line = line.strip()

        try:
            next_line = lines[i+1].strip()
        except:
            print('-------fin del archivo-------')

        if "contacto hoy" in line.lower():
            print(line)
            print(next_line)

        """ next_line = lines[i+1].strip()
        reactions.append(re.findall(reactions_pattern, next_line))


with open('clean_postsFB.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write(str(reactions)) """