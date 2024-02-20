import requests
from bs4 import BeautifulSoup
import time
from Functions.get_latitude_longtitude import getting_lat_long

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

    def house_data_by_category(self, category, page_count, time_to_repeat):
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


if __name__ == "__main__":

    house = ListAmHouseData()
    # Bnakaranneri Vacharq
    links_to_parse1 = house.house_data_by_category(60, 250, 3)
    # Tneri vacharq
    links_to_parse2 = house.house_data_by_category(62, 167, 3)
    # Tneri vardzakalutyun
    links_to_parse3 = house.house_data_by_category(63, 68, 3)
    # Avtotnakneri ev avtokayanaterxineri vacharq
    links_to_parse4 = house.house_data_by_category(173, 12, 3)
    # Vardzov senyakner
    links_to_parse5 = house.house_data_by_category(212, 6, 3)
    # Mijocarumneri anckacman vayrer
    links_to_parse6 = house.house_data_by_category(267, 3, 3)
    # Tnakneri ev krpakneri vardzakalutyun
    links_to_parse7 = house.house_data_by_category(58, 2, 3)
    # Bnakaranneri erkarajamket vardzakalutyun
    links_to_parse8 = house.house_data_by_category(56, 250, 3)
    # Komercion ansharj guyqi ev grasenyakneri vardzakalutyun
    links_to_parse9 = house.house_data_by_category(59, 85, 3)
    # Komericon ansharj guyqi vacharq
    links_to_parse10 = house.house_data_by_category(199, 58, 3)
    # Nor bnakaranneri vacharq
    links_to_parse11 = house.house_data_by_category(268, 9, 3)
    # Avtotnakneri ev avtokayanatexineri vardzakalutyun
    links_to_parse12 = house.house_data_by_category(175, 4, 3)
    # Oravardzov senyakner
    links_to_parse13 = house.house_data_by_category(275, 3, 3)
    # Hoxataracqneri vacharq
    links_to_parse14 = house.house_data_by_category(55, 175, 3)
    #Oravardzov bnakaranner
    links_to_parse15 = house.house_data_by_category(166, 79, 3)
    #Oravardzov tner
    links_to_parse16 = house.house_data_by_category(222, 33, 3)
    #Tnakneri ev krpakneri vacharq
    links_to_parse17 = house.house_data_by_category(61, 7, 3)
    #Norakaruyc tneri vacharq
    links_to_parse18 = house.house_data_by_category(269, 3, 3)
    #Hoxataracqneri vardzakalutyun
    links_to_parse19 = house.house_data_by_category(270, 3, 3)




