import requests
from xml.etree import ElementTree as ET
import json
import csv
import io

class Component:
    def fetch(self):
        raise NotImplementedError("Метод fetch должен быть переопределен")



class CurrenciesList(Component):
    """Получение данных с цб"""
    def fetch(self):
        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.content)
        currencies = {}
        for valute in root.findall('Valute'):
            charcode = valute.find('CharCode').text
            name = valute.find('Name').text
            value = float(valute.find('Value').text.replace(',', '.'))
            nominal = int(valute.find('Nominal').text)
            currencies[charcode] = {'name': name, 'value': value, 'nominal': nominal}
        return currencies

# Базовый декоратор
class Decorator(Component):
    def __init__(self, component):
        self._component = component

    def fetch(self):
        return self._component.fetch()

class DecoratorFormatted(Decorator):
    """Декоратор формата лр5"""
    def fetch(self):
        data = self._component.fetch()
        result = []
        for charcode, details in data.items():
            result.append({charcode: (details['name'], f"{details['value']:.4f}")})
        return "\n".join(map(str, result))

class DecoratorJSON(Decorator):
    """Декоратор формата JSON"""
    def fetch(self):
        data = self._component.fetch()
        return json.dumps(data, indent=4, ensure_ascii=False)

class DecoratorCSV(Decorator):
    """Декоратор формата CSV"""
    def fetch(self):
        data = self._component.fetch()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['CharCode', 'Name', 'Value', 'Nominal'])
        for charcode, details in data.items():
            writer.writerow([charcode, details['name'], details['value'], details['nominal']])
        return output.getvalue()



if __name__ == "__main__":
    # Объект базового класса
    currencies = CurrenciesList()

    print("Данные в виде словаря:")
    print(currencies.fetch())

    # Формат лр5
    formatted = DecoratorFormatted(currencies)
    print("\nДанные в  формате лр5:")
    print(formatted.fetch())

    # JSON
    as_json = DecoratorJSON(currencies)
    print("\nДанные в формате JSON:")
    print(as_json.fetch())

    # CSV
    as_csv = DecoratorCSV(currencies)
    print("\nДанные в формате CSV:")
    print(as_csv.fetch())
