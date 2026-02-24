import json
import os
import re
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from pandas import DateOffset

from src.logger_config import get_file_logger

logger = get_file_logger(__name__, "reports.log")

PATH = os.path.dirname(os.path.dirname(__file__))


def sanitize_filename(name: str) -> str:
    """Функция принимает имя файла и фильтрует его от мусора.
    Возвращает очищенное имя."""
    name = name.strip().lower()
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-zA-Z0-9_-]", "", name)
    return name or "reports"


def save_reports(filename: str | None = None) -> Callable[..., Any]:
    """
    Декоратор для функций-отчетов, записывает в файл результат,
    который возвращает функция, формирующая отчет.
    Если filename не указан — отчет записывается в файл
     с дефолтным названием (records.json).
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            save_enabled = kwargs.pop("save", False)
            user_file_name = kwargs.pop("file_name", None)

            result = func(*args, **kwargs)

            if not save_enabled:
                return result

            file_name = sanitize_filename(user_file_name or filename or "reports")

            path_to_file = os.path.join(PATH, "data", f"{file_name}.json")
            os.makedirs(os.path.dirname(path_to_file), exist_ok=True)

            if isinstance(result, pd.DataFrame):
                data_to_save = result.to_dict(orient="records")
            else:
                data_to_save = result

            with open(path_to_file, "w", encoding="utf-8") as file:
                json.dump(data_to_save, file, indent=2, ensure_ascii=False, default=str)

            logger.info("Отчет успешно сохранен в %s", path_to_file)

            return result

        return wrapper

    return decorator


@save_reports()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории
    за последние три месяца (от переданной даты)
    Формат даты: (01.01.2021)"""
    logger.info("Запуск spending_by_category")

    try:
        if date is None:
            today = datetime.today().date()
            end_date = datetime.combine(today, datetime.min.time())

        else:
            end_date = datetime.strptime(date, "%d.%m.%Y")

        start_date = end_date - DateOffset(months=3)
        logger.info(
            "Определяем начало: %s, и конец: %s", start_date.strftime("%d.%m.%Y"), end_date.strftime("%d.%m.%Y")
        )

        df = transactions.copy()

        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True).dt.normalize()

        filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

        result = filtered_df[filtered_df["Категория"] == category]

        if result.empty:
            raise ValueError("Нет данных за указанный период")

        logger.info("Возвращаем готовый DateFrame. Завершение работы.")
        return pd.DataFrame(result)

    except Exception as error:
        logger.error("Произошла ошибка %s", error)
        return pd.DataFrame({"Произошла ошибка": f"{error}"})
