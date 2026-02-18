import json
import pandas as pd
import logging
from datetime import datetime
from typing import Optional
from pandas import DateOffset

def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории
     за последние три месяца (от переданной даты)
     Формат даты: (01.01.2021)"""

    if date is None:
        today = datetime.today().date()
        end_date = datetime.combine(today, datetime.min.time())

    else:
        end_date = datetime.strptime(date, "%d.%m.%Y")

    start_date = end_date - DateOffset(months=3)

    df = transactions.copy()

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True).dt.normalize()

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
    ]

    result = filtered_df[filtered_df['Категория'] == category]

    return pd.DataFrame(result)

