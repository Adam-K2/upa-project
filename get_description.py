import sys
import requests
from bs4 import BeautifulSoup
import csv 
import re

#pocty karton, pocty krabica, farba, norma, prostredie

# for row in sys.stdin:     # For urls from stdin 
#     print(row)

#url = 'https://www.ardon.cz/kombinovane-rukavice-ardon-r-elton-s-prodejni-etiketou'
url = 'https://www.ardon.cz/macene-rukavice-ardonsafety-houston-y-zluta'

resp = requests.get(url)

if resp.status_code == 200:
    # Parse of xml file
    content = BeautifulSoup(resp.content, 'html.parser')

    product_name = content.find('h1', class_='product-content__name').text.strip()
    stripped_product_name = product_name.split(' - ')[0]
    print(f'Product name: {stripped_product_name}')

    scripts = content.find_all('script')

    # Use regex to find the price within the script content
    price_pattern = re.compile(r'price":\s*"([^"]+)"')
    for script in scripts:
        if script.string:
            match = price_pattern.search(script.string)
            if match:
                price = match.group(1)
                print(f'Price: {price}')  # Print the extracted price
                break

    list_arrow = content.find('div', class_='list-arrow')
    package_info = {}

    # TODO: Pridaj este aby aj prazdne udaje tam boli a bude to asi ok
    for ul in list_arrow.find_all('ul'):
        for li in ul.find_all('li'):
            # Check for "počet v balení" and "počet v kartonu"
            if "počet v balení" in li.text:
                # Extract values
                parts = li.text.split(';')
                for part in parts:
                    key, value = part.split(':')
                    package_info[key.strip()] = value.strip()

            # Check for "barva"
            if "barva:" in li.text:
                package_info['barva'] = li.text.split('barva:')[1].strip()
            
            # Check for "materiál"
            if "materiál:" in li.text:
                package_info['materiál'] = li.text.split('materiál:')[1].strip()

            # Check for "norma"
            if "norma:" in li.text:
                package_info['norma'] = li.text.split('norma:')[1].strip()
            
            if "máčení:" in li.text:
                package_info['máčení'] = li.text.split('máčení:')[1].strip()
    for key, value in package_info.items():
        print(f"{key}: {value}")
else:
    print('Failed to retrieve the data')