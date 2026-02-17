import pytest
import logging

from src.logger_config import get_file_logger

def test_get_file_logger_base():
    logger = get_file_logger('test', 'test.log')

    assert isinstance(logger, logging.Logger)


def test_get_file_logger_not_duplicate():
    logger_1 = get_file_logger('test', 'test.log')
    logger_2 = get_file_logger('test', 'test.log')

    assert len(logger_1.handlers) == 1
