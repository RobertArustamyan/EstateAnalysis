import requests
import re


def getting_lat_long(id: int):
    '''
    Retrieves the latitude and longitude values associated with a given ID from a web page on list.am.

    :param id: The ID of the item for which latitude and longitude are to be retrieved.
    :return: A list containing the latitude and longitude values [latitude, longitude], or None if the values cannot be found in the response.
    '''
    params = {'i': id}
    cookies = {
        'lang': '0',
        '__stripe_mid': 'b455a402-4c15-473b-80ff-0770047fe1bcdcc265',
        '_gid': 'GA1.2.1698014694.1708345634',
        '__stripe_sid': 'ae480c2d-5f8e-4556-a616-1d3fb2870f249dd314',
        '_ga_KVLP4BC4K8': 'GS1.1.1708368084.4.1.1708368357.0.0.0',
        '_ga': 'GA1.2.1736374402.1708001971',
    }
    headers = {
        'authority': 'www.list.am',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': 'lang=0; __stripe_mid=b455a402-4c15-473b-80ff-0770047fe1bcdcc265; _gid=GA1.2.1698014694.1708345634; __stripe_sid=ae480c2d-5f8e-4556-a616-1d3fb2870f249dd314; _ga_KVLP4BC4K8=GS1.1.1708368084.4.1.1708368357.0.0.0; _ga=GA1.2.1736374402.1708001971',
        'referer': 'https://www.list.am/en/item/20269258',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    response = requests.get('https://www.list.am/rtac', params=params, cookies=cookies, headers=headers)
    match = re.search(r'amap\.init\(\[([\d\.,]+)\]', response.text)
    if match:
        lat_long_str = match.group(1)
        lat_long = [float(coord) for coord in lat_long_str.split(',')]
        return lat_long[:2]
    else:
        print(f"Latitude and longitude not found in {id}")
        return None


if __name__ == "__main__":
    #TEST CASE
    print(getting_lat_long(19293046))
