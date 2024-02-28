def get_dict_for_type(item):
    '''
    Used in main.py for finding type
    :param item: name in armenian
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
    if item and item in item_dict.keys():
        return item_dict[item]
    else:
        return item_dict


def get_dict_for_bld_type(item):
    '''
        Used in main.py for finding type
        :param item: name in armenian
        :return: type in english
        '''
    item_dict = {
        "Քարե" : "stone",
        "Պանելային" : "panel",
        "Մոնոլիտ" : "monolith",
        "Աղյուսե" : "brick",
        "Կասետային" : "tape",
        "Փայտե" : "wooden",
    }
    if item and item in item_dict.keys():
        return item_dict[item]
    else:
        return item_dict

def get_dict_furniture(item):
    item_dict = {
        'Առկա է' : 'available',
        'Առկա չէ' : 'notavailable',
        'Մասնակի կահույք' : 'partly',
        'Համաձայնությամբ' : 'agreement'
    }
    if item and item in item_dict.keys():
        return item_dict[item]
    else:
        return item_dict

def get_dict_repair(item):
    item_dict = {
        'Չվերանորոգված': 'unrepaired',
        'Հին վերանորոգում': 'oldrepair',
        'Մասնակի վերանորոգում': 'partical',
        'Կոսմետիկ վերանորոգում': 'cosmetic',
        'Եվրովերանորոգված': 'euro',
        'Դիզայներական ոճով վերանորոգված': 'designer-style',
        'Կապիտալ վերանորոգված': 'capital-reconstructed'
    }
    if item and item in item_dict.keys():
        return item_dict[item]
    else:
        return item_dict

def get_guest_count(item):
    item_dict = {
        'մինչև 15 անձ' : '<15',
        '15-ից 30 անձ' : '15-30',
        '30-ից 50 անձ' : '30-50',
        '50-ից 100 անձ' : '50-100',
        '100-ից 300 անձ' : '100-300',
        '300-ից 500 անձ': '300-500',
        '500 և ավելի անձ' : '500>'
    }
    if item and item in item_dict.keys():
        return item_dict[item]
    else:
        return item_dict

def get_house_has_dict(items):
    item_dict = {
        'հեռուստացույց' : 'tv',
        'օդորակիչ' : 'conditioner',
        'ինտերնետ' : 'wi-fi',
        'կայանատեղի' : 'parking-lot',
        'սառնարան' : 'refrigerator',
        'սալօջախ' : 'stove',
        'աման լվացող մեքենա' : 'dishwasher',
        'լվացքի մեքենա' : 'washing-machine',
        'ջրատաքացուցիչ' : 'water-heater',
        'լողավազան' : 'swimming-pool',
        'սաունա' : 'sauna',
        'բուխարի' : 'fireplace',
        'խորովածի վառարան' : 'barbecue-oven',
        'բիլիարդ' : 'billiard',
        'տաղավար' : 'pavilion',
        'անվտանգության համակարգ' : 'security-system',
        'էլեկտրականություն' : 'electricity',
        'ջուր' : 'water',
        'ջեռուցում' : 'warming',
        'էլեկտրական մեքենաների լիցքավորիչ' : 'car-charger',
        'ավտոմատ դարպասներ' : 'automatic-gates',
        'տեսահսկում' : 'video-security',
        'սրբիչներ' : 'towels',
        'անկողնային պարագաներ' : 'bedding',
        'հիգիենայի պարագաներ' : 'hygiene-items',
        'խոհանոց': 'kitchen',
        'բար': 'bar',
        'բեմ': 'stage',
        'պարահրապարակ': 'dance-floor',
        'աուդիո համակարգ': 'audio-system',
        'կարաոկե': 'karaoke',
        'պրոյեկտոր': 'projector',
        'խաղային ավտոմատներ': 'gaming-machines',
        'սեղանի խաղեր': 'board-games',
        'էլեկտրականություն': 'electricity',
        'ջրամատակարարում': 'water-supply',
        'գազ': 'gas',
        'կոյուղի': 'sewerage'
    }
    if items:
        res = []
        for item in items:
            it = item.lower().strip()
            if it in item_dict.keys():
                res.append(item_dict[it])
        return res
    return item_dict
