from json import JSONDecodeError
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from requests import RequestException

from src.utils import (get_data_currencies, get_data_stocks, get_data_top_transactions_from_df,
                       get_data_transactions_from_df, get_data_transactions_from_xlsx, get_exchange_currencies,
                       get_greeting, get_stock_price)


@patch("src.utils.datetime.datetime")
def test_get_greeting_base_1(mock_get):
    mock_get.now.return_value.hour = 8

    assert get_greeting() == "Доброе утро"


@patch("src.utils.datetime.datetime")
def test_get_greeting_base_2(mock_get):
    mock_get.now.return_value.hour = 14

    assert get_greeting() == "Добрый день"


@patch("src.utils.datetime.datetime")
def test_get_greeting_base_22(mock_get):
    mock_get.now.return_value.hour = 20

    assert get_greeting() == "Добрый вечер"


@patch("src.utils.datetime.datetime")
def test_get_greeting_base_4(mock_get):
    mock_get.now.return_value.hour = 22

    assert get_greeting() == "Доброй ночи"


@patch("src.utils.pd.read_excel")
def test_get_data_transactions_from_xlsx_base(mock_get):
    mock_get.return_value = pd.DataFrame(
        {"Дата операции": ["01.12.2021 10:00:00", "02.12.2021 11:00:00"], "Сумма": [100, 200]}
    )

    result = get_data_transactions_from_xlsx("test.xlsx")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    mock_get.assert_called_once_with("test.xlsx")


@patch("src.utils.pd.read_excel")
def test_get_data_transactions_from_xlsx_date(mock_get, sample_excel_df):
    mock_get.return_value = sample_excel_df

    result = get_data_transactions_from_xlsx("test.xlsx", "03.12.2021")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    mock_get.assert_called_once_with("test.xlsx")


@patch("src.utils.pd.read_excel")
def test_get_data_transactions_from_xlsx_not_date(mock_get, sample_excel_df):
    mock_get.return_value = sample_excel_df

    with pytest.raises(ValueError, match="Нет данных с такой датой: 11.11.2020"):
        get_data_transactions_from_xlsx("test.xlsx", "11.11.2020")


@patch("src.utils.pd.read_excel", side_effect=FileNotFoundError)
def test_get_data_transactions_from_xlsx_not_file(mock_read):
    with pytest.raises(FileNotFoundError):
        get_data_transactions_from_xlsx()

    mock_read.assert_called_once()


def test_get_data_transactions_from_xlsx_new_file(sample_excel_file):
    result = get_data_transactions_from_xlsx(str(sample_excel_file))

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


def test_get_data_transactions_from_df_base(sample_transactions_df):
    result = get_data_transactions_from_df(sample_transactions_df)

    assert result == [
        {"last_digits": "5814", "total_spent": 300.0, "cashback": 3.0},
        {"last_digits": "2222", "total_spent": 300.0, "cashback": 3.0},
        {"last_digits": "7512", "total_spent": 50.0, "cashback": 0.5},
    ]


def test_get_data_transactions_from_df_wrong_type():
    with pytest.raises(AttributeError):
        get_data_transactions_from_df([1, 2, 3])

    with pytest.raises(AttributeError):
        get_data_transactions_from_df([{"Номер карты": "1234567812345814", "Кэшбэк": 1.0}])

    with pytest.raises(TypeError):
        get_data_transactions_from_df()


def test_get_data_top_transactions_from_df_base(df_transactions_top_example):
    result = get_data_top_transactions_from_df(df_transactions_top_example)

    assert result == [
        {"amount": 500.0, "category": "Переводы", "date": "2026-02-13", "description": "Перевод на карту"},
        {"amount": 300.0, "category": "Переводы", "date": "2026-02-16", "description": "Перевод другу"},
    ]


def test_get_data_top_transactions_from_df_wrong_type():
    with pytest.raises(ValueError):
        get_data_top_transactions_from_df(
            pd.DataFrame({"Номер": "1234567812345814", "Сумма": 100.0, "Кэшбэк": 1.0})
        )

    with pytest.raises(TypeError):
        get_data_top_transactions_from_df(222)


