class Transformer:
    def __init__(self):
        pass

    def transform_btype(self, item: str) -> int:
        '''
        Transform building type.
        This function maps a balcony type string to an integer value.

        :param item:  The building type.
        :return: int The transformed integer value.
        '''
        item_dict = {
            'stone': 3,
            'monolith': 1,
            'panel': 2,
            'brick' : 0,
            'tape' : 4,
            'wooden' : 5,
        }
        return item_dict.get(item)

    def transform_reptype(self, item: str) -> int:
        '''
        Transform repair type.
        This function maps a balcony type string to an integer value.

        :param item:  The repair type.
        :return: int The transformed integer value.
        '''
        item_dict = {
            'capital-reconstructed': 0,
            'unrepaired': 6,
            'designer-style': 2,
            'euro': 3,
            'cosmetic' : 1,
            'oldrepair' : 4,
            'partical' : 5,
        }
        return item_dict.get(item)

    def transform_baltype(self, item: str) -> int:
        '''
        Transform balcony type.
        This function maps a balcony type string to an integer value.

        :param item:  The Balcony type.
        :return: int The transformed integer value.
        '''
        item_dict = {
            'notavailable': 1,
            'open': 2,
            'close': 0,
        }
        return item_dict.get(item)

    def transform_booltype(self, item: bool) -> int:
        '''
        Transform Boolean type.
        This function maps a boolean value representing the presence of a garden to an integer value.
        :param item: Bool value
        :return: int The transformed integer value.
        '''
        item_dict = {
            False: 0,
            True: 1,
        }
        return item_dict.get(item)

