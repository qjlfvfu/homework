import random
from typing import Generator


def card_number_generator(start: int = 1, stop: int = 9999999999999999) -> Generator[str, None, None]:
    """
    Генератор уникальных номеров банковских карт в заданном диапазоне.

    Args:
        start: Начальный номер карты (по умолчанию 1)
        stop: Конечный номер карты (по умолчанию 9999999999999999)

    Yields:
        str: Отформатированный уникальный номер карты (XXXX XXXX XXXX XXXX)

    Raises:
        ValueError: Если start > stop или диапазон исчерпан
    """
    if start > stop:
        raise ValueError("start не может быть больше stop")

    if start < 1 or stop > 9999999999999999:
        raise ValueError("Диапазон должен быть от 1 до 9999999999999999")

    # Генерируем все возможные номера в диапазоне и перемешиваем
    total_numbers = stop - start + 1
    numbers = list(range(start, stop + 1))
    random.shuffle(numbers)  # Перемешиваем для случайного порядка

    for number in numbers:
        # Форматируем номер карты
        digit_str = str(number).zfill(16)
        card_number = f"{digit_str[:4]} {digit_str[4:8]} {digit_str[8:12]} {digit_str[12:16]}"
        yield card_number
