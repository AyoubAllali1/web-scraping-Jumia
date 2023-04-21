import requests
from bs4 import BeautifulSoup
import re

# Function to check if a product name matches the search query
def matches_query(name, query):
    name_words = name.text.strip().lower().split()
    if name_words[0] != query[0].lower():
        return False
    if len(query) > 1 and len(name_words) < 2:
        return False
    if len(query) > 1 and name_words[1] != query[1].lower():
        return False
    if len(query) > 2 and len(name_words) < 3:
        return False
    if len(query) > 2 and name_words[2] != query[2].lower():
        return False
    return True
def extract_price(price_str):
    # remove all non-numeric characters from the string
    numeric_str = ''.join(filter(str.isdigit, price_str))

    # convert the resulting string to a float and return it
    return float(numeric_str) / 100
import re
def convert_to_float(value_str):
    # Replace any comma with a period
    value_str = value_str.replace(",", ".")
    # Remove any non-numeric characters
    value_str = "".join(filter(str.isdigit, value_str))
    # Convert the string to a float and divide by 100
    return float(value_str) / 100

def extract_price1(price):
    if price is None:
        return None

    price_str = price.replace("Dhs", "").strip()
    pattern = r'\d[\d\,\.]*'
    match = re.search(pattern, price_str)

    if match is None:
        return None

    numeric_str = match.group().replace(',', '')
    return float(numeric_str)

# Main function to scrape Jumia and CosmosElectro for products
def scrape_products(query):
    base_jumia_url='https://www.jumia.ma'
    jumia_url = base_jumia_url+'/catalog/?q=' + '+'.join(query) + '+pro#catalog-listing&page='
    cosmos_url = 'https://www.cosmoselectro.ma/products?categories%5B%5D=0&q=' + '+'.join(query)
    bousfiha_url="https://electrobousfiha.com/recherche?cat_id=all&controller=search&s="+str(query)+"&spr_submit_search=Search&n=21"
#   ecplanet_url = 'https://www.electroplanet.ma/recherche?q='+'+'.join(query)
    columns = {'name': [], 'price': [], 'img url': []}
    for page in range(1, 2):
        print('---', page, '---')
        jumia_r = requests.get(jumia_url + str(page))
        jumia_soup = BeautifulSoup(jumia_r.content, "html.parser")
        jumia_anchors = jumia_soup.find('div', {'class': '-paxs row _no-g _4cl-3cm-shs'}).find_all('article',{'class': 'prd _fb col c-prd'})
        for anchor in jumia_anchors:
            img = anchor.find('a',href=True)["href"]
            name = anchor.find('a').find('div', {'class': 'info'}).find('h3', {'class': 'name'})
            price = anchor.find('a').find('div', {'class': 'info'}).find('div', {'class': 'prc'})
            if matches_query(name, query):
                columns['name'].append(name.text)
                columns['price'].append(extract_price(price.text))
                columns['img url'].append(base_jumia_url+str(img))
        cosmos_r=requests.get(cosmos_url)
        cosmos_soup= BeautifulSoup(cosmos_r.content,"html.parser")
        cosmos_anchors = cosmos_soup.find_all(class_='col-xl-2 col-lg-4 col-md-4 col-sm-6 col-6')
        for anchor in cosmos_anchors:
            img = anchor.find('a', href=True)["href"]
            price = anchor.find(class_='ps-product__price').string
            name = anchor.find(class_='ps-product__title').string

            if matches_query(name, query):
                columns['name'].append(name)
                columns['price'].append(extract_price1(price))
                columns['img url'].append(img)
        bousfiha_r=requests.get(bousfiha_url)
        bousfiha_soup= BeautifulSoup(bousfiha_r.content,'html.parser')
        bousfiha_anchors = bousfiha_soup.find_all(class_="product-container")
        for anchor in bousfiha_anchors:
            img = anchor.find('a',href=True)["href"]
            price = anchor.find(class_='price').string
            name = anchor.find('a',href=True).text
            bousfiha_r = requests.get(bousfiha_url)
            bousfiha_soup = BeautifulSoup(bousfiha_r.content, 'html.parser')
            bousfiha_anchors = bousfiha_soup.find_all(class_="product-container")
            for anchor in bousfiha_anchors:
                img = anchor.find('a', href=True)["href"]
                price = anchor.find(class_='price').string
                name = anchor.find(class_='product-title').find('a', href=True).text
                columns['name'].append(name)
                columns['price'].append(convert_to_float(price))
                columns['img url'].append(img)

    #       ecplanet_r = requests.get(ecplanet_url)
    #       ecplanet_soup = BeautifulSoup(ecplanet_r.content,"html.parser")
    #       ecplanet_anchors = ecplanet_soup.findAll(class_='item product product-item col-lg-3 col-md-3 col-sm-4 col-xs-12')
    #       print(ecplanet_anchors)
    #       for anchor in ecplanet_anchors:
    #        img=anchor.find('a', href=True)["href"]
    #        prices= anchor.find(class_='price')
    #        name = anchor.find(class_='brand').string
    #        name1= anchor.find(class_='ref').string
    #        columns['name'].append(f"{name} {name1}")
    #        columns['price'].append(float(prices))
    #        columns['img url'].append(img)
    return columns

if __name__ == '__main__':
    print("-------------- Please paste the exact name of the item ------------")
    query = input("item name: ").split()
    products=scrape_products(query)
    print("------------------------------")
    for name, price, img_url in zip(products['name'], products['price'], products['img url']):
        print(name, price, img_url)
