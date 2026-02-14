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
        {"Номер карты": "1234567812345814", "Сумма операции": 100.0, "Кэшбэк": 1.0}
    ])
    return pd.DataFrame(data)