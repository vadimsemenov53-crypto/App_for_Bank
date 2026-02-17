import datetime
import json
import logging
import os
from json import JSONDecodeError

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

from src.logger_config import setup_logging_utils

setup_logging_utils()
logger = logging.getLogger(__name__)

path = os.path.dirname(os.path.dirname(__file__))
path_env = os.path.join(path, ".env")
load_dotenv(path_env)

API_KEY_1 = os.getenv("API_KEY_1")
API_KEY_2 = os.getenv("API_KEY_2")

PATH = os.path.dirname(os.path.dirname(__file__))


def get_greeting() -> str:
    """Функция приветствия, в зависимости от текущего времени.
    Выводит приветствие."""
    logger.info("Запуск get_greeting. Выполняем запрос для получения времени.")
    time = datetime.datetime.now().hour

    logger.info("Определение приветствия от времени суток")
    if 5 <= time <= 11:
        logger.info("Время: %s часов; Возвращаем: Доброе утро", time)
        return "Доброе утро"

    elif 12 <= time <= 16:
        logger.info("Время: %s часов; Возвращаем: Добрый день", time)
        return "Добрый день"

    elif 17 <= time <= 20:
        logger.info("Время: %s часов; Возвращаем: Добрый вечер", time)
        return "Добрый вечер"

    else:
        logger.info("Время: %s часов; Возвращаем: Доброй ночи", time)
        return "Доброй ночи"


def get_data_transactions_from_xlsx(path_to_file: str | None = None, date: str | None = None) -> DataFrame:
    """Функция возвращает данные о транзакциях из файла XLSX,
    Вы можете передать свой, если он не передан то функция выведет данные
    из файла проекта."""
    logger.info("Запуск get_data_transactions_from_xlsx.")
    if not path_to_file:
        path_to_file = os.path.join(PATH, "data/operations.xlsx")
        logger.debug("Используем стандартный путь: %s", path_to_file)

    logger.info("Читаем файл %s", path_to_file)
    try:
        df = pd.read_excel(path_to_file)
    except Exception as error:
        logger.exception("Ошибка: %s  при чтении файла: %s", error, path_to_file)
        raise

    logger.info("Приводим строки с датой к объекту datetime")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True).dt.normalize()

    if not date:
        logger.info("Возвращаем DataFrame. Завершение работы.")
        return df

    end_date = pd.to_datetime(date, dayfirst=True)
    start_date = end_date.replace(day=1)

    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    if filtered_df.empty:
        logger.error("Нет данных по переданной дате: %s", date)
        raise ValueError(f"Нет данных с такой датой: {date}")

    logger.info(
        "Возвращаем DataFrame за период %s - %s. Найдено записей: %s",
        start_date.date(),
        end_date.date(),
        len(filtered_df),
    )

    return filtered_df


def get_data_transactions_from_df(dataframe: DataFrame) -> list[dict]:
    """Функция возвращает список словарей из переданного DataFrame
    Пример структуры:  [{
    "last_digits": "5814",
    "total_spent": 1262.00,
      "cashback": 12.62
    }]"""
    logger.info("Запуск get_data_transactions_from_df")

    try:
        new_df = dataframe.groupby("Номер карты").agg({"Сумма операции": "sum", "Кэшбэк": "sum"})
    except AttributeError as error:
        logger.error("Отсутствуют необходимые колонки: %s", error)
        raise AttributeError

    logger.debug("Первые строки сгруппированных данных: %s", new_df.head().to_dict())
    result = []

    for card_number, row in new_df.iterrows():
        result.append(
            {
                "last_digits": str(card_number)[-4:],
                "total_spent": round(float(row["Сумма операции"]), 2),
                "cashback": float(row["Кэшбэк"]),
            }
        )

    logger.info("Возвращаем данные по картам. Завершение работы.")
    return result


