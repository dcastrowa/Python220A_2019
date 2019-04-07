'''
Inventory class
'''


class Inventory:
    '''
    parent inventory class
    '''

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        '''
        produces a dictionary of fields
        :return: dictionary of fields
        '''
        output_dict = {
            'product_code': self.product_code,
            'description': self.description,
            'market_price': self.market_price,
            'rental_price': self.rental_price,
        }

        return output_dict
