from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.core import SummaryIndex, Document
from llama_index.readers.web import BeautifulSoupWebReader, SimpleWebPageReader
import requests
from decouple import config
import os
from bs4 import BeautifulSoup


os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

def search_amazon(query):
    azon_products = []
    base_url = "https://www.amazon.com/s"
    params = {
        "k": query,
        "tag": "gabuzee-20"
    }
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
                           'Accept-Language': 'en-US, en;q=0.5'})

    response = requests.get(base_url, params=params, headers=HEADERS)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', {'class': 'puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right'})
    url = response.url
    # print(results)

    #  Extract product names and URLs
    for result in results[:5]:
        try:
            title_element = result.find('h2')
            price_whole = soup.find('span', class_='a-price-whole')

            if title_element and price_whole:
                product_name = title_element.text.strip()
                price_whole = soup.find('span', class_='a-price-whole')
                price_whole = price_whole.text.strip()
                price_decimal = soup.find('span', class_='a-price-fraction')
                price_decimal = price_decimal.text.strip()
                product_price = price_whole + price_decimal
                product_link = soup.find('a', class_='a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal')
                product_link = product_link['href']
                product_url = "https://www.amazon.com" + str(product_link) + "&tag=gabuzee-20"
                # print(product_url)
                product_info = f"Product Name: {product_name}\nProduct Price: {product_price}\nProduct URL: {product_url}"
                azon_products.append(Document(text=product_info))
        except Exception as e:
            print(e)
            # continue
            
    # print(azon_products)
    return azon_products


def amazon_engine(user_input):
    documents = search_amazon(user_input)
    
    return documents

 

amazon_reader_engine = FunctionTool.from_defaults(
    fn=amazon_engine,
    name="amazon_reader_engine",
    description="This tool can retrieve content from an Amazon search page"
)