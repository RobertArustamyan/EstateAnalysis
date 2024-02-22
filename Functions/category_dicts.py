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
    if item:
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
    if item:
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
    if item:
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
    if item:
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
    if item:
        return item_dict[item]
    else:
        return item_dict