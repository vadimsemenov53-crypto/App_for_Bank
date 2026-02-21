import json
from datetime import datetime

import pandas as pd
import pytest

import src.reports as reports
from src.reports import save_reports, spending_by_category, sanitize_filename


def test_spending_by_category_base(reports_df):
    result_df = spending_by_category(reports_df, "Еда", "10.03.2024")

    result = result_df.to_dict()
    assert result == {
        "Дата операции": {0: datetime(2024, 1, 1), 1: datetime(2024, 2, 15)},
        "Категория": {0: "Еда", 1: "Еда"},
        "Сумма": {0: 1500, 1: 2000},
    }


def test_spending_by_category_no_date(reports_df):
    result_df = spending_by_category(reports_df, "Еда")

    result = result_df.to_dict()
    assert result == {"Дата операции": {3: datetime(2026, 2, 1)}, "Категория": {3: "Еда"}, "Сумма": {3: 500}}


def test_spending_by_category_non_cat(reports_df):
    with pytest.raises(ValueError):
        spending_by_category(reports_df, "", "10.03.2024")


def test_spending_by_category_wrong_df():
    reports_df = pd.DataFrame([{"Операция": datetime(2026, 2, 5), "Оплата": 2222, "Кэшбек": 0.2}])
    with pytest.raises(ValueError):
        spending_by_category(reports_df, "")


def test_save_reports_base(tmp_path):
    @save_reports("test_reports")
    def example_report():
        return pd.DataFrame({"a": [1, 2]})

    reports.PATH = tmp_path

    example_report(save=True)

    file_path = tmp_path / "data" / "test_reports.json"

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data == [{'a': 1}, {'a': 2}]


def test_save_reports_error(tmp_path):
    @save_reports()
    def example_report():
        raise ValueError("ERROR")

    reports.PATH = tmp_path

    with pytest.raises(ValueError):
        example_report(save=True, file_name='')


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("Market reports", 'market_reports'),
        ("", "reports"),
        ("name_file", "name_file"),
    ]
)
def tests_sanitize_filename(file_name, expected):
    assert sanitize_filename(file_name) == expected

