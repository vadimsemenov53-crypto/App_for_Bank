import pandas as pd
import pytest


@pytest.fixture()
def sample_excel_df():
    df = pd.DataFrame(
        {
            "Дата операции": ["01.12.2021 10:00:00", "10.12.2021 12:00:00", "25.12.2021 15:00:00"],
            "Сумма": [100, 200, 300],
        }
    )
    return df


@pytest.fixture()
def sample_excel_file(tmp_path):
    file_path = tmp_path / "test.xlsx"

    df = pd.DataFrame(
        {
            "Дата операции": ["01.12.2021 10:00:00", "10.12.2021 12:00:00", "25.12.2021 15:00:00"],
            "Сумма": [100, 200, 300],
        }
    )
    df.to_excel(file_path, index=False)

    return file_path


@pytest.fixture()
def sample_transactions_df():
    data = [
        {"Номер карты": "1234567812345814", "Сумма операции": 100.0, "Кэшбэк": 1.0},
        {"Номер карты": "1234567812345814", "Сумма операции": 200.0, "Кэшбэк": 2.0},
        {"Номер карты": "9876543212347512", "Сумма операции": 50.0, "Кэшбэк": 0.5},
        {"Номер карты": "5555444433332222", "Сумма операции": 300.0, "Кэшбэк": 3.0},
    ]
    return pd.DataFrame(data)


@pytest.fixture()
def df_transactions_top_example():
    data = [
        {
            "Дата операции": "2026-02-13",
            "Сумма операции": 500.0,
            "Категория": "Переводы",
            "Описание": "Перевод на карту",
        },
        {"Дата операции": "2026-02-16", "Сумма операции": 300.0, "Категория": "Переводы", "Описание": "Перевод другу"},
    ]
    return pd.DataFrame(data)


@pytest.fixture()
def data_exchange_currencies():
    return {
        "success": True,
        "timestamp": 1771063088,
        "base": "RUB",
        "date": "2026-02-14",
        "rates": {"USD": 0.012956, "EUR": 0.010914},
    }


@pytest.fixture()
def sample_df_views():
    return pd.DataFrame(
        {
            "Номер карты": ["1234", "5678"],
            "Сумма операции": [1000, 500],
            "Кэшбэк": [10, 5],
            "Дата операции": ["01.02.2026", "02.02.2026"],
            "Категория": ["Покупки", "Переводы"],
            "Описание": ["Магазин", "Перевод другу"],
        }
    )
