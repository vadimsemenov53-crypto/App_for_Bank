import json
import pandas as pd
import pytest
import src.reports as reports

from datetime import datetime
from src.reports import spending_by_category, save_reports
from tests.conftest import reports_df


def test_spending_by_category_base(reports_df):
    result_df = spending_by_category(reports_df, 'Еда','10.03.2024')

    result = result_df.to_dict()
    assert result == {'Дата операции': {0: datetime(2024, 1, 1),
                                        1: datetime(2024, 2, 15)},
                      'Категория': {0: 'Еда',
                                    1: 'Еда'},
                      'Сумма': {0: 1500,
                                1: 2000}}


def test_spending_by_category_no_date(reports_df):
    result_df = spending_by_category(reports_df, 'Еда')

    result = result_df.to_dict()
    assert result == {'Дата операции': {3: datetime(2026,2,1)},
                      'Категория': {3: 'Еда'},
                      'Сумма': {3: 500}}


def test_spending_by_category_non_cat(reports_df):
    result_df = spending_by_category(reports_df, '','10.03.2024')

    result = result_df.to_dict()
    assert result == {'Дата операции': {}, 'Категория': {}, 'Сумма': {}}


def test_spending_by_category_wrong_df():
    reports_df = pd.DataFrame([{
        'Операция' : datetime(2026, 2,5),
        'Оплата' : 2222,
        'Кэшбек' : 0.2
    }])
    with pytest.raises(ValueError):
        spending_by_category(reports_df, '')


def test_save_reports_base(tmp_path):
    @save_reports('test_reports')
    def example_report():
        return pd.DataFrame({"a": [1, 2]})

    reports.PATH = tmp_path

    example_report()

    file_path = tmp_path / "data" / "test_reports.json"

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "a" in data
    assert data["a"] == {'0': 1, '1': 2}


def test_save_reports_error(tmp_path):
    @save_reports()
    def example_report():
        raise ValueError("ERROR")

    reports.PATH = tmp_path

    example_report()

    file_path = tmp_path / "data" / "reports.json"

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["Тип ошибки"] == "ValueError"


def test_save_reports_erro():
    @save_reports()
    def example_report():
        return {"a": [1, 2]}

    example_report()

    with open("/Users/vadimsemenov/PycharmProjects/App_for_Bank/data/reports.json",
              "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["a"] == [1, 2]