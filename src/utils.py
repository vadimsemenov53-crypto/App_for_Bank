import datetime

def get_greeting() -> str:
    """Функция приветствия, в зависимости от текущего времени.
    Выводит приветствие."""
    time = datetime.datetime.now().hour

    if 5 <= time <= 11:
        return 'Доброе утро'
    elif 12 <= time <= 16:
        return 'Добрый день'
    elif 17 <= time <= 20:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'

