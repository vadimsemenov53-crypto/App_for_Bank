import json
from unittest.mock import patch

from src.views import build_response_json


@patch("src.views.get_stock_price", return_value=[{"stock": "AAPL", "price": 150}])
@patch("src.views.get_exchange_currencies", return_value=[{"currency": "USD", "rate": 75.0}])
@patch(
    "src.views.get_data_top_transactions_from_df",
    return_value=[{"date": "01.02.2026", "amount": 1000, "category": "Покупки", "description": "Магазин"}],
)
@patch(
    "src.views.get_data_transactions_from_df",
    return_value=[{"last_digits": "1234", "total_spent": 1000, "cashback": 10}],
)
@patch("src.views.get_greeting", return_value="Добрый день")
@patch("src.views.get_data_transactions_from_xlsx")
def test_build_response_json_base(
    mock_get_xlsx, mock_greeting, mock_cards, mock_top, mock_currencies, mock_stocks, sample_df_views
):
    mock_get_xlsx.return_value = sample_df_views

    result_json = build_response_json("06.02.2026")

    assert isinstance(result_json, str)

    result = json.loads(result_json)

    assert result["greeting"] == "Добрый день"
    assert isinstance(result["cards"], list)
    assert result["cards"][0]["last_digits"] == "1234"
    assert result["top_transactions"][0]["category"] == "Покупки"
    assert result["currency_rates"][0]["currency"] == "USD"
    assert result["stock_prices"][0]["stock"] == "AAPL"

    mock_get_xlsx.assetr_called_once()
    mock_greeting.assetr_called_once()
    mock_cards.assetr_called_once()
    mock_top.assetr_called_once()
    mock_currencies.assetr_called_once()
    mock_stocks.assetr_called_once()
