import random

import requests
from bs4 import BeautifulSoup
import time
from get_latitude_longtitude import getting_lat_long
from category_dicts import get_dict_for_type, get_dict_for_bld_type, get_dict_furniture, get_dict_repair, \
    get_guest_count, get_house_has_dict
import json
import concurrent.futures
import re
import pprint
import csv
import urllib3
from datetime import datetime
from fake_useragent import UserAgent

urllib3.disable_warnings()

# Dram to USD
AMD_TO_USD = 0.0025
# Proxy lists for parsing
proxies = [
    'https://UX8KfY:05CVG0@217.29.53.133:11771',
    'https://2BHXm7:U0GXqA@217.29.53.70:13307',
    'https://2BHXm7:U0GXqA@217.29.53.64:12143',
    'https://2BHXm7:U0GXqA@217.29.53.64:12144',
    'https://2BHXm7:U0GXqA@217.29.53.64:12145',
]


class SeleniumSetup:
    def __init__(self):

        chrome_options = Options()
        ua = UserAgent()
        chrome_options.add_argument(f'user-agent={ua.random}')

        chrome_options.add_argument('--disable-blink-features')
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    def fetch_html(self, url):
        self.driver.get(url)
        return self.driver.page_source
        try:
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//h1[@itemprop='name']")))
            return self.driver.page_source
        except TimeoutException:
            print(f"Timed out waiting for page to load{url}")
            return None
    def quit_driver(self):
        self.driver.quit()

