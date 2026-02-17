import logging
import os

PATH = os.path.dirname(os.path.dirname(__file__))


def setup_logging_views() -> None:
    """Функция для базовых настроек логера"""
    path_to_file = os.path.join(PATH, "data/views.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=path_to_file,  # имя файла
        filemode="w",  # перезапись файла при запуске
        encoding="utf-8",
    )
