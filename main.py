from src.logger_config import get_file_logger
from src.reports import spending_by_category
from src.utils import get_data_transactions_from_xlsx
from src.views import build_response_json

logger = get_file_logger(__name__, "main.log")


def main() -> None:
    logger.info("Запущено основное приложение.")
    print("""
        Программа: Привет! Добро пожаловать в Приложение для анализа банковских операций.
        Данное приложение анализирует транзакции из XLSX-файла
        """)

    try:
        while True:
            print("""
            Программа:
            Выберите действие:
            1 — Анализ операций
            2 — Отчет по категории за 3 месяца
            0 — Выход
            """)

            choice = input("Пользователь: ")

            if choice == "1":
                print("""Программа: Передайте дату в формате: 20.05.2020
                    Будет произведен анализ данных за начало месяца и до переданной даты
                    Вы можете оставить окно пустым, в таком случае будет произведен анализ
                    всего файла целиком""")
                date_user = str(input("Пользователь: "))

                logger.info("JSON-ответ сформирован -> вывод в консоль.")
                result_json = build_response_json(date=date_user)
                print(result_json)

            elif choice == "2":
                print("""Программа: Получить данные по тратам в заданной категории
                    за последние три месяца (от переданной даты).
                    Передайте дату в формате: 20.05.2020,
                    Вы можете оставить окно пустым, в таком случае будет произведен анализ
                    от текущей даты.""")
                date_user = str(input("Пользователь: "))

                print("Программа: Напишите категорию для поиска.")
                category_user = str(input("Пользователь: ")).strip()

                logger.info("Пользователь выбрал категорию: %s, дата: %s", category_user, date_user or "текущая")

                result_df = get_data_transactions_from_xlsx()

                print("Программа: Сохранить отчет? (да/нет).")
                save_answer = str(input("Пользователь: ")).strip().lower()

                file_name_user = None

                if save_answer == "да":
                    print("Программа: Введите имя файла (или Enter для стандартного).")
                    file_name_user = str(input("Пользователь: ")).strip()

                    if not file_name_user:
                        file_name_user = None

                logger.info("Запись отчета в файл: %s.json", file_name_user)

                report = spending_by_category(
                    result_df, category_user, date_user, save=(save_answer.lower() == "да"), file_name=file_name_user
                )

                logger.info("Отчет сформирован -> вывод в консоль")
                print(report)

            elif choice == "0":
                logger.info("Завершение работы программы.")
                print("Программа: Завершение работы.")
                break

            else:
                print("Программа: Неверный выбор. Попробуйте снова.")

    except Exception as error:
        logger.error("Произошла ошибка %s", error)
        raise


if __name__ == "__main__":
    main()