class ListAmHouseData:
    '''
    Class for getting all data from List.am
    '''
    cookies = {
        '__stripe_mid': 'b455a402-4c15-473b-80ff-0770047fe1bcdcc265',
        '_gid': 'GA1.2.1698014694.1708345634',
        'lang': '2',
        'cf_clearance': '9X6JiPKl.yFNVTWUWgdCucvKtN5D7Sy7Y3AR60.q7E8-1708423596-1.0-Aeu/0z7RgiE0w2rU4gkoXo+bIEbQdMmmrochC79oIVEntG0h45OgggSU725iScQHUvV1fEDG7QuF57B7xvcN9Xk=',
        'u': '00076wz6388a79dd0207594ecfffc01a3ab2606654bcf888411cdbf',
        '_gat': '1',
        '_ga_KVLP4BC4K8': 'GS1.1.1708701844.15.1.1708701929.0.0.0',
        '_ga': 'GA1.1.1736374402.1708001971',
    }

    headers = {
        'authority': 'www.list.am',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': '__stripe_mid=b455a402-4c15-473b-80ff-0770047fe1bcdcc265; _gid=GA1.2.1698014694.1708345634; lang=2; cf_clearance=9X6JiPKl.yFNVTWUWgdCucvKtN5D7Sy7Y3AR60.q7E8-1708423596-1.0-Aeu/0z7RgiE0w2rU4gkoXo+bIEbQdMmmrochC79oIVEntG0h45OgggSU725iScQHUvV1fEDG7QuF57B7xvcN9Xk=; u=00076wz6388a79dd0207594ecfffc01a3ab2606654bcf888411cdbf; _gat=1; _ga_KVLP4BC4K8=GS1.1.1708701844.15.1.1708701929.0.0.0; _ga=GA1.1.1736374402.1708001971',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"121.0.6167.187"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Google Chrome";v="121.0.6167.187", "Chromium";v="121.0.6167.187"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()

    def __house_data_links_for_parce_by_category(self, category, page_count, time_to_repeat):
        '''
        Retrieve list of links for parsing per category from list.am

        :param category: Category ID from list.am
        :param page_count: Amount of pages per category
        :param time_to_repeat: Time to repeat (for increasing search result)
        :return: List of links (as strings) for parsing per category
        '''
        links_to_parse = []
        for _ in range(time_to_repeat):
            i = 1
            while i <= page_count:
                proxy = random.choice(proxies)
                response = requests.get(f'https://www.list.am/category/{category}/{i}', cookies=self.cookies,
                                        headers=self.headers, verify=False, proxies={'http': proxy})
                soup = BeautifulSoup(response.text, features="lxml")
                links = soup.find_all('a')
                print(f"{category} - {i}")
                for link in links:
                    href = link.get('href')
                    if href and href.startswith('/item/'):
                        links_to_parse.append(f"https://www.list.am{href}")
                i += 1
        return links_to_parse

    def house_data_links_json(self, time_to_repeat):
        category_names = {
            60: "apartments-sale",
            62: "houses-sale",
            63: "houses-rent",
            173: "garages-parking-slots-sale",
            212: "rooms-rent",
            267: "event-venues",
            58: "tnak-krpak-rent",
            56: "apartments-long_term-rent",
            59: "commercial-estate-offices-rent",
            199: "commercial-estate-sale",
            268: "new-apartments-sale",
            175: "garages-parking-slots-rent",
            275: "rooms-daily-rent",
            55: "land-sale",
            166: "daily-apartments-rent",
            222: "daily-house-rent",
            61: "tnak-krpak-sale",
            269: "new-houses-sale",
            270: "land-rent"
        }

        # Define a function to fetch links for a given category
        def __fetch_links(category, page_count):
            return self.__house_data_links_for_parce_by_category(category, page_count, time_to_repeat)

        # List of categories and page counts
        categories = [
            (60, 250), (62, 167), (63, 68), (173, 12), (212, 6),
            (267, 3), (58, 2), (56, 250), (59, 85), (199, 58),
            (268, 9), (175, 4), (275, 3), (55, 175), (166, 79),
            (222, 33), (61, 7), (269, 3), (270, 3)
        ]

        # Dictionary to hold the results
        data = {}

        # Execute the function concurrently for each category
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(__fetch_links, category, page_count): category for category, page_count in
                       categories}
            for future in concurrent.futures.as_completed(futures):
                category_id = futures[future]
                category_name = category_names[category_id]
                links = future.result()
                data[category_name] = list(set(links))

        # Write data to JSON file
        json_data = json.dumps(data, indent=4)
        with open("../Data/house_data_links.json", "w") as json_file:
            json_file.write(json_data)

        return json_data

    def parse_link(self, category_to_parse):
        with open("../Data/house_data_links.json", "r") as json_file:
            data = json.load(json_file)

        parsed_data = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.__fetch_and_parse_links, category_to_parse, data[category_to_parse])]
            for future in concurrent.futures.as_completed(futures):
                parsed_data.extend(future.result())

        csv_filename = f"../Data/{category_to_parse}.csv"

        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=parsed_data[0].keys())
            writer.writeheader()
            writer.writerows(parsed_data)

        return csv_filename

    def __fetch_and_parse_links(self, category, links):
        parsed_data = []
        for link in links:
            parsed_data.append(self.__fetch_and_parse_link(link, category))
        return parsed_data

    def __fetch_and_parse_link(self, link, category):
        '''
        Parsing data for link
        :param link: Link of data from list.am
        :param category: category from house_data_links.json file
        :return: parsed data sorted by categories
        '''

        self.headers['user-agent'] = self.ua.random
        try:
            proxy = random.choice(proxies)
            response = self.session.get(link, headers=self.headers, proxies={'http': proxy})
        except requests.exceptions.ProxyError as e:
            print(f"Proxy Error: {e}")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            return None
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.find('h1', itemprop='name')
        # Title for data
        TitleContent = title.text if title else None
        # Address of data
        AddressDiv = soup.find('div', class_='loc')
        AddressContent = AddressDiv.find('a').text if AddressDiv and AddressDiv.find('a') else None
        # Category for data
        if 'new' in category:
            CategoryTitle = "inprocess"
        elif category == 'event-venues' or "daily" in category:
            CategoryTitle = "dailyrent"
        elif 'sale' in category:
            CategoryTitle = 'sale'
        else:
            CategoryTitle = 'rent'

        coordinates = getting_lat_long(link.split("/")[-1])
        # Latitude longitude for data
        Latitude, Longitude = coordinates if coordinates else (None, None)

        price = soup.find('span', class_='price x')
        PriceContent = int(float(price['content']) // 1) if price else None
        price_currency = price.meta['content'] if price and price.meta else None
        # Price for data USD
        if PriceContent and price_currency == "AMD":
            PriceContent = PriceContent * AMD_TO_USD

        # Agency checking
        agency_d = soup.find_all('span', class_='clabel')
        AgencyContent = False
        if agency_d:
            for agency in agency_d:
                if agency.text == 'Գործակալություն':
                    AgencyContent = True

        # Description
        desc = soup.find('div', class_='body')
        DescriptionContent = desc.text if desc else None

        attrs = soup.find_all('div', class_='attr g')
        all_attributes = {}
        for attr in attrs:
            attributes = attr.find_all('div', class_='c')
            for attribute in attributes:
                all_attributes[attribute.find('div', class_='t').text] = attribute.find('div', class_='i').text
        # Parsing attributes
        (TotalArea, LandArea, Type, BuildingType, Elevator, FloorCount,
         RoomCount, BathroomCount, NewBuilded, FurnitureInfo, GarageInfo,
         RepairInfo, BalconyInfo, Floor, LocFromStreet, ExteriorDecoration,
         GuestCount, ChilderInfo, AnimalInfo, EveningNoise, UtilityPayments, PrePayment) = (
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None)

        (playground, doorman, domophone, covered_parking, othdoor_parkin, garage_tf) = (
            False, False, False, False, False, False)
        # Things that house has
        HouseHas = []
        for item in all_attributes.keys():
            if item == 'Ընդհանուր մակերես':
                TotalArea = int(all_attributes[item].replace(',', '').split(' ')[0])
            elif item == 'Սենյակի մակերեսը':
                TotalArea = int(all_attributes[item].replace(',', '').split(' ')[0])
            elif item == 'Հողատարածքի մակերեսը':
                LandArea = int(all_attributes[item].replace(',', '').split(' ')[0])
            elif item == 'Տեսակ':
                Type = get_dict_for_type(all_attributes[item])
            elif item == 'Շինության տիպ':
                BuildingType = get_dict_for_bld_type(all_attributes[item])
            elif item == 'Վերելակ':
                Elevator = True if all_attributes[item] == 'Առկա է' else False
            elif item == 'Հարկերի քանակ':
                if '+' in all_attributes[item]:
                    FloorCount = int(all_attributes[item].split("+")[0])
                else:
                    FloorCount = int(all_attributes[item])
            elif item == 'Սենյակների քանակ':
                if '+' in all_attributes[item]:
                    RoomCount = int(all_attributes[item].split("+")[0])
                else:
                    RoomCount = int(all_attributes[item])
            elif item == 'Սանհանգույցների քանակ':
                if all_attributes[item] == '1':
                    BathroomCount = 1
                elif all_attributes[item] == '2':
                    BathroomCount = 2
                else:
                    BathroomCount = 3
            elif item == 'Նորակառույց':
                if all_attributes[item] == 'Այո':
                    NewBuilded = True
                else:
                    NewBuilded = False
            elif item == 'Կահույք':
                FurnitureInfo = get_dict_furniture(all_attributes[item])
            elif item == 'Ավտոտնակ':
                if all_attributes[item] == '1 տեղ':
                    GarageInfo = 1
                elif all_attributes[item] == '2 տեղ':
                    GarageInfo = 2
                elif all_attributes[item] == 'Առկա չէ':
                    GarageInfo = None
                else:
                    GarageInfo = 3
            elif item == 'Վերանորոգում':
                RepairInfo = get_dict_repair(all_attributes[item])

            elif item == 'Պատշգամբ':
                if all_attributes[item] == 'Բաց պատշգամբ':
                    BalconyInfo = 'open'
                elif all_attributes[item] == 'Փակ պատշգամբ':
                    BalconyInfo = 'close'
                else:
                    BalconyInfo = 'notavailable'
            elif item == 'Հարկ':
                if "+" in all_attributes[item]:
                    Floor = int(all_attributes[item].split("+")[0])
                else:
                    Floor = int(all_attributes[item])
            elif item == 'Գտնվելու վայրը փողոցից':
                if all_attributes[item] == 'Առաջին գիծ':
                    LocFromStreet = 1
                elif all_attributes[item] == 'Երկրորդ գիծ':
                    LocFromStreet = 2
            elif item == 'Արտաքին հարդարում':
                if all_attributes[item] == 'Մետաղ':
                    ExteriorDecoration = 'metal'
                elif all_attributes[item] == 'Փայտ':
                    ExteriorDecoration = 'wood'
            elif item == 'Հյուրերի քանակ':
                GuestCount = get_guest_count(all_attributes[item])

            # Checkbox Parsing
            elif item == 'Առկա են':
                if 'Դոմոֆոն' in all_attributes[item]:
                    domophone = True
                if 'Դռնապահ' in all_attributes[item]:
                    doorman = True
                if 'Խաղահրապարակ' in all_attributes[item]:
                    playground = True
            elif item == 'Կայանատեղի':
                if 'Բացօթյա կայանատեղի' in all_attributes[item]:
                    othdoor_parkin = True
                if 'Ծածկապատ կայանատեղի' in all_attributes[item]:
                    covered_parking = True
                if 'Ավտոտնակ' in all_attributes[item]:
                    garage_tf = True
            elif item == 'Հարմարություններ' or item == 'Կենցաղային տեխնիկա' or item == 'Կոմունալ ծառայություններ' or item == 'Կոմֆորտ' \
                    or item == 'Սարքավորումներ' or item == 'Կոմունիկացիաներ':
                HouseHas.extend(get_house_has_dict(all_attributes[item].split(',')))

            elif item == 'Կարելի է երեխաների հետ':
                if all_attributes[item] == 'Այո':
                    ChilderInfo = 'allowed'
                elif all_attributes[item] == 'Ոչ':
                    ChilderInfo = 'notallowed'
                else:
                    ChilderInfo = 'agreement'
            elif item == 'Թույլատրվում են ընտանի կենդանիներ':
                if all_attributes[item] == 'Այո':
                    AnimalInfo = 'allowed'
                elif all_attributes[item] == 'Ոչ':
                    AnimalInfo = 'notallowed'
                else:
                    AnimalInfo = 'agreement'
            elif item == 'Երեկոյան հնարավոր է աղմկել':
                if all_attributes[item] == 'Այո':
                    EveningNoise = 'allowed'
                else:
                    EveningNoise = 'notallowed'
            elif item == 'Կոմունալ վճարումներ':
                if all_attributes[item] == 'Ներառված':
                    UtilityPayments = 'included'
                elif all_attributes[item] == 'Չներառված':
                    UtilityPayments = 'notincluded'
                else:
                    UtilityPayments = 'agreeement'
            elif item == 'Կանխավճար':
                if all_attributes[item] == 'Առանց կանխավճարի':
                    PrePayment = False
                else:
                    PrePayment = True

        return {
            'link': link,  # Link of the item
            'category': CategoryTitle,  # Category(rent,sale,inprocess,dailyrent)
            'category_from_list': category,  # Category from house_data_links.json
            'title': TitleContent,  # Title of item
            'address': AddressContent,  # Address of item
            'price': PriceContent,  # Price of item in USD
            'agency': AgencyContent,  # Agency(True,False)
            'longtitude': Longitude,  # Longtitude of item
            'latitude': Latitude,  # Latitude of item
            'area': TotalArea,  # Total area
            'landarea': LandArea,  # Area of land
            'purpose': Type,  # Type for what porpose
            'buildingtype': BuildingType,  # Type of building
            'elevator': Elevator,  # (True, False, None)
            'floorcount': FloorCount,  # Number of floors
            'roomcount': RoomCount,  # Number of rooms
            'bathroomcount': BathroomCount,  # Number of bathrooms
            'newbuilded': NewBuilded,  # Is building newbuilded or no
            'furniture': FurnitureInfo,  # Info about furniture
            'garagecount': GarageInfo,  # Info about Garage count
            'repairstatus': RepairInfo,  # Info about repair status of item
            'balcony': BalconyInfo,  # Info about balcony (Open,closed,none,noaviailable)
            'guests': GuestCount,  # Number of guests per location
            'domophone': domophone,  # (T/F)
            'doorman': doorman,  # (T/F)
            'playground': playground,  # (T/F)
            'coveredparking': covered_parking,  # (T/F)
            'outdoorparking': othdoor_parkin,  # (T/F)
            'garage_tr_fl': garage_tf,  # (T/F)
            'househas': HouseHas,  # List of items that house has
            'childer': ChilderInfo,  # (Allowed,NotAllowed,ByAgreement)
            'animal': AnimalInfo,  # (Allowed,NotAllowed,ByAgreement)
            'utilitypayment': UtilityPayments,  # Info about Utility Payments
            'prepayment': PrePayment,  # Info about pre payment
            'description': DescriptionContent,  # Description added by user
        }


if __name__ == "__main__":
    house = ListAmHouseData()

