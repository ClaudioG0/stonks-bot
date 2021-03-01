import telebot
import re

bot = telebot.TeleBot('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

import translators as ts
from lxml import html
import requests as rq
from bs4 import BeautifulSoup






@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Это тестовая версия бота для показа индикаторов компании."
                          "Чтобы узнать все доступные команды, введи /help")


@bot.message_handler(content_types=['text'])
def send_indicators(message):

    text = message.text
    if text[0] == '.':
        text = text.split('.')
        with rq.Session() as se:
            se.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en"
            }

        # ticker = input("Enter ticker: ")
        link = 'https://finviz.com/quote.ashx?t=' + str(text[1])
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
        recom = float(recom.text)
        if recom >=1 and recom <3:
            recom = "ПОКУПАТЬ"
        elif recom >=3 and recom <4:
            recom = "ДЕРЖАТЬ"
        elif recom>=4 and recom <=5:
            recom = "ПРОДАВАТЬ"
        introAboutComp = soup.find('td', attrs={'class': 'fullview-profile'})
        link = soup.find('table', attrs={'class': 'fullview-title'}).find('a', attrs={'class': 'tab-link'})

        marketCap = 'Market Cap: ' + marketCap.text
        print(marketCap)
        pe = 'P/E: ' + PE.text + '\n'
        ps = 'P/S: ' + PS.text + '\n'
        pb = 'P/B: ' + PB.text + '\n'
        roe = 'ROE: ' + ROE.text + '\n'
        roa = 'ROA: ' + ROA.text + '\n'
        shortFloat = 'Short Float: ' + shortFloat.text + '\n'
        recom = 'recom: ' + recom + '\n'

        link = 'link: ' + link['href'] + '\n'
        introAboutComp = '\n' + ts.google(introAboutComp.text, to_language='ru') + '\n'

        text = marketCap + pe + ps + pb + roe + roa + shortFloat + recom + link
        bot.send_message(message.chat.id, text)



bot.polling()
