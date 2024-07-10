from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.core import SummaryIndex, Document
from llama_index.readers.web import SimpleWebPageReader
import requests
from decouple import config
import os
from bs4 import BeautifulSoup



os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

def search_ebay(query):
    ebay_products = []
    base_url = "https://www.ebay.com/sch/i.html"
    params = {
        "_nkw": query,
        "_sacat": "0",  # 0 means search in all categories
        "LH_BIN": "1"
    }
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
                           'Accept-Language': 'en-US, en;q=0.5'})
    
    response = requests.get(base_url, params=params, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    print(response.url)

    # Extract product names and URLs
    for result in results[:5]:
        title_element = result.find('div', class_='s-item__title')
        if title_element:
            product_name = title_element.text.strip()
            product_price = result.find('span', class_='s-item__price').text.strip()
            product_url = result.find('a')['href']
            product_info = f"Product Name: {product_name}\nProduct Price: {product_price}\nProduct URL: {product_url}"
            print(product_info)
            ebay_products.append(Document(text=product_info))

    return ebay_products


def ebay_engine(query):
    ebay_products = search_ebay(query)
    
    return ebay_products


ebay_reader_engine = FunctionTool.from_defaults(
    fn=ebay_engine,
    name="ebay_reader_engine",
    description="This tool can retrieve content from an Ebay search page"
)