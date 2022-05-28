import pandas as pd
import requests
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup

# Получение ссылки
location = input('Введите субъект федерации (транслитом) ') # субект федерации
city = input('Введите город (транслитом) ') # город
url = 'https://dom.mingkh.ru/'+location+'/'+city+'/houses'
loc = Nominatim(user_agent="GetLoc")
print(url)

f = open('Houses.csv', 'w')
f.write('Широта;Долгота;Площадь;Этажность\n')

def convertAdrToCoord(street):
    global loc
    try:
        getLoc = loc.geocode(street)
        lat = getLoc.latitude
        lon = getLoc.longitude
        return [lat, lon]
    except:
        return -1


def scrapData(url):
    global f
    request = requests.get(url)
    soup = BeautifulSoup(request.text)
    table = soup.find('table')
    if len(table.findAll('tr')) == 1: #если длина 1, то остался только заголовок
        return False
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for i in range(len(columns)):
            if i == 2: #3-я колонка на сайте - адресс
                coord = convertAdrToCoord(columns[i].text)
                if (coord != -1): #если есть координаты
                    output_row += coord
                else:
                    output_row = []
                    break
            else:
                output_row.append(columns[i].text)
        if not '—' in output_row and output_row != []: #если в строке пропуск, то она повреждена
            output_row = output_row[2:] #удаляем колонку с городом и индексом
            del(output_row[-2]) #удаляем лишнюю колонку (в ней находится год постройки)
            for t in output_row:
                f.write(str(t)+';')
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
except Exception as e:
    print(e)

f.close()
print('Данные успешно загружены')
input()