def get_data_top_transactions_from_df(dataframe: DataFrame) -> list[dict]:
    """Функция возвращает топ 5 транзакций из переданного DataFrame.
    Структура - список словарей.
    Пример структуры:
    [{"date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"}]"""
    logger.info("Запуск get_data_top_transactions_from_df")
    logger.info("Входной DataFrame с %d строками", len(dataframe))

    try:
        new_df = dataframe.sort_values("Сумма операции", ascending=False)
    except Exception as error:
        logger.error("Произошла ошибка: %s", error)
        raise

    top_trans_df = new_df.head()

    result = []

    logger.info("Сортировка данных.")
    for card_number, rows in top_trans_df.iterrows():
        result.append(
            {
                "date": str(rows["Дата операции"])[:10],
                "amount": float(rows["Сумма операции"]),
                "category": str(rows["Категория"]),
                "description": str(rows["Описание"]),
            }
        )
    logger.info("Возвращаем данные ТОП-операций. Завершение работы.")
    return result


def get_data_currencies() -> str:
    """Функция читает файл user_settings.json (забирает список валют),
    возвращает строку валют для дальнейшего поиска"""
    logger.info("Запуск get_data_currencies")
    path_to_file_json = os.path.join(PATH, "data/user_settings.json")

    try:
        logger.info("Чтение файла user_settings.json")
        with open(path_to_file_json, "r") as file:
            data_currencies = json.load(file)

        str_currencies = ",".join(data_currencies["user_currencies"])

        logger.info("Возвращаем полученные данные: %s", str_currencies)
        logger.info("Завершение работы.")
        return str_currencies

    except JSONDecodeError:
        logger.error("Произошла ошибка: JSONDecodeError")
        return ""

    except FileNotFoundError:
        logger.error("Произошла ошибка: FileNotFoundError")
        return ""


def get_exchange_currencies() -> list[dict]:
    """Функция, делает запрос к внешнему API для получения текущего курса валют
    возвращает список словарей.
    Валюты для отображения задаются в отдельном файле пользовательских настроек
    user_settings.json.
    Курс считается от RUB"""
    logger.info("Запуск get_exchange_currencies")

    logger.info("Получение данных из user_settings.json")
    symbols = get_data_currencies()

    try:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base=RUB"
        headers = {"apikey": API_KEY_1}

        logger.info("Обращение к внешнему API-сервису (https://api.apilayer.com)")
        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            logger.error("Ошибка API: %c", response.status_code)
            raise requests.exceptions.RequestException(f"Ошибка API: {response.status_code}")

        result = []

        for currency, rates in response.json()["rates"].items():
            result.append({"currency": currency, "rate": round(1 / rates, 2)})

        logger.info("Возвращаем курс для валют: %s", symbols)
        logger.info("Завершение работы.")
        return result

    except KeyError as error:
        logger.error("Ключ не найден: %s", error)
        raise KeyError(f"Ключ не найден: {error}")


def get_data_stocks() -> list[str]:
    """Функция читает файл user_settings.json (забирает список акций),
    возвращает строку валют для дальнейшего поиска."""
    logger.info("Запуск get_data_stocks")
    path_to_file_json = os.path.join(PATH, "data/user_settings.json")

    try:
        logger.info("Чтение файла user_settings.json")
        with open(path_to_file_json, "r") as file:
            data_stocks = json.load(file)

        list_stocks = data_stocks["user_stocks"]

        if isinstance(list_stocks, list):
            logger.info("Возвращаем полученные данные: %s", list_stocks)
            logger.info("Завершение работы.")
            return [str(stock) for stock in list_stocks]

        return []

    except JSONDecodeError:
        logger.error("Произошла ошибка: JSONDecodeError")
        return []

    except FileNotFoundError:
        logger.error("Произошла ошибка: FileNotFoundError")
        return []


def get_stock_price() -> list[dict]:
    """Функция, делает запрос к внешнему API для получения данных
    об акциях из https://www.alphavantage.co/
    Акции для отображения задаются в отдельном файле пользовательских настроек
    user_settings.json."""
    logger.info("Запуск get_stock_price")

    logger.info("Получение данных из user_settings.json")
    stocks = get_data_stocks()

    result = []

    logger.info("Обращение к внешнему API-сервису (https://finnhub.io)")
    for stock in stocks:
        url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={API_KEY_2}"

        response = requests.get(url)

        if response.status_code != 200:
            logger.error("Ошибка API: %s", response.status_code)
            raise requests.exceptions.RequestException(f"Ошибка API: {response.status_code}")

        result.append({"stock": stock, "price": response.json()["c"]})  # ключ -> 'c' - текущая цена

    logger.info("Возвращаем полученные данные для %s", stocks)
    logger.info("Завершение работы.")
    return result
