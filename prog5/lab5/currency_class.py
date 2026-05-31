import requests
import xmltodict
import matplotlib.pyplot as pplt
import os
import time

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    

class CurrenciesLst(metaclass = Singleton):
    
    def __init__(self, time_reset = 10):
        self.formated_dict = []
        self.currencies = []
        self.time_reset = time_reset
        self.request_time = 0
    


    # Получение курсов валют и их предобработка
    def getter(self):
        if (time.time() - self.request_time) <= self.time_reset:                    # проверка кулдауна запросов
            raise Exception(f"Не более одного запроса в {self.time_reset} сек.")    # ошибка проверки
        
        self.request_time = time.time()
        with(
            requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        ) as f:
            fdict = xmltodict.parse(f.content) # Используем xmltodict.parse для перевода xml в dict
            self.formated_dict = [
                {currency.get('CharCode') : (currency.get("Name"), (currency.get("VunitRate").split(',')))} # Берем VunitRate а не Value, чтобы не мучаться с номиналом, разьеденяем целую и дробную часть с помощью split
                for currency in fdict['ValCurs']['Valute']
                ]
            
            formatted_output = "[\n" + ",\n ".join(str(item) for item in self.formated_dict) + "\n]" # чтобы красиво как в тз
            return(formatted_output)
        


    # Задача нужных валют для дальнейшей обработки
    def setter(self, currencies):
        self.currencies = currencies
        return(self.currencies)


    # Визуализация на графике
    def visualiser(self):
        
        x_value = []
        y_value = []

        for currency in self.formated_dict:
            for code, (_, value) in currency.items():
                if code in self.currencies:                        # отсеивание нужных валют
                    x_value.append(code)
                    y_value.append(float(f"{value[0]}.{value[1]}")) # соединение чисел в флоат

        pplt.bar(x_value, y_value)
        pplt.title('Курсы валют по отношению к рублю')
        pplt.xlabel('Валюта')
        pplt.ylabel('Курс')
        file_path = os.path.join(os.path.dirname(__file__), 'currencies.jpg')
        pplt.savefig(file_path)
        pplt.show