from datetime import datetime
from src.reports import spending_by_category

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