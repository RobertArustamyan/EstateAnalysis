import requests
from bs4 import BeautifulSoup
import time
from Functions.get_latitude_longtitude import getting_lat_long
from Functions.category_dicts import get_dict_for_type, get_dict_for_bld_type, get_dict_furniture, get_dict_repair, \
    get_guest_count, get_house_has_dict
import json
import concurrent.futures
import re
import pprint

AMD_TO_USD = 0.0025


class ListAmHouseData:
    cookies = {
        '__stripe_mid': 'b455a402-4c15-473b-80ff-0770047fe1bcdcc265',
        '_gid': 'GA1.2.1698014694.1708345634',
        '__stripe_sid': 'ae480c2d-5f8e-4556-a616-1d3fb2870f249dd314',
        'lang': '2',
        '_gat': '1',
        '_ga_KVLP4BC4K8': 'GS1.1.1708368084.4.1.1708370706.0.0.0',
        '_ga': 'GA1.2.1736374402.1708001971',
    }

    headers = {
        'authority': 'www.list.am',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '__stripe_mid=b455a402-4c15-473b-80ff-0770047fe1bcdcc265; _gid=GA1.2.1698014694.1708345634; __stripe_sid=ae480c2d-5f8e-4556-a616-1d3fb2870f249dd314; lang=2; _gat=1; _ga_KVLP4BC4K8=GS1.1.1708368084.4.1.1708370706.0.0.0; _ga=GA1.2.1736374402.1708001971',
        'referer': 'https://www.list.am/category/54',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    def __init__(self):
        self.session = requests.Session()

    def house_data_links_for_parce_by_category(self, category, page_count, time_to_repeat):
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
                response = requests.get(f'https://www.list.am/category/{category}/{i}', cookies=self.cookies,
                                        headers=self.headers)
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
        links_to_parse1 = self.house_data_links_for_parce_by_category(60, 250, time_to_repeat)
        # Tneri vacharq
        links_to_parse2 = self.house_data_links_for_parce_by_category(62, 167, time_to_repeat)
        # Tneri vardzakalutyun
        links_to_parse3 = self.house_data_links_for_parce_by_category(63, 68, time_to_repeat)
        # Avtotnakneri ev avtokayanaterxineri vacharq
        links_to_parse4 = self.house_data_links_for_parce_by_category(173, 12, time_to_repeat)
        # Vardzov senyakner
        links_to_parse5 = self.house_data_links_for_parce_by_category(212, 6, time_to_repeat)
        # Mijocarumneri anckacman vayrer
        links_to_parse6 = self.house_data_links_for_parce_by_category(267, 3, time_to_repeat)
        # Tnakneri ev krpakneri vardzakalutyun
        links_to_parse7 = self.house_data_links_for_parce_by_category(58, 2, time_to_repeat)
        # Bnakaranneri erkarajamket vardzakalutyun
        links_to_parse8 = self.house_data_links_for_parce_by_category(56, 250, time_to_repeat)
        # Komercion ansharj guyqi ev grasenyakneri vardzakalutyun
        links_to_parse9 = self.house_data_links_for_parce_by_category(59, 85, time_to_repeat)
        # Komericon ansharj guyqi vacharq
        links_to_parse10 = self.house_data_links_for_parce_by_category(199, 58, time_to_repeat)
        # Nor bnakaranneri vacharq
        links_to_parse11 = self.house_data_links_for_parce_by_category(268, 9, time_to_repeat)
        # Avtotnakneri ev avtokayanatexineri vardzakalutyun
        links_to_parse12 = self.house_data_links_for_parce_by_category(175, 4, time_to_repeat)
        # Oravardzov senyakner
        links_to_parse13 = self.house_data_links_for_parce_by_category(275, 3, time_to_repeat)
        # Hoxataracqneri vacharq
        links_to_parse14 = self.house_data_links_for_parce_by_category(55, 175, time_to_repeat)
        # Oravardzov bnakaranner
        links_to_parse15 = self.house_data_links_for_parce_by_category(166, 79, time_to_repeat)
        # Oravardzov tner
        links_to_parse16 = self.house_data_links_for_parce_by_category(222, 33, time_to_repeat)
        # Tnakneri ev krpakneri vacharq
        links_to_parse17 = self.house_data_links_for_parce_by_category(61, 7, time_to_repeat)
        # Norakaruyc tneri vacharq
        links_to_parse18 = self.house_data_links_for_parce_by_category(269, 3, time_to_repeat)
        # Hoxataracqneri vardzakalutyun
        links_to_parse19 = self.house_data_links_for_parce_by_category(270, 3, time_to_repeat)

        data = {
            "apartments-sale": list(set(links_to_parse1)),
            "houses-sale": list(set(links_to_parse2)),
            "houses-rent": list(set(links_to_parse3)),
            "garages-parking-slots-sale": list(set(links_to_parse4)),
            "rooms-rent": list(set(links_to_parse5)),
            "event-venues": list(set(links_to_parse6)),
            "tnak-krpak-rent": list(set(links_to_parse7)),
            "apartments-rent-long_term": list(set(links_to_parse8)),
            "commercial-estate-offices-rent": list(set(links_to_parse9)),
            "commercial-estate-sale": list(set(links_to_parse10)),
            "new-apartments-sale": list(set(links_to_parse11)),
            "garages-parking-slots-rent": list(set(links_to_parse12)),
            "rooms-daily-rent": list(set(links_to_parse13)),
            "land-sale": list(set(links_to_parse14)),
            "daily-apartments-rent": list(set(links_to_parse15)),
            "daily-house-rent": list(set(links_to_parse16)),
            "tnak-krpak-sale": list(set(links_to_parse17)),
            "new-houses-sale": list(set(links_to_parse18)),
            "land-rent": list(set(links_to_parse19))
        }
        json_data = json.dumps(data, indent=4)
        with open("Data/house_data_links.json", "w") as json_file:
            json_file.write(json_data)

        return json_data

    def parse_link(self):
        with open("Data/house_data_links.json", "r") as json_file:
            data = json.load(json_file)

        parsed_data = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for category, links in data.items():
                futures.append(executor.submit(self.fetch_and_parse_links, category, links))
            for future in concurrent.futures.as_completed(futures):
                parsed_data.extend(future.result())
        return parsed_data

    def fetch_and_parse_links(self, category, links):
        parsed_data = []
        for link in links:
            parsed_data.append(self.fetch_and_parse_link(link, category))
        return parsed_data

    def fetch_and_parse_link(self, link, category):
        '''
        Parsing data for link
        :param link: Link of data from list.am
        :param category: category from house_data_links.json file
        :return: parsed data sorted by categories
        '''
        response = self.session.get(link, headers=self.headers)

        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.find('h1', itemprop='name')
        # Title for data
        TitleContent = title.text if title else None
        # Address of data
        AddressDiv = soup.find('div', class_='loc')
        AddressContent = AddressDiv.find('a').text if AddressDiv.find('a') else None
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
        PriceContent = int(price['content']) if price else None
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
         GuestCount) = (None, None, None, None, None, None, None, None, None, None, None,
                        None, None, None, None, None, None)

        (playground, doorman, domophone, covered_parking, othdoor_parkin, garage_tf) = (
        False, False, False, False, False, False)
        # Things that house has
        HouseHas = []
        for item in all_attributes.keys():
            if item == 'Ընդհանուր մակերես':
                TotalArea = int(all_attributes[item].split(' ')[0])
            elif item == 'Սենյակի մակերեսը':
                TotalArea = int(all_attributes[item].split(' ')[0])
            elif item == 'Հողատարածքի մակերեսը':
                LandArea = int(all_attributes[item].split(' ')[0])
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
                if int(all_attributes[item]) == 1:
                    BathroomCount = 1
                elif int(all_attributes[item]) == 2:
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
            'description': DescriptionContent,  # Description added by user
        }


if __name__ == "__main__":
    house = ListAmHouseData()
    pprint.pprint(house.fetch_and_parse_link("https://www.list.am/item/19630058", "land-rent")['househas'])
