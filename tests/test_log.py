import os

from src.decorators import log


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


@log
def test_log_check():
    return "Проверка работы записи в файл"
