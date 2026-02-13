import datetime
import pandas as pd
import os
import requests

from pandas.core.interchange.dataframe_protocol import DataFrame


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


def get_data_top_transactions_from_df(dataframe: DataFrame) -> list[dict]:
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


def get_exchange_currencies():

print(get_data_top_transactions_from_df(get_data_transactions_from_xlsx()))