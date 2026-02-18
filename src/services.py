import json
import re

from src.logger_config import get_file_logger

PHONE_PATTERN = r"\+7\s\d{3}\s\d{3}-\d{2}-\d{2}"

logger = get_file_logger(__name__, "services.log")


def has_phone(text: str) -> bool:
    """Функция проверяет строку на наличие номера.
    Возвращает bool - ответ.
    (True - да, False - нет)"""
    return bool(re.search(PHONE_PATTERN, text))


def get_transactions_with_phones(transactions: list[dict]) -> str:
    """Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""
    try:
        logger.info("Запускаем get_transactions_with_phones")

        filtered_transactions = []

        logger.info("Фильтруем переданный список, ищем номера телефонов.")
        for transaction in transactions:
            description = str(transaction.get("Описание", ""))

            if re.search(PHONE_PATTERN, description):
                filtered_transactions.append(transaction)

        if not filtered_transactions:
            return json.dumps(
                [{"Транзакции": "Нет транзакций содержащих мобильные телефоны."}], ensure_ascii=False, indent=2
            )

        logger.info("Сформированный JSON-ответ, содержит: %s транзакций", len(filtered_transactions))
        return json.dumps(filtered_transactions, ensure_ascii=False, indent=2)

    except Exception as error:
        logger.error("Ошибка при обработке транзакций: %s", error)
        return json.dumps(
            [{f"{error}": "Ошибка в формировании отчета."}],
            ensure_ascii=False,
        )
