import bs4 as bs
from typing import List
from selenium import webdriver

def generate_url(name:str)->str:
    processed_name=name.replace(" ","+")
    return f"https://www.jusbrasil.com.br/jurisprudencia/busca?q={processed_name}"

def get_page(url:str)->bs.BeautifulSoup:
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('--headless=new')
    webdriver_options.add_argument("--no-sandbox")
    webdriver_options.add_argument('--disable-dev-shm-usage')
    webdriver_options.binary_location = '/usr/bin/chromium-browser'
    dr = webdriver.Chrome(options=webdriver_options)
    
    dr.get(url)
    soup = bs.BeautifulSoup(dr.page_source, 'html.parser')
    
    return soup

async def get_jurisprudences(name:str)->List[str]:
    url=generate_url(name)
    page=get_page(url)
    raw=page.find_all(class_='search-snippet-base_SearchSnippetBase__sMKry')
    print(raw)
    jurisprudences=[]
    for j in raw:
        item={
            "title":j.find(class_='search-snippet-base_SearchSnippetBase-titleLink__ms7sZ').text,
            "body":j.find(class_='search-snippet-base_SearchSnippetBase-body__OY5oa').text,
        }
        jurisprudences.append(item)
        
    return jurisprudences