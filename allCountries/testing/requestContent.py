import concurrent.futures
import requests
from bs4 import BeautifulSoup

test_url = 'https://www.undercurrentnews.com/2020/11/23/canadian-lobster-dock-prices-plummeted-weeks-before-dumping-day/'

resp = requests.get(test_url)
soup = BeautifulSoup(resp.content, 'html.parser')
paragraphs = soup.find_all('p')

for p in paragraphs:
    print(p)

inputFilePath = ''
f = open(inputFilePath, 'r')
URLS = f.readlines()
f.close()

def checkContent(url):
    
    hasRelevantContent = False

    resp = requests.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        paragraphs = soup.find_all('p')
        
    else:
        print('ERROR WITH GETTING URL CONTENT')
    
    return [url, hasRelevantContent]

RESULTS = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for url in URLS:
        futures.append(executor.submit(checkContent, url))
    
    for future in concurrent.futures.as_completed(futures):
        RESULTS.append(future.result())

csvHeader = 'url,relevant\n'
csvContent = ''
csvContent += csvHeader

for result in RESULTS:
    csvLine = result[0] + ',' + result[1] + '\n'
    csvContent += csvLine

fOut = open('testingContentResults.csv', 'w')
fOut.write(csvContent)
fOut.close()