import logging
import os

PATH = os.path.dirname(os.path.dirname(__file__))


def get_file_logger(name: str, filename: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        path_to_file = os.path.join(PATH, f"data/{filename}")

        file_handler = logging.FileHandler(path_to_file, mode="w", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger