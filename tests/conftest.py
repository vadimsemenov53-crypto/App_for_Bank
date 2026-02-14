import pytest
import pandas as pd

@pytest.fixture()
def sample_excel(tmp_path):
    file_path = tmp_path / 'test.xlsx'

    df = pd.DataFrame({"A": [1, 2, 3]})
    df.to_excel(file_path, index=False)

    return file_path


@pytest.fixture()
def sample_transactions_df():
    data = ([
        {"Номер карты": "1234567812345814", "Сумма операции": 100.0, "Кэшбэк": 1.0},
        {"Номер карты": "1234567812345814", "Сумма операции": 200.0, "Кэшбэк": 2.0},
        {"Номер карты": "9876543212347512", "Сумма операции": 50.0, "Кэшбэк": 0.5},
        {"Номер карты": "5555444433332222", "Сумма операции": 300.0, "Кэшбэк": 3.0},
    ])
    return pd.DataFrame(data)


@pytest.fixture()
def df_transactions_top_example():
    data = ([
        {"Дата платежа": "2026-02-13", "Сумма операции": 500.0, "Категория": "Переводы", "Описание": "Перевод на карту"},
        {"Дата платежа": "2026-02-16", "Сумма операции": 300.0, "Категория": "Переводы", "Описание": "Перевод другу"},
    ])
    return pd.DataFrame(data)