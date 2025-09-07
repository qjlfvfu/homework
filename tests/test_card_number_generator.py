from generators.card_num_generator import card_number_generator


def test_card_number_generator():
    """Тестируем функциональность генератора"""
    generator = card_number_generator()

    # Получаем несколько номеров карт
    card1 = next(generator)
    card2 = next(generator)
    card3 = next(generator)

    print(f"Card 1: {card1}")
    print(f"Card 2: {card2}")
    print(f"Card 3: {card3}")

    # Проверяем общие свойства
    assert len(card1.replace(" ", "")) == 16
    assert len(card2.replace(" ", "")) == 16
    assert len(card3.replace(" ", "")) == 16

    # Проверяем формат
    assert len(card1.split()) == 4
    assert len(card2.split()) == 4
    assert len(card3.split()) == 4

    # Проверяем символы
    assert all(c.isdigit() or c.isspace() for c in card1)
    assert all(c.isdigit() or c.isspace() for c in card2)
    assert all(c.isdigit() or c.isspace() for c in card3)


def test_card_number_generator_multiple_calls():
    """Тестируем несколько вызовов генератора"""
    generator = card_number_generator()

    # Получаем 5 номеров карт
    results = []
    for i in range(5):
        card = next(generator)
        results.append(card)
        print(f"Карта {i + 1}: {card}")

    # Проверяем что все номера разные
    unique_cards = set(results)
    assert len(unique_cards) == 5
