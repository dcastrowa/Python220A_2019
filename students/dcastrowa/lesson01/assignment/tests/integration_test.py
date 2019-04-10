""" This is an integration test module """

from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management import main
from inventory_management import market_prices


class ModuleTests(TestCase):

    def test_main(self):
        with patch('builtins.input', lambda value: '1'):
            main.main_menu()
            market_prices.get_latest_price = MagicMock(return_value=1000)

        input_info = [10, 'phone', 230, 'y', 'platinum', 'XL']
        with patch('builtins.input', side_effect=input_info):
            new_item = main.add_new_item()
        self.assertEqual(
            {
                'product_code': 10,
                'description': 'phone',
                'market_price': 1000,
                'rental_price': 230,
                'material': 'platinum',
                'size': 'XL'
            },
            new_item)

        input_info = [11, 'lunchbox', 25, 'n', 'y', 'Lunchies', 5]
        with patch('builtins.input', lambda value: '1'):
            main.main_menu()
            market_prices.get_latest_price = MagicMock(return_value=5)
        with patch('builtins.input', side_effect=input_info):
            new_item = main.add_new_item()
        self.assertEqual(
            {
                'product_code': 11,
                'description': 'lunchbox',
                'market_price': 5,
                'rental_price': 25,
                'brand': 'Lunchies',
                'voltage': 5
            },
            new_item)

        with patch('builtins.input', lambda value: '1'):
            main.main_menu()
            market_prices.get_latest_price = MagicMock(return_value=10)

        input_info = [12, 'camera', 50, 'n', 'n']
        with patch('builtins.input', side_effect=input_info):
            new_item = main.add_new_item()
        self.assertEqual(
            {
                'product_code': 12,
                'description': 'camera',
                'market_price': 10,
                'rental_price': 50
            },
            new_item)

        with patch('builtins.input', lambda value: '2'):
            main.main_menu()

            with patch('builtins.input', lambda value: 10):
                item_dict = main.item_info()[0]
                self.assertDictEqual(
                    {
                        'product_code': 10,
                        'description': 'phone',
                        'market_price': 1000,
                        'rental_price': 230,
                        'material': 'platinum',
                        'size': 'XL'
                    },
                    item_dict)

        with patch('builtins.input', lambda value: '2'):
            main.main_menu()

            with patch('builtins.input', lambda value: 11):
                item_dict = main.item_info()[0]
                self.assertDictEqual(
                    {
                        'product_code': 11,
                        'description': 'lunchbox',
                        'market_price': 5,
                        'rental_price': 25,
                        'brand': 'Lunchies',
                        'voltage': 5
                    },
                    item_dict)

        with patch('builtins.input', lambda value: '2'):
            main.main_menu()

            with patch('builtins.input', lambda value: 12):
                item_dict = main.item_info()[0]
                self.assertDictEqual(
                    {
                        'product_code': 12,
                        'description': 'camera',
                        'market_price': 10,
                        'rental_price': 50
                    },
                    item_dict)

        with patch('builtins.input', lambda value: 'q'):
            main.main_menu()
            self.assertRaises(SystemExit)
