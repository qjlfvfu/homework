import datetime
import functools
from typing import Any, Callable, Optional


def log(func: Optional[Callable[..., Any]] = None, *, filename: Optional[str] = "log_file.html") -> Callable[..., Any]:
    """
    Декоратор для логирования в HTML-файл или консоль.
    Если filename=None - вывод в консоль, иначе в HTML-файл.
    """
    if func is None:
        return lambda f: log(f, filename=filename)

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = datetime.datetime.now()
        func_name = func.__name__
        timestamp = start_time.strftime("%Y-%m-%d %H:%M:%S")

        # Логируем начало выполнения
        start_message = f"{timestamp} - {func_name} - Начало выполнения"
        write_log(start_message, filename)

        try:
            # Выполняем функцию
            result = func(*args, **kwargs)

            # Логируем успешное завершение
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            success_message = (
                f"{timestamp} - {func_name} - Успешно завершено. Время: {duration:.3f}с. Результат: {result}"
            )
            write_log(success_message, filename)

            return result

        except Exception as e:
            # Логируем ошибку
            error_time = datetime.datetime.now()
            duration = (error_time - start_time).total_seconds()
            error_message = f"{timestamp} - {func_name} - Ошибка: {type(e).__name__}: {e}. Время: {duration:.3f}с"
            write_log(error_message, filename)

            raise

    return wrapper


def write_log(message: str, filename: Optional[str] = "log_file.html") -> None:
    """
    Записывает сообщение в HTML-файл или консоль.
    """
    if filename is None:
        # Вывод в консоль
        print(message)
    else:
        # Запись в HTML-файл
        html_message = convert_to_html(message)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(html_message + "\n")


def convert_to_html(message: str) -> str:
    """
    Конвертирует текстовое сообщение в HTML-формат.
    """
    if "Ошибка" in message:
        # Красный цвет для ошибок
        return f'<p style="color: red;">{message}</p>'
    elif "Успешно" in message:
        # Зеленый цвет для успешных операций
        return f'<p style="color: green;">{message}</p>'
    elif "Начало" in message:
        # Синий цвет для начала выполнения
        return f'<p style="color: blue;">{message}</p>'
    else:
        # Черный цвет для остальных сообщений
        return f"<p>{message}</p>"


def init_html_log(filename: str = "log_file.html") -> None:
    """
    Инициализирует HTML-файл с базовой структурой.
    """
    html_header = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Лог выполнения</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        p { margin: 5px 0; padding: 2px; }
    </style>
</head>
<body>
    <h1>Лог выполнения функций</h1>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_header)


def close_html_log(filename: str = "log_file.html") -> None:
    """
    Закрывает HTML-файл.
    """
    html_footer = """</body>
</html>"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(html_footer)
