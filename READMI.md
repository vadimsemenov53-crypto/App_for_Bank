# 🏦 App for Bank

### Приложение для анализа банковских транзакций с возможностью генерации отчетов, фильтрации по категориям и работе с финансовыми данными.

## 🚀 Описание проекта

### App for Bank позволяет:

- Загружать и анализировать транзакции из XLSX-файлов.
- Фильтровать операции по категориям, времени и суммам.
- Генерировать отчеты в JSON с возможностью сохранения в файл.
- Определять топовые транзакции, валютные операции и котировки акций.
- Проверять текст на наличие телефонных номеров.
- Получать приветственные сообщения и собирать итоговые отчеты в формате JSON.

#### Проект использует Python 3.10+ и библиотеки pandas, json, logging, re.

## 📦 Установка и запуск

Для работы проекта требуется Python **3.14+** и Poetry.

### 1. Установите Poetry (если ещё не установлен)
```pip install poetry```
### 2. Клонирование репозитория
### `git@github.com:vadimsemenov53-crypto/App_for_Bank.git`
### 3. Установка зависимостей
### ```poetry install```
### 4. Запуск программы
### ```python3 main.py```
### 5. Запуск тестов
### ```pytest```
#### Проверка покрытия кода:
```pytest --cov --cov-report=term-missing```

## 🗂 Структура проекта:
```
app_for_bank/
│
├─ src/
│   ├─ main.py                 # Основной модуль запуска
│   ├─ reports.py              # Функции отчетов и декоратор save_reports
│   ├─ views.py                # Формирование JSON ответов
│   ├─ utils.py                # Вспомогательные функции для работы с данными
│   └─ logger_config.py        # Настройка логгера
│
├─ data/                       # Данные и файлы отчетов
├─ tests/                      # Тесты функций
└─ README.md
```
## ⚙️ Функционал

| Функция                                              | Модуль             | Описание                                                     |
| ---------------------------------------------------- | ------------------ | ------------------------------------------------------------ |
| `main()`                                             | `main.py`          | Основной цикл приложения для работы с пользователем.         |
| `get_file_logger()`                                  | `logger_config.py` | Создает настроенный логгер.                                  |
| `sanitize_filename(name)`                            | `reports.py`       | Очищает имя файла от запрещенных символов.                   |
| `save_reports(filename)`                             | `reports.py`       | Декоратор для сохранения результатов функции в JSON.         |
| `spending_by_category(transactions, category, date)` | `reports.py`       | Возвращает траты по категории за последние 3 месяца от даты. |
| `has_phone(text)`                                    | `views.py`         | Проверяет наличие номера телефона в строке.                  |
| `get_transactions_with_phones(dataframe)`            | `views.py`         | Возвращает транзакции с телефонами в JSON.                   |
| `get_greeting()`                                     | `views.py`         | Возвращает приветственное сообщение.                         |
| `get_data_transactions_from_xlsx()`                  | `utils.py`         | Загружает транзакции из XLSX файла.                          |
| `get_data_transactions_from_df(df)`                  | `utils.py`         | Обрабатывает DataFrame транзакций.                           |
| `get_data_top_transactions_from_df(df, n)`           | `utils.py`         | Возвращает топ-N транзакций.                                 |
| `get_data_currencies()`                              | `utils.py`         | Получает данные по валютам.                                  |
| `get_exchange_currencies(currencies, date)`          | `utils.py`         | Возвращает курсы валют на дату.                              |
| `get_data_stocks()`                                  | `utils.py`         | Получает данные по акциям.                                   |
| `get_stock_price(stock_name, date)`                  | `utils.py`         | Возвращает цену акции на дату.                               |
| `build_response_json(date=None)`                     | `views.py`         | Формирует итоговый JSON-ответ со всеми отчетами.             |

## 📝 Примеры использования

### 1. Получение отчета по категории за последние 3 месяца
```
from src.reports import spending_by_category

report_df = spending_by_category(transactions_df, category="Супермаркеты", date="20.05.2020", save=True)
print(report_df)
```
### 2. Сохранение отчета через декоратор
```
from src.reports import save_reports

@save_reports("my_report")
def example_report():
    return transactions_df.head(10)

example_report(save=True)
```

### 3. Получение транзакций с телефонами
```
from src.views import get_transactions_with_phones

json_report = get_transactions_with_phones(transactions_df)
print(json_report)
```

### 🧾 Логирование

- Логи создаются для основной программы (main.log) и для отчетов (views, utils, services, reports.log).
- Логи содержат информацию о запуске функций, фильтрации данных, сохранении файлов и ошибках.

### ✅ Тестирование

### Используется pytest.
#### Примеры тестов:
- Проверка работы декоратора save_reports.
- Фильтрация транзакций в spending_by_category.
- Поиск телефонов в get_transactions_with_phones.
- Очистка имен файлов в sanitize_filename.

### 💡 Особенности
- Все функции работают с pandas.DataFrame.
- Декоратор save_reports поддерживает:
- Параметр save=True/False — включение/выключение сохранения.
- Параметр file_name — пользовательское имя файла.
- Даты принимаются в формате dd.mm.yyyy.
- Все JSON файлы создаются с кодировкой UTF-8.
