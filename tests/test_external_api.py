from unittest.mock import Mock, patch

import requests

from src.external_api import convert_currency


def test_convert_currency():
    result = convert_currency(1500, "RUB", "USD,EUR")

    if result and result["success"]:
        print("✅ Конвертация успешна!")
        print(f"💵 Исходная сумма: {result['query']['amount']} {result['query']['from']}")
        print(f"🔁 Курс на дату: {result['date']}")
        print("📊 Результаты:")

        # Если конвертируем в несколько валют
        if isinstance(result["result"], dict):
            for currency, amount in result["result"].items():
                print(f"   {currency}: {amount:.2f}")
        else:
            print(f"   {result['query']['to']}: {result['result']:.2f}")

    else:
        print("❌ Ошибка конвертации")
        if result:
            print(f"Код ошибки: {result.get('error', {}).get('code', 'Unknown')}")


@patch("requests.get")
def test_get_currency_with_mock(mock_requests, currency_data):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    mock_requests.return_value = mock_response
    API_KEY = {"apikey": "88005553535niG"}
    resp = requests.get(url="https://api.apilayer.com/currency_data/convert", headers=API_KEY, params=currency_data[2])

    assert resp.status_code == 200
    assert resp.json()["result"] == "success"

    mock_requests.assert_called_once_with(
        url="https://api.apilayer.com/currency_data/convert", headers=API_KEY, params=currency_data[2]
    )


def test_get_currency():
    if __name__ == "__main__":
        result = convert_currency(1000, "RUB", "USD,EUR")
        if result:
            print("✅ Конвертация успешна!")
            print(f"Результат: {result}")
        else:
            print("❌ Ошибка конвертации")


def test_get_currency_anytime(currency_data):
    if __name__ == "__main__":
        result1 = convert_currency(currency_data[0])
        result2 = convert_currency(currency_data[1])
        print(result1, result2)
