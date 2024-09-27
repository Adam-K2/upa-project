import sys
import urllib.request
from bs4 import BeautifulSoup
import csv 
import re

# Some descriptions contain many values, sorting only the first one
def extract_first(text):
    text = text.split(':', 1)[-1]  # Get the part after the first colon
    parts = re.split(r'[,\s/]+', text.strip())  # Spliting spaces and other dividers
    if parts:
        return parts[0].strip()
    else:
        return 'None'

# Create tsv file to output
writer = csv.writer(sys.stdout, delimiter='\t')
# TSV header
writer.writerow(['url', 'name', 'price', 'quantity_box', 'quantity_carton', 'color', 'material', 'dipping'])
# Data from stdin
for url in sys.stdin:
    url = url.strip() # To remove \n character at the end of url string

    try:
        # Fetch the URL content
        with urllib.request.urlopen(url) as response:
            resp_content = response.read()
        content = BeautifulSoup(resp_content, 'html.parser')

        # All parameters for each product
        package_info = {
            'url': url,
            'name': 'None',
            'price': 'None',
            'quantity_box': 'None',
            'quantity_carton': 'None',
            'color': 'None',
            'material': 'None',
            'dipping': 'None'
        }

        product_name = content.find('h1', class_='product-content__name').text.strip()
        stripped_product_name = product_name.split(' - ')[0]
        package_info['name'] = stripped_product_name

        # Needed to find price in JavaScript variable
        scripts = content.find_all('script')

        # Use regex to find the price within the script content
        price_pattern = re.compile(r'price":\s*"([^"]+)"')
        for script in scripts:
            if script.string:
                match = price_pattern.search(script.string)
                if match:
                    price = match.group(1)
                    package_info['price'] = price
                    break

        list_arrow = content.find('div', class_='list-arrow')
        # In case of any error would occur
        if list_arrow is None:
            print(f"Error: No additional parameters found for {url}")
            continue

        for ul in list_arrow.find_all('ul'):
            for li in ul.find_all('li'):
                # Loop for "počet v balení" and "počet v kartonu"
                if "počet v balení" in li.text:
                    # Extract values
                    parts = li.text.split(';')
                    for part in parts:
                        # Check where the string is longer and contain extra information
                        if ':' in part:
                            key, value = part.split(':', 1)  # Split only on the first colon, without this longer description cause error
                            key = key.strip()
                            if key == "počet v balení":
                                package_info['quantity_box'] = extract_first(value)
                            elif key == "počet v kartonu":
                                package_info['quantity_carton'] = extract_first(value)
                        else:
                            continue

                # Check for "barva"
                if "barva:" in li.text:
                    package_info['color'] = extract_first(li.text.split('barva:')[1])
                
                # Check for "materiál"
                if "materiál:" in li.text:
                    package_info['material'] = extract_first(li.text.split('materiál:')[1])
                
                # Check for "máčení"
                if "máčení:" in li.text:
                    package_info['dipping'] = extract_first(li.text.split('máčení:')[1])
      
        # Write into tsv file
        writer.writerow([
            package_info['url'],
            package_info['name'],
            package_info['price'],
            package_info['quantity_box'],
            package_info['quantity_carton'],
            package_info['color'],
            package_info['material'],
            package_info['dipping']
        ])
    except Exception as e:
        print(f'Failed to retrieve the data for {url}: {e}')