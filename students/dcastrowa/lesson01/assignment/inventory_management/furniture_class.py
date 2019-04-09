'''
Furniture class
'''

from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    '''
    Furniture inventory
    '''

    def __init__(self, product_code, description, market_price,
                 rental_price, material, size):
        '''
        # Creates common instance variables from the parent class
        :param product_code:
        :param description:
        :param market_price:
        :param rental_price:
        :param material:
        :param size:
        '''

        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        '''
        produces dictionary of fields
        :return:
        '''
        output_dict = super().return_as_dictionary()
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
