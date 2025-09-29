from unittest.mock import Mock, patch

from src.external_api import convert_currency, convert_from_rub, convert_to_rub


def test_convert_usd_to_rub_success():
    """Тест успешной конвертации долларов в рубли"""
    with patch("src.external_api.requests.request") as mock_request:
        # Настраиваем мок ответа API
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": 7500.0}  # 100 USD = 7500 RUB
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Вызываем функцию конвертации
        result = convert_currency(100, "USD", "RUB")

        # Проверяем результат
        assert result == 7500.0

        # Проверяем, что API вызвался с правильными параметрами
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        url = call_args[0][1]
        assert "from=USD" in url
        assert "to=RUB" in url
        assert "amount=100" in url
        print("✓ USD в RUB конвертируется правильно")


def test_convert_eur_to_usd_success():
    """Тест успешной конвертации евро в доллары"""
    with patch("src.external_api.requests.request") as mock_request:
        # Настраиваем мок ответа API
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": 110.0}  # 100 EUR = 110 USD
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Вызываем функцию конвертации
        result = convert_currency(100, "EUR", "USD")

        # Проверяем результат
        assert result == 110.0

        # Проверяем параметры вызова
        mock_request.assert_called_once()
        url = mock_request.call_args[0][1]
        assert "from=EUR" in url
        assert "to=USD" in url
        print("✓ EUR в USD конвертируется правильно")


if __name__ == "__main__":
    test_convert_usd_to_rub_success()
    test_convert_eur_to_usd_success()
    print("Все тесты пройдены! 🎉")


def test_convert_usd_to_rub():
    """Минимальный тест: USD → RUB"""

    with patch("src.external_api.convert_currency") as mock_convert:
        mock_convert.return_value = 7500.0
        transaction = {"amount": 100, "currency": "USD"}
        result = convert_to_rub(transaction)
        assert result == 7500.0
        print("✓ Тест пройден!")


if __name__ == "__main__":
    test_convert_usd_to_rub()


def test_convert_rub_to_usd():
    """Минимальный тест: RUB → USD"""

    with patch("src.external_api.convert_currency") as mock_convert:
        mock_convert.return_value = 13.5

        result = convert_from_rub(1000, "USD")

        assert result == 13.5
        print("✓ Тест пройден!")


if __name__ == "__main__":
    test_convert_rub_to_usd()
