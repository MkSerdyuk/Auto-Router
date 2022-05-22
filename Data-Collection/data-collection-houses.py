import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Получение ссылки
location = input('Введите субъект федерации (транслитом) ') # субект федерации
city = input('Введите город (транслитом) ') # город
url = 'https://dom.mingkh.ru/'+location+'/'+city+'/houses'
print(url)

f = open('houses.csv', 'w')

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
    if len(output_rows) == 1: #если длина 1, то колонок нет
        return False
    del(output_rows[0])
    for p in output_rows:
        if not '—' in p: #если в строке пропуск, то она повреждена
            for t in p:
                t=t.replace(';', ',')
                f.write(t+';')
            f.write('\n')
    return True

#сбор данных со всех страниц

try:
    scrapData(url) #собираем данные с первой страницы
    print('Страница',1,'загружена')
    i = 2 #номер страницы

    pUrl = url + '?page=' + str(i) #получаем ссылку на страницу

    while scrapData(pUrl):
        print('Страница',i,'загружена')
        i+=1
        pUrl = url + '?page=' + str(i) #получаем ссылку на страницу
except:
    print('[Error] Такого города нет')

f.close()
print('Данные успешно загружены')
