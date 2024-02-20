import requests
from bs4 import BeautifulSoup
import time
from Functions.get_latitude_longtitude import getting_lat_long
import json

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

if __name__ == "__main__":
    house = ListAmHouseData()
    house.house_data_links_json(5)
