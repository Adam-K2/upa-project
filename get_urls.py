import requests
from bs4 import BeautifulSoup

# Eshop site
site_url = 'https://www.ardon.cz/feeds/site-map-products-cz-cs-CZ.xml'
resp = requests.get(site_url)

if resp.status_code == 200:
    # Parse of xml file
    content = BeautifulSoup(resp.content, 'lxml-xml')

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
else:
    print('Failed to retrieve the data')