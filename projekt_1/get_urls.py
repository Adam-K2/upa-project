import urllib.request
from bs4 import BeautifulSoup

# Eshop site
site_url = 'https://www.ardon.cz/feeds/site-map-products-cz-cs-CZ.xml'

try:
    # Fetch the XML content
    with urllib.request.urlopen(site_url) as response:
        cont = response.read()
    
    content = BeautifulSoup(cont, 'lxml-xml')

    # Load all urls in <loc>
    product_urls = []
    for loc in content.find_all('loc'):
        product_urls.append(loc.text)

    # Filter only gloves urls
    gloves_urls = []
    for url in product_urls:
        if 'rukavice' in url:
            gloves_urls.append(url)

    # Print 150 urls
    for url in gloves_urls[:150]:
        print(url)
        
except Exception as e:
    print(f'Failed to retrieve the data: {e}')