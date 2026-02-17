import json
import re

from pandas import DataFrame
from src.logger_config import get_file_logger

PHONE_PATTERN = r"\+7\s\d{3}\s\d{3}-\d{2}-\d{2}"

logger = get_file_logger(__name__, 'services.log')

def has_phone(text: str) -> bool:
    """Функция проверяет строку на наличие номера.
    Возвращает bool - ответ.
    (True - да, False - нет)"""
    return bool(re.search(PHONE_PATTERN, text))


def get_transactions_with_phones(dataframe: DataFrame) -> str:
    """Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""
    try:
        logger.info('Запускаем get_transactions_with_phones')
        dict_df = dataframe.to_dict('records')

        filtered_dict = []

        logger.info('Фильтруем переданный DataFrame, ищем номера телефонов.')
        for row in dict_df:
            if has_phone(str(row['Описание'])):
                row["Дата операции"] = row["Дата операции"].strftime("%d.%m.%Y") #Преобразовать дату в строку
                filtered_dict.append(row)

        logger.info('Сформированный JSON-ответ, содержит: %s транзакций', len(filtered_dict))
        return json.dumps(filtered_dict, ensure_ascii=False, indent=2)


    except Exception as error:
        logger.error('Произошла ошибка: %s', error)
        return json.dumps(
            {"error": "Ошибка в формировании отчета."},
            ensure_ascii=False,
        )
