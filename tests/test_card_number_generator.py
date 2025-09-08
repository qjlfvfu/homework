import pytest
from src.generators.card_num_generator import card_number_generator


def test_unique_numbers():
    """Тестируем уникальность номеров карт"""
    generator = card_number_generator(1000, 1010)
    cards = list(generator)

    # Все номера должны быть уникальными
    assert len(cards) == 11
    assert len(set(cards)) == 11  # Все уникальны

    # Проверяем формат
    for card in cards:
        assert len(card.replace(" ", "")) == 16
        assert all(part.isdigit() for part in card.split())


def test_generator_exhaustion():
    """Тестируем корректное завершение генератора"""
    generator = card_number_generator(1, 5)
    cards = list(generator)

    assert len(cards) == 5

    # Генератор должен завершиться
    with pytest.raises(StopIteration):
        next(generator)