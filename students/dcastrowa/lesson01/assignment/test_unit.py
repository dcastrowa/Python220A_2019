from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management import market_prices
from inventory_management import main


class InventoryTests(TestCase):

    def test_return_as_dictionary(self):

        chair = Inventory(1, 'brown', 25, 30)

        test_dictionary = {
            'product_code': 1,
            'description': 'brown',
            'market_price': 25,
            'rental_price': 30
        }

        for key, value in test_dictionary.items():
            self.assertEqual(test_dictionary[f'{key}'],
                             chair.return_as_dictionary()[f'{key}'])

        self.assertEqual(dict, type(chair.return_as_dictionary()))


class ElectricAppliancesTests(TestCase):

    def test_return_as_dictionary(self):
        stove = ElectricAppliances(2, 'black', 200, 100, 'Steve Stoves', 55)

        test_dictionary = {
            'product_code': 2,
            'description': 'black',
            'market_price': 200,
            'rental_price': 100,
            'brand': 'Steve Stoves',
            'voltage': 55
        }

        for key, value in test_dictionary.items():
            self.assertEqual(test_dictionary[f'{key}'],
                             stove.return_as_dictionary()[f'{key}'])

        self.assertEqual(dict, type(stove.return_as_dictionary()))


class FurnitureTests(TestCase):

    def test_return_as_dictionary(self):

        couch = Furniture(3, 'comfy', 500, 600, 'leather', 'M')

        test_dictionary = {
            'product_code': 3,
            'description': 'comfy',
            'market_price': 500,
            'rental_price': 600,
            'material': 'leather',
            'size': 'M'
        }

        for key, value in test_dictionary.items():
            self.assertEqual(value, couch.return_as_dictionary()[f'{key}'])

        self.assertEqual(dict, type(couch.return_as_dictionary()))


class MarketPricesTests(TestCase):

    def test_get_latest_price(self):

        latest_price = market_prices.get_latest_price()

        self.assertEqual(24, latest_price)


class MainTests(TestCase):

    def test_add_item(self):

        input_info = [2, 'chair', 20, 'n', 'n']
        with patch('builtins.input', side_effect=input_info):
            new_item = main.add_new_item()
        self.assertEqual({
                'product_code': 2,
                'description': 'chair',
                'market_price': 24,
                'rental_price': 20,
        }, new_item)

    def test_add_furniture_item(self):

        input_info = [3, 'couch', 250, 'y', 'leather', 'L']
        with patch('builtins.input', side_effect=input_info):
            new_furniture = main.add_new_item()
        self.assertEqual({
            'product_code': 3,
            'description': 'couch',
            'market_price': 24,
            'rental_price': 250,
            'material': 'leather',
            'size': 'L'
        }, new_furniture)

    def test_add_electric_appliance_item(self):
        input_info = [4, 'stove', 500, 'n', 'y', 'Steve Stoves', 55]
        with patch('builtins.input', side_effect=input_info):
            new_electric_appliance = main.add_new_item()
        self.assertEqual({
            'product_code': 4,
            'description': 'stove',
            'market_price': 24,
            'rental_price': 500,
            'brand': 'Steve Stoves',
            'voltage': 55
        }, new_electric_appliance)

    def test_get_info(self):
        input_info = [1, 'computer', 1200, 'n', 'y', 'Apple', 300]
        with patch('builtins.input', side_effect=input_info):
            main.add_new_item()
        with patch('builtins.input', lambda value: 1):
            item_dict = main.item_info()[0]
            self.assertDictEqual(
                {
                    'product_code': 1,
                    'description': 'computer',
                    'market_price': 24,
                    'rental_price': 1200,
                    'brand': 'Apple',
                    'voltage': 300
                },
                item_dict)
        with patch('builtins.input', lambda value: 0):
            not_found = main.item_info()
            self.assertEqual(
                "Item not found in inventory", not_found)

    def test_get_price(self):

        input_info = [2, 'stove', 1000, 'n', 'y', 'Steve Stoves', 220]
        with patch('builtins.input', side_effect=input_info):
            main.add_new_item()
        price = main.get_price(2)
        self.assertEqual(price, 1000)

    def test_main_menu_add(self):
        with patch('builtins.input', lambda value: '1'):
            sel = main.main_menu()
            self.assertEqual(sel.__name__, 'add_new_item')

    def test_main_menu_get(self):
        with patch('builtins.input', lambda value: '2'):
            sel = main.main_menu()
            self.assertEqual(sel.__name__, 'item_info')

    def test_main_menu_quit(self):
        with patch('builtins.input', lambda value: 'q'):
            main.main_menu()
        self.assertRaises(SystemExit)


if __name__ == '__main__':
    unittest.main()
