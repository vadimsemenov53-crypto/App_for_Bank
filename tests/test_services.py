import json

import pytest

from src.services import get_transactions_with_phones, has_phone


@pytest.mark.parametrize(
    "phone_number, expected",
    [
        ("Тинькофф Мобайл +7 777 555-21-21", True),
        ("МТС Мобайл +7 995 555-55-55", True),
        ("Федеральная Налоговая Служба", False),
    ],
)
def test_has_phone_base(phone_number, expected):
    assert has_phone(phone_number) == expected


def test_get_transactions_with_phones_base(data_services):
    result_json = get_transactions_with_phones(data_services)

    result = json.loads(result_json)

    assert result == [{"Дата операции": "10.01.2024", "Описание": "Оплата по номеру +7 999 123-45-67", "Сумма": 1500}]


def test_get_transactions_with_phones_not_phone():
    data = [
        {
            "Дата операции": "11.01.2024",
            "Описание": "Покупка в магазине",
            "Сумма": 2300,
        }
    ]
    result_json = get_transactions_with_phones(data)

    result = json.loads(result_json)

    assert result == [{"Транзакции": "Нет транзакций содержащих мобильные телефоны."}]


def test_get_transactions_with_key_errors():
    data = [1233, 222, "Описание"]
    result_json = get_transactions_with_phones(data)

    result = json.loads(result_json)

    assert result == [{"'int' object has no attribute 'get'": "Ошибка в формировании отчета."}]
