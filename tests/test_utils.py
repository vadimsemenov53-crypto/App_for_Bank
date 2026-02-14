import pytest
from unittest.mock import patch
import pandas as pd
from pandas.core.methods.selectn import DataFrame

from src.utils import get_greeting, get_data_transactions_from_xlsx, get_data_transactions_from_df
from src.utils import get_data_top_transactions_from_df

@patch('src.utils.datetime.datetime')
def test_get_greeting_base_1(mock_get):
    mock_get.now.return_value.hour = 8

    assert get_greeting() == 'Доброе утро'


@patch('src.utils.datetime.datetime')
def test_get_greeting_base_2(mock_get):
    mock_get.now.return_value.hour = 14

    assert get_greeting() == 'Добрый день'


@patch('src.utils.datetime.datetime')
def test_get_greeting_base_22(mock_get):
    mock_get.now.return_value.hour = 20

    assert get_greeting() == 'Добрый вечер'


@patch('src.utils.datetime.datetime')
def test_get_greeting_base_4(mock_get):
    mock_get.now.return_value.hour = 22

    assert get_greeting() == 'Доброй ночи'

@patch('src.utils.pd.read_excel')
def test_get_data_transactions_from_xlsx_base(mock_get):
    mock_get.return_value = pd.DataFrame({"A": [1, 2]})

    result = get_data_transactions_from_xlsx("test.xlsx")

    mock_get.assert_called_once_with("test.xlsx")
    assert isinstance(result, pd.DataFrame)


def test_get_data_transactions_from_xlsx_new_file(sample_excel):
    result = get_data_transactions_from_xlsx(str(sample_excel))

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


def test_get_data_transactions_from_df_base(sample_transactions_df):
    result = get_data_transactions_from_df(sample_transactions_df)

    assert result == [{'last_digits': '5814', 'total_spent': 100.0, 'cashback': 1.0}]


def test_get_data_transactions_from_df_wrong_type():
    with pytest.raises(AttributeError):
        get_data_transactions_from_df([1, 2, 3])

    with pytest.raises(AttributeError):
        get_data_transactions_from_df([
        {"Номер карты": "1234567812345814", "Кэшбэк": 1.0}
    ])

    with pytest.raises(TypeError):
        get_data_transactions_from_df()


def test_get_data_top_transactions_from_df():
