from urllib import request
from enum import Enum
import pandas as pd 
from math import floor
from bs4 import BeautifulSoup

URL = 'otodom.pl'
SEARCH_PER_PAGE = 72
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
class PropertyType(Enum):
    DOM = 1
    MIESZKANIE = 2

class DealType(Enum):
    BUY = 1
    RENT = 2

class Looker:
    def __init__(self, city: str, dealType: DealType, 
                propertyType: PropertyType, maxSearch: int = -1 ):
        self.city = city
        self.dealType = 'sprzedaz' if dealType == DealType.BUY else 'wynajem'
        self.propertyType = 'dom' if propertyType == PropertyType.DOM else 'mieszkanie'
        self.maxSearch = maxSearch if maxSearch >= 0 else 200
        self.data = []
# https://www.otodom.pl/pl/oferty/sprzedaz/lokal/poznan
    def search(self):
        search_pages = floor(self.maxSearch/SEARCH_PER_PAGE)
        for i in range(search_pages+1):
            page = i+1
            amount_per_page = SEARCH_PER_PAGE if i < search_pages else self.maxSearch%SEARCH_PER_PAGE
            if amount_per_page == 0:
                break
            url = f'https://{URL}/pl/oferty/{self.dealType}/{self.propertyType}/{self.city}?limit={amount_per_page}&page={page}'
            request_info = request.Request(url, headers=HEADERS)
            requested_html = request.urlopen(request_info)
            soup = BeautifulSoup(requested_html, features='html.parser')
            property_list = soup.find_all('li', {"class": "css-x9km8e es62z2j27"})
            for property in property_list:
                property_dict = {}
                try:
                    price_per_sqaure = property.find_all('strong')[0].string
                    price = property.find_all('p', {'class': 'css-lk61n3 es62z2j16'})[0].string
                    district = property.find_all('span', {'class': 'css-17o293g es62z2j19'})[0].string
                    size = property.find_all('span', {'class': 'css-348r18 es62z2j17'})[1].string
                    rooms = property.find_all('span', {'class': 'css-348r18 es62z2j17'})[0].string.split(' ')[0]
                    info_url =f"https://otodom.pl/{property.find_all('a', href=True)[0]['href']}"
                    
                    property_dict['price'] = price
                    property_dict['price per sqaure'] = price_per_sqaure
                    property_dict['district'] = district
                    property_dict['room'] = rooms
                    property_dict['size'] = size
                    property_dict['url'] = info_url
                    self.data.append(property_dict)
                except:
                    pass
    def search_info(self, url):
        pass
    
        return

    def save_csv(self, file_name):
        data_frame = pd.DataFrame(self.data)
        data_frame.drop_duplicates()
        data_frame.to_csv(file_name)
