# Python script to adjust the CSV file of dataset

new_header = "rok,mesiac,obvod,kod_obvodu,udalost,dopravni_prestupky,ostatni,preventivni_akce\n"

with open('20220101_20240901_mp.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()

lines[0] = new_header

# To adjust lines with \N to NULL for db engine
for i in range(1, len(lines)):
    lines[i] = lines[i].replace('\\N', '')

with open('20220101_20240901_mp.csv', 'w', encoding='utf-8') as file:
    file.writelines(lines)
