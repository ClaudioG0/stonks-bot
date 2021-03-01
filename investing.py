import translators as ts
from lxml import html
import requests as rq
from bs4 import BeautifulSoup



with rq.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }

ticker = input("Enter ticker: ")
link = 'https://finviz.com/quote.ashx?t=' + ticker
response = se.get(link)

soup = BeautifulSoup(response.text, 'lxml')
print(soup.title.text, '\n')
marketCap = soup.find('td', text='Market Cap').find_next()
PE = soup.find('td', text='P/E').find_next()
PS = soup.find('td', text='P/S').find_next()
PB = soup.find('td', text='P/B').find_next()
ROE = soup.find('td', text='ROE').find_next()
ROA = soup.find('td', text='Debt/Eq').find_next()
shortFloat = soup.find('td', text='Short Float').find_next()
recom = soup.find('td', text='Recom').find_next()


introAboutComp = soup.find('td', attrs={'class': 'fullview-profile'})
link = soup.find('table', attrs={'class': 'fullview-title'}).find('a', attrs={'class': 'tab-link'})

print('Market Cap: ', marketCap.text)
print('P/E: ', PE.text)
print('P/S: ', PS.text)
print('P/B: ', PB.text)
print('ROE: ', ROE.text)
print('ROA: ', ROA.text)
print('Short Float: ', shortFloat.text)
print('recom: ', recom.text)

print('link: ', link['href'])
print('\n', ts.google(introAboutComp.text, to_language='ru'))
