import requests
from bs4 import BeautifulSoup

test_url = 'https://www.undercurrentnews.com/2020/11/23/canadian-lobster-dock-prices-plummeted-weeks-before-dumping-day/'

resp = requests.get(test_url)
soup = BeautifulSoup(resp.content, 'html.parser')
paragraphs = soup.find_all('p')

for p in paragraphs:
    print(p)