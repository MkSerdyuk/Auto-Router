import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Получение ссылки
location = input('Введите субъект федерации (транслитом) ') # субект федерации
city = input('Введите город (транслитом) ') # город
url = 'https://dom.mingkh.ru/krym/'+location+'/'+city
print(url)

f = open('table.csv', 'w')

def scrapData(url):
    global f
    request = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(request.text)
    table = soup.find('table')

    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    del(output_rows[0])
    for p in output_rows:
      for t in p:
        t=t.replace(';', ',')
        f.write(t[:-1]+';')
      f.write('\n')

#сбор данных со всех страниц

scrapData(url) #собираем данные с первой страницы

try:
    scrapData(url) #собираем данные с первой страницы
except:
    print('[Error] Такого города нет')

i = 2 #номер страницы
while True:
    try:
        pUrl = url + '?page=' + str(i) #получаем ссылку на страницу
        scrapData(pUrl)
        i+=1
    except: #как только появляется ошибка, значит страницы с нужным номером уже нет
        break

f.close()
print('Данные успешно загружены')
