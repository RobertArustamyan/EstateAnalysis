def get_dict_for_type(item):
    '''
    Used in main.py for finding type
    :param item: name in armenan
    :return: type in english
    '''
    item_dict =  {
        'Տուն' : 'house',
        'Թաունհաուզ': 'townhouse',
        'Ամառանոց' : 'summerhouse',
        'Բնակարան': 'apartment',
        'Սեփական տուն': 'ownhouse',
        'Հյուրանոց': 'hotel',
        'Հյուրատուն': 'guesthouse',
        'Հոսթել': 'hostel',
        'Հանրակացարան': 'dormitory',
        'Գրասենյակային տարածք': 'officearea',
        'Առևտրային տարածք': 'commercialarea',
        'Արտադրական տարածք': 'productionarea',
        'Պահեստ': 'warehouse',
        'Ռեստորան': 'therestaurant',
        'Ավտոսպասարկում': 'carservice',
        'Գործող բիզնես': 'operatingbusiness',
        'Շենք': 'building',
        'Հյուրանոց': 'hotel',
        'Բազմաֆունկցիոնալ գույք': 'multipurposeproperty',
        'Գյուղատնտեսական գույք': 'agriculturalproperty',
        'Այլ': 'other',
        'Գյուղատնտեսական': 'agricultural',
        'Բնակելի շինությունների համար': 'residentialbuildings',
        'Արդյունաբերական օգտագործման': 'industrialuse',
        'Հասարակական շինությունների համար': 'publicbuildings',
        'Ընդհանուր օգտագործման': 'generaluse',
        'Ավտոտնակ' : 'garage',
        'Ավտոկայանատեղի' : 'parkinglot'
    }
    return item_dict[item]