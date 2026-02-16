import json

from src.utils import (get_data_top_transactions_from_df, get_data_transactions_from_df,
                       get_data_transactions_from_xlsx, get_exchange_currencies, get_greeting, get_stock_price)


def build_response_json(date: str | None = None) -> str:
    """Функция - конструктор, принимает дату формата(20.05.2020),
    формирует JSON-ответ для фронта.
    Структура ответа:
    "greeting": "Добрый день",
    "cards": cards,
    "top_transactions": transactions,
    "currency_rates": currencies,
    "stock_prices": stocks"""
    df = get_data_transactions_from_xlsx(date=date)

    response = {
        "greeting": get_greeting(),
        "cards": get_data_transactions_from_df(df),
        "top_transactions": get_data_top_transactions_from_df(df),
        "currency_rates": get_exchange_currencies(),
        "stock_prices": get_stock_price(),
    }

    return json.dumps(response, ensure_ascii=False, indent=4)
