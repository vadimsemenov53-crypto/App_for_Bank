import datetime
import json
from json import JSONDecodeError
from dotenv import load_dotenv
import pandas as pd
import os
import requests

from pandas.core.interchange.dataframe_protocol import DataFrame


path = os.path.dirname(os.path.dirname(__file__))
path_env = os.path.join(path, '.env')
load_dotenv(path_env)

API_KEY_1 = os.getenv('API_KEY_1')
API_KEY_2 = os.getenv('API_KEY_2')

PATH = os.path.dirname(os.path.dirname(__file__))


def get_greeting() -> str:
    """Функция приветствия, в зависимости от текущего времени.
    Выводит приветствие."""
    time = datetime.datetime.now().hour

    if 5 <= time <= 11:
        return "Доброе утро"
    elif 12 <= time <= 16:
        return "Добрый день"
    elif 17 <= time <= 20:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_data_transactions_from_xlsx(path_to_file: str | None = None) -> DataFrame:
    """Функция возвращает данные о транзакциях из файла XLSX,
    Вы можете передать свой, если он не передан то функция выведет данные
    из файла проекта."""
    if  not path_to_file:
        path = os.path.dirname(os.path.dirname(__file__))
        path_to_file = os.path.join(path, 'data/operations.xlsx')

    df = pd.read_excel(path_to_file)

    return df


def get_data_transactions_from_df(dataframe: DataFrame) -> list[dict[str, str | float]]:
    """Функция возвращает список словарей из переданного DataFrame
    Пример структуры:  [{
    "last_digits": "5814",
    "total_spent": 1262.00,
      "cashback": 12.62
    }]"""
    new_df = dataframe.groupby('Номер карты').agg({
        'Сумма операции' : 'sum',
        'Кэшбэк' : 'sum'
    })

    result = []

    for card_number, row in new_df.iterrows():
        result.append({
            'last_digits' : str(card_number)[-4:],
            'total_spent' : float(row['Сумма операции']),
            'cashback' : float(row['Кэшбэк'])
        })

    return result


def get_data_top_transactions_from_df(dataframe: DataFrame) -> list[dict[str, str|float]]:
    """Функция возвращает топ 5 транзакций из переданного DataFrame.
    Структура - список словарей.
    Пример структуры:
    [{"date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"}]"""
    new_df = dataframe.sort_values('Сумма операции', ascending=False)

    top_trans_df = new_df.head()

    result = []

    for card_number, rows in top_trans_df.iterrows():
        result.append({
            "date" : str(rows['Дата платежа']),
            "amount" : float(rows['Сумма операции']),
            "category" : str(rows["Категория"]),
            "description" : str(rows["Описание"])
        })

    return result


def get_data_currencies() -> str:
    """Функция читает файл user_settings.json (забирает список валют),
    возвращает строку валют для дальнейшего поиска"""
    path_to_file_json = os.path.join(PATH, 'data/user_settings.json')

    try:
        with open(path_to_file_json, 'r') as file:
            data_currencies = json.load(file)

        str_currencies = ','.join(data_currencies['user_currencies'])

        return str_currencies

    except JSONDecodeError:
        return ''

    except FileNotFoundError:
        return ''


def get_exchange_currencies() -> list[dict]:
    """Функция, делает запрос к внешнему API для получения текущего курса валют
    возвращает список словарей.
    Валюты для отображения задаются в отдельном файле пользовательских настроек
    user_settings.json.
    Курс считается от RUB"""
    symbols = get_data_currencies()

    try:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base=RUB"
        headers = {
            "apikey": API_KEY_1
        }

        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Ошибка API: {response.status_code}")

        result = []

        for currency, rates in response.json()['rates'].items():
            result.append({
                "currency": currency,
                "rate" : round(1 / rates, 2)
            })

        return result

    except KeyError as error:
        raise KeyError(f"Ключ не найден: {error}")


def get_data_stocks() -> list[str]:
    """Функция читает файл user_settings.json (забирает список акций),
    возвращает строку валют для дальнейшего поиска."""
    path_to_file_json = os.path.join(PATH, 'data/user_settings.json')

    try:
        with open(path_to_file_json, 'r') as file:
            data_stocks = json.load(file)

        list_stocks = data_stocks['user_stocks']

        return list_stocks

    except JSONDecodeError:
        return []

    except FileNotFoundError:
        return []


def get_stock_price() -> list[dict]:
    """Функция, делает запрос к внешнему API для получения данных
    об акциях из https://www.alphavantage.co/"""
    stocks = get_data_stocks()
    result = []

    for stock in stocks:
        url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={API_KEY_2}"
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Ошибка API: {response.status_code}")

        result.append({
            "stock" : stock,
            'price' : response.json()['c'] # ключ -> 'c' - текущая цена
        })

    return result
