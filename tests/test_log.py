import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.decorators import log, write_log, convert_to_html, init_html_log, close_html_log


def test_write_log_console():
    """Тест write_log с выводом в консоль (filename=None)"""
    with patch('builtins.print') as mock_print:
        write_log("Тестовое сообщение", filename=None)
        mock_print.assert_called_once_with("Тестовое сообщение")


def test_write_log_file():
    """Тест write_log с записью в файл"""
    test_message = "Тестовое сообщение для файла"

    with patch('builtins.open', mock_open()) as mock_file:
        write_log(test_message, filename="test_log.html")

        # Проверяем что файл был открыт для записи
        mock_file.assert_called_once_with("test_log.html", "a", encoding="utf-8")

        # Проверяем что была запись в файл
        handle = mock_file()
        handle.write.assert_called()


def test_convert_to_html_error():
    """Тест convert_to_html для сообщений об ошибке"""
    result = convert_to_html("Ошибка: что-то пошло не так")
    assert 'color: red' in result
    assert "Ошибка: что-то пошло не так" in result


def test_convert_to_html_success():
    """Тест convert_to_html для успешных сообщений"""
    result = convert_to_html("Успешно завершено")
    assert 'color: green' in result


def test_convert_to_html_start():
    """Тест convert_to_html для сообщений о начале"""
    result = convert_to_html("Начало выполнения функции")
    assert 'color: blue' in result


def test_convert_to_html_default():
    """Тест convert_to_html для обычных сообщений"""
    result = convert_to_html("Обычное сообщение")
    assert 'color:' not in result
    assert "<p>Обычное сообщение</p>" in result


def test_init_html_log():
    """Тест init_html_log"""
    with patch('builtins.open', mock_open()) as mock_file:
        init_html_log("test_init.html")

        mock_file.assert_called_once_with("test_init.html", "w", encoding="utf-8")

        handle = mock_file()
        # Проверяем что был записан HTML заголовок
        assert handle.write.called


def test_close_html_log():
    """Тест close_html_log"""
    with patch('builtins.open', mock_open()) as mock_file:
        close_html_log("test_close.html")

        mock_file.assert_called_once_with("test_close.html", "a", encoding="utf-8")

        handle = mock_file()
        assert handle.write.called


def test_log_decorator_with_exception():
    """Тест декоратора log при возникновении исключения"""

    @log(filename=None)
    def failing_function():
        raise ValueError("Тестовая ошибка")

    with patch('src.decorators.write_log') as mock_write_log:
        try:
            failing_function()
        except ValueError:
            pass

        # Проверяем что были логи начала и ошибки
        assert mock_write_log.call_count >= 2
        calls = [call[0][0] for call in mock_write_log.call_args_list]
        assert any("Начало выполнения" in call for call in calls)
        assert any("Ошибка" in call for call in calls)


def test_log_decorator_with_arguments():
    """Тест декоратора log с аргументами"""

    @log(filename="test_decorator.html")
    def sample_function(x, y):
        return x + y

    with patch('src.decorators.write_log') as mock_write_log:
        result = sample_function(2, 3)

        assert result == 5
        # Проверяем что были логи начала и успешного завершения
        assert mock_write_log.call_count >= 2


def test_log_decorator_with_custom_filename():
    """Тест декоратора log с кастомным filename"""

    # Декоратор с аргументами
    @log(filename="custom_log.html")
    def test_func():
        return "result"

    with patch('src.decorators.write_log') as mock_write_log:
        test_func()

        # Проверяем что write_log вызывался с правильным filename
        mock_write_log.assert_called()
        for call in mock_write_log.call_args_list:
            assert call[0][1] == "custom_log.html"


def test_log_decorator_direct_call():
    """Тест прямого вызова декоратора"""

    def test_function():
        return "test"

    # Прямой вызов декоратора
    decorated = log(filename=None)(test_function)

    with patch('src.decorators.write_log') as mock_write_log:
        result = decorated()

        assert result == "test"
        mock_write_log.assert_called()

def test_log_decorator_console_output(capsys):
    """Test log decorator console output (filename=None)"""

    @log(filename=None)  # Вывод в консоль
    def sample_function():
        return "success"

    result = sample_function()
    assert result == "success"

    captured = capsys.readouterr()
    output = captured.out
    assert "sample_function - Начало выполнения" in output
    assert "sample_function - Успешно завершено" in output


@log(filename="log_file.html")
def test_log_decorator_file_output():
    """Test log decorator file output"""
    test_file = "test_log.log"
    if os.path.exists(test_file):
        os.remove(test_file)

    @log(filename=test_file)  # Вывод в файл
    def sample_function():
        return "success"

    result = sample_function()
    assert result == "success"

    # Проверяем файл
    assert os.path.exists(test_file)
    with open(test_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "sample_function - Начало выполнения" in content

    # Очистка
    if os.path.exists(test_file):
        os.remove(test_file)


if __name__ == "__main__":
    print("Запуск тестов ...")
