from src.views import build_response_json
from src.utils import get_data_transactions_from_xlsx
from src.reports import spending_by_category, save_reports

def main() -> None:
    print(
        """
        Программа: Привет! Добро пожаловать в Приложение для анализа банковских операций.
        Данное приложение анализирует транзакции из XLSX-файла
        """
    )

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

            result_json = build_response_json(date=date_user)
            print(result_json)

        elif choice == "2":
            print("""Программа: Получить данные по тратам в заданной категории
                за последние три месяца (от переданной даты).
                Передайте дату в формате: 20.05.2020,
                Вы можете оставить окно пустым, в таком случае будет произведен анализ
                от текущей даты.""")
            date_user = str(input('Пользователь: '))

            print("Программа: Напишите категорию для поиска.")
            category_user = str(input("Пользователь: ")).strip()

            result_df = get_data_transactions_from_xlsx()

            print("Программа: Сохранить отчет? (да/нет).")
            save_answer = str(input('Пользователь: ')).strip().lower()

            file_name_user = None

            if save_answer == 'да':
                print("Программа: Введите имя файла (или Enter для стандартного).")
                file_name_user = str(input("Пользователь: ")).strip()
                if not file_name_user:
                    file_name_user = None


            report = spending_by_category(
                result_df,
                category_user,
                date_user,
                save=(save_answer.lower() == 'да'),
                file_name=file_name_user
                )
            print(report)

        elif choice == "0":
            print("Программа: Завершение работы.")
            break

        else:
            print("Программа: Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()