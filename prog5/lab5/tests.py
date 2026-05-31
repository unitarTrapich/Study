import unittest
from unittest.mock import patch
from io import BytesIO
import xmltodict
from currency_class import CurrenciesLst


class TestCurrenciesLst(unittest.TestCase):
    
    # Тест на некорректный код валюты
    @patch('requests.get')
    def test_invalid_currency_code(self, mock_get):
        # XML с двумя элементами Valute, чтобы гарантировать список
        mock_response = """
        <ValCurs Date="16.11.2024" name="Foreign Currency Market">
            <Valute ID="R9999">
                <CharCode>XYZ</CharCode>
                <Name>Неправильная валюта</Name>
                <VunitRate>None</VunitRate>
            </Valute>
            <Valute ID="R01010">
                <CharCode>AUD</CharCode>
                <Name>Австралийский доллар</Name>
                <VunitRate>64,6581</VunitRate>
            </Valute>
        </ValCurs>
        """
        mock_get.return_value.__enter__.return_value.content = mock_response

        currencies = CurrenciesLst(time_reset=0)  # Создаем объект класса
        result = currencies.getter()  # Вызываем метод

        # Проверка результатов
        expected_output = [
            {'XYZ': ('Неправильная валюта', ['None'])},
            {'AUD': ('Австралийский доллар', ['64', '6581'])}
        ]

        self.assertEqual(currencies.formated_dict, expected_output)ы

    # Тест на корректный ID валюты: проверка диапазона курса
    @patch('requests.get')
    def test_valid_currency_values(self, mock_get):
        mock_response = """
        <ValCurs Date="16.11.2024" name="Foreign Currency Market">
            <Valute ID="R01010">
                <CharCode>USD</CharCode>
                <Name>Доллар США</Name>
                <VunitRate>75,1234</VunitRate>
            </Valute>
            <Valute ID="R01020">
                <CharCode>EUR</CharCode>
                <Name>Евро</Name>
                <VunitRate>85,5678</VunitRate>
            </Valute>
        </ValCurs>
        """
        mock_get.return_value.__enter__.return_value.content = mock_response
        currencies = CurrenciesLst(time_reset=0)
        currencies.getter()

        # Проверяем наличие валюты и диапазон значений
        for currency in currencies.formated_dict:
            for code, (name, value) in currency.items():
                self.assertIn(code, ['USD', 'EUR'])
                self.assertIn(name, ['Доллар США', 'Евро'])
                combined_value = float(f"{value[0]}.{value[1]}")
                self.assertTrue(0 <= combined_value <= 999)


unittest.main()