@patch("builtins.open")
@patch("src.utils.json.load")
def test_get_data_currencies_base(mock_json, mock_open):
    mock_json.return_value = {"user_currencies": ["USD", "EUR", "JPY"], "user_stocks": ["APPLE", "GOOGLE"]}
    result = get_data_currencies()

    assert result == "USD,EUR,JPY"

    mock_json.assert_called_once()
    mock_open.assert_called_once()


@patch("builtins.open", side_effect=FileNotFoundError)
def test_get_data_currencies_not_found(mock_open):
    assert get_data_currencies() == ""

    mock_open.assert_called_once()


@patch("builtins.open")
@patch("src.utils.json.load", side_effect=JSONDecodeError("msg", "doc", 0))
def test_get_data_currencies_json_err(mock_json, mock_open):
    assert get_data_currencies() == ""

    mock_json.assert_called_once()
    mock_open.assert_called_once()


@patch("src.utils.requests.get")
@patch("src.utils.get_data_currencies", return_value="USD,EUR")
def test_get_exchange_currencies_base(mock_get_data, mock_requests, data_exchange_currencies):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = data_exchange_currencies

    mock_requests.return_value = mock_response

    result = get_exchange_currencies()

    assert result == [{"currency": "USD", "rate": 77.18}, {"currency": "EUR", "rate": 91.63}]
    mock_get_data.assert_called_once()
    mock_requests.assetr_called_once()


@patch("src.utils.requests.get")
@patch("src.utils.get_data_currencies", return_value="USD,EUR")
def test_get_exchange_currencies_wrong_status(mock_get_data, mock_requests, data_exchange_currencies):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.return_value = data_exchange_currencies

    mock_requests.return_value = mock_response

    with pytest.raises(RequestException, match="Ошибка API: 400"):
        get_exchange_currencies()

    mock_get_data.assert_called_once()
    mock_requests.assert_called_once()


@patch("src.utils.requests.get")
@patch("src.utils.get_data_currencies", return_value="USD,EUR")
def test_get_exchange_currencies_not_key(mock_get_data, mock_requests):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "timestamp": 1771063088, "base": "RUB", "date": "2026-02-14"}

    mock_requests.return_value = mock_response

    with pytest.raises(KeyError, match="Ключ не найден: 'rates'"):
        get_exchange_currencies()

    mock_get_data.assert_called_once()
    mock_requests.assert_called_once()


@patch("builtins.open")
@patch("src.utils.json.load")
def test_get_data_stocks_base(mock_json, mock_open):
    mock_json.return_value = {"user_currencies": ["USD", "EUR", "JPY"], "user_stocks": ["APPLE", "GOOGLE"]}
    result = get_data_stocks()

    assert result == ["APPLE", "GOOGLE"]

    mock_json.assert_called_once()
    mock_open.assert_called_once()


@patch("builtins.open", side_effect=FileNotFoundError)
def test_get_data_stocks_not_found(mock_open):
    assert get_data_stocks() == []

    mock_open.assert_called_once()


@patch("builtins.open")
@patch("src.utils.json.load", side_effect=JSONDecodeError("msg", "doc", 0))
def test_get_data_stocks_json_err(mock_json, mock_open):
    assert get_data_stocks() == []

    mock_json.assert_called_once()
    mock_open.assert_called_once()


@patch("src.utils.requests.get")
@patch("src.utils.get_data_stocks", return_value=["AAPL", "MSFT"])
def test_get_stock_price_base(mock_get_data, mock_requests):
    mock_response_1 = Mock()
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {"c": 189.12, "h": 190.45}

    mock_response_2 = Mock()
    mock_response_2.status_code = 200
    mock_response_2.json.return_value = {"c": 332.22, "h": 333.33}

    mock_requests.side_effect = [mock_response_1, mock_response_2]

    result = get_stock_price()

    assert result == [{"stock": "AAPL", "price": 189.12}, {"stock": "MSFT", "price": 332.22}]

    mock_get_data.assert_called_once()
    assert mock_requests.call_count == 2


@patch("src.utils.requests.get")
@patch("src.utils.get_data_stocks", return_value=["AAPL", "MSFT"])
def test_get_stock_price_wrong_status(mock_get_data, mock_requests):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"c": 189.12}

    mock_requests.return_value = mock_response

    with pytest.raises(RequestException, match="Ошибка API: 404"):
        get_stock_price()

    mock_get_data.assert_called_once()
    mock_requests.assert_called_once()
