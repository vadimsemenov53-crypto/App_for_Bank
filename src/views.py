import json
import logging

from src.logger_config import setup_logging_views
from src.utils import (get_data_top_transactions_from_df, get_data_transactions_from_df,
                       get_data_transactions_from_xlsx, get_exchange_currencies, get_greeting, get_stock_price)

setup_logging_views()
logger = logging.getLogger(__name__)


def build_response_json(date: str | None = None) -> str:
    """Функция - конструктор, принимает дату формата(20.05.2020),
    формирует JSON-ответ для фронта.
    Структура ответа:
    "greeting": "Добрый день",
    "cards": cards,
    "top_transactions": transactions,
    "currency_rates": currencies,
    "stock_prices": stocks"""
    if date:
        logger.info(
            "Запущено приложение: Страница «Главная». Передаем дату %s для сортировки.",
            date,
        )
    else:
        logger.info("Запущено приложение: Страница «Главная».")

    try:
        df = get_data_transactions_from_xlsx(date=date)

        logger.info("Формирование JSON-ответа.")
        response = {
            "greeting": get_greeting(),
            "cards": get_data_transactions_from_df(df),
            "top_transactions": get_data_top_transactions_from_df(df),
            "currency_rates": get_exchange_currencies(),
            "stock_prices": get_stock_price(),
        }

        logger.info("JSON-ответ готов. Завершение работы.")
        return json.dumps(response, ensure_ascii=False, indent=4)

    except Exception as error:
        logger.warning(f"Ошибка при получении данных: {error}")
        return json.dumps(
            {"error": "Ошибка в формировании отчета."},
            ensure_ascii=False,
        )

print(build_response_json("22.01.2020"))