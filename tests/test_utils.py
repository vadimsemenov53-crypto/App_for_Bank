import pytest
from unittest.mock import patch

from src.utils import get_greeting

@patch('src.utils.datetime.datetime')
def test_get_greeting_base_1(mock_get):
    mock_get.now.return_value.hour = 8

    assert get_greeting() == 'Доброе утро'


@patch('src.utils.datetime.datetime')
def test_get_greeting_base_2(mock_get):
    mock_get.now.return_value.hour = 14

    assert get_greeting() == 'Добрый день'


@patch('src.utils.datetime.datetime')
def test_get_greeting_base_3(mock_get):
    mock_get.now.return_value.hour = 20

    assert get_greeting() == 'Добрый вечер'


@patch('src.utils.datetime.datetime')
def test_get_greeting_base_4(mock_get):
    mock_get.now.return_value.hour = 22

    assert get_greeting() == 'Доброй ночи'
