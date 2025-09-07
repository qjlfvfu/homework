import random


def card_number_generator(start=1,stop=9999999999999999):
    """Генератор номеров банковских карт"""
    while True:
        # Генерируем случайное число
        random_digit = random.randint(start, stop)
        digit_str = str(random_digit).zfill(16)
        # Форматируем номер карты
        card_number = f"{digit_str[:4]} {digit_str[4:8]} {digit_str[8:12]} {digit_str[12:16]}"

        # Возвращаем результат
        yield card_number
