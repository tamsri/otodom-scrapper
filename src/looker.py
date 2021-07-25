from urllib import request
from enum import Enum
from numpy import string_
import pandas as pd 
import re
from math import floor
from bs4 import BeautifulSoup
from datetime import datetime

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
                propertyType: PropertyType, postAfter: str, postBefore: str, maxSearch: int = -1 ):
        self.city = city
        self.dealType = 'sprzedaz' if dealType == DealType.BUY else 'wynajem'
        self.propertyType = 'dom' if propertyType == PropertyType.DOM else 'mieszkanie'
        self.maxSearch = maxSearch if maxSearch >= 0 else 9999999
        self.data = []
        self.dataFrame = None

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
                    info_url =f"https://www.otodom.pl{property.find_all('a', href=True)[0]['href']}"
                    
                    property_dict['price'] = price
                    property_dict['price per sqaure'] = price_per_sqaure
                    property_dict['district'] = district
                    property_dict['room'] = rooms
                    property_dict['size'] = size
                    
                    property_info = self.search_info(info_url)
                    info_params = ['rynek', 'piętro', 'rok', 'zabudowy', 'balkon', 'when']
                    for param in info_params:
                        if param in property_info:
                            property_dict[param] = property_info[param]
                    property_dict['url'] = info_url
                    self.data.append(property_dict)
                except Exception as e:
                    print(e)
        
        self.dataFrame = pd.DataFrame(self.data)
        self.dataFrame.drop_duplicates()

    def search_info(self, url):
        print(f"search info url {url}")
        request_info = request.Request(url)
        requested_html = request.urlopen(request_info)
        soup = BeautifulSoup(requested_html, features='html.parser')
        property_info = {}
        try:
            year_section = soup.find_all('div', {"aria-label": "Rok budowy"})[0]
            year = year_section.find_all('div', {'class': 'css-1ytkscc ev4i3ak0'})[0].string
            property_info['rok'] = year
            print(f'Year: {year}')
        except:
            pass
        
        try:
            floor_section = soup.find_all('div', {"aria-label": "Piętro"})[0]
            floor = floor_section.find_all('div', {'class': 'css-1ytkscc ev4i3ak0'})[0].string
            property_info['piętro'] = floor
            print(f'Floor: {floor}')
        except:
            pass
        
        try:
            hand_section = soup.find_all('div', {"aria-label": "Rynek"})[0]
            hand = hand_section.find_all('div', {'class': 'css-1ytkscc ev4i3ak0'})[0].string
            property_info['rynek'] = hand
        except:
            pass

        try:
            style_section = soup.find_all('div', {"aria-label": "Rodzaj zabudowy"})[0]
            style = style_section.find_all('div', {'class': 'css-1ytkscc ev4i3ak0'})[0].string
            property_info['zabudowy'] = style
        except:
            pass

        additional_info = ['winda', 'balkon']
        additional_section = str(soup.find_all('h3', string='informacje dodatkowe')[0].parent)
        for info in additional_info:
            if info in additional_section:
                property_info[info] = 'tak'
    
        # print(soup.prettify())
        plain = soup.prettify()
        if 'dateModified' in plain:
            cropped = plain.split('dateModified')[1][2:28]
            editTime = re.search('"(.*)","', cropped).group(1).strip()
            print(editTime)
            property_info['when'] = editTime
        return property_info

    def save_csv(self, file_name):
        self.dataFrame.to_csv(file_name)
