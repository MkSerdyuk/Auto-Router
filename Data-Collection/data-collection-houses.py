import pandas as pd
import requests
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup

# Получение ссылки
location = input('Введите субъект федерации (транслитом) ') # субект федерации
city = input('Введите город (транслитом) ') # город
url = 'https://dom.mingkh.ru/'+location+'/'+city+'/houses'
loc = Nominatim(user_agent="GetLoc")
f = open('Houses.csv', 'w')
f.write('Широта;Долгота;Население\n')

def getPopulation(scale, stages):
    return scale*stages/18 #18 кв. м - норма площади на одного человека в РФ

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
        row = {'lat' : 0, 'lon' : 0, 'pop' : 0}
        try:
            coord = convertAdrToCoord(columns[1].text + ', ' + columns[2].text)
            row['lat'] = str(coord[0])
            row['lon'] = str(coord[1])
            row['pop'] = str(getPopulation(float(columns[-3].text), float(columns[-1].text)))
        except:
            row = []
        if row != []:
            f.write(';'.join([row['lat'], row['lon'], row['pop']]))
            f.write('\n')
    return True

#сбор данных со всех страниц

try:
    scrapData(url) #собираем данные с первой страницы
    print('Страница 1 загружена')

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