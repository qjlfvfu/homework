import unittest
from unittest.mock import patch, Mock
import requests
from src.external_api import convert_currency, convert_from_rub, convert_to_rub


class TestConvertCurrency(unittest.TestCase):

    @patch('your_module.requests.request')
    def test_convert_currency_success(self, mock_request):
        """Тест успешной конвертации валют"""
        # Мокаем ответ API
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': 7500.0
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        result = convert_currency(100, 'USD', 'RUB')

        # Проверяем результат
        self.assertEqual(result, 7500.0)

        # Проверяем параметры вызова
        mock_request.assert_called_once_with(
            "GET",
            "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100",
            headers={"apikey": "dRqlRls7sqb8Qtbmqo8abG2skNv6gwwt"},
            data={},
            timeout=10
        )

    @patch('your_module.requests.request')
    def test_convert_currency_api_error(self, mock_request):
        """Тест обработки ошибки API"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': False,
            'error': {'info': 'Invalid API key'}
        }
        mock_request.return_value = mock_response

        result = convert_currency(100, 'USD', 'RUB')

        # При ошибке API должна вернуться исходная сумма
        self.assertEqual(result, 100.0)

    @patch('your_module.requests.request')
    def test_convert_currency_network_exception(self, mock_request):
        """Тест обработки сетевой ошибки"""
        mock_request.side_effect = requests.exceptions.RequestException("Network error")

        result = convert_currency(100, 'EUR', 'RUB')
        self.assertEqual(result, 100.0)

    @patch('your_module.requests.request')
    def test_convert_currency_timeout(self, mock_request):
        """Тест обработки таймаута"""
        mock_request.side_effect = requests.exceptions.Timeout("Timeout error")

        result = convert_currency(50, 'USD', 'EUR')
        self.assertEqual(result, 50.0)

    @patch('your_module.requests.request')
    def test_convert_currency_different_currencies(self, mock_request):
        """Тест конвертации между разными валютами"""
        mock_response = Mock()
        mock_response.json.return_value = {'success': True, 'result': 85.0}
        mock_request.return_value = mock_response

        result = convert_currency(100, 'EUR', 'USD')
        self.assertEqual(result, 85.0)

        # Проверяем URL
        called_url = mock_request.call_args[0][1]
        self.assertIn('from=EUR', called_url)
        self.assertIn('to=USD', called_url)


class TestConvertFromRub(unittest.TestCase):

    @patch('your_module.convert_currency')
    def test_convert_from_rub_usd(self, mock_convert):
        """Тест конвертации рублей в доллары"""
        mock_convert.return_value = 13.5

        result = convert_from_rub(1000, 'USD')

        self.assertEqual(result, 13.5)
        mock_convert.assert_called_once_with(1000, 'RUB', 'USD')

    @patch('your_module.convert_currency')
    def test_convert_from_rub_eur(self, mock_convert):
        """Тест конвертации рублей в евро"""
        mock_convert.return_value = 12.2

        result = convert_from_rub(1000, 'EUR')

        self.assertEqual(result, 12.2)
        mock_convert.assert_called_once_with(1000, 'RUB', 'EUR')

    def test_convert_from_rub_unsupported_currency(self):
        """Тест конвертации рублей в неподдерживаемую валюту"""
        result = convert_from_rub(1000, 'GBP')

        # Должна вернуться исходная сумма
        self.assertEqual(result, 1000.0)

    def test_convert_from_rub_unknown_currency(self):
        """Тест конвертации рублей в неизвестную валюту"""
        result = convert_from_rub(500, 'JPY')
        self.assertEqual(result, 500.0)

    @patch('your_module.convert_currency')
    def test_convert_from_rub_zero_amount(self, mock_convert):
        """Тест конвертации нулевой суммы"""
        result = convert_from_rub(0, 'USD')
        self.assertEqual(result, 0.0)
        mock_convert.assert_called_once_with(0, 'RUB', 'USD')


class TestConvertToRub(unittest.TestCase):

    @patch('your_module.convert_currency')
    def test_convert_to_rub_usd(self, mock_convert):
        """Тест конвертации USD транзакции в рубли"""
        mock_convert.return_value = 7500.0

        transaction = {'amount': 100.0, 'currency': 'USD'}
        result = convert_to_rub(transaction)

        self.assertEqual(result, 7500.0)
        mock_convert.assert_called_once_with(100.0, 'USD', 'RUB')

    @patch('your_module.convert_currency')
    def test_convert_to_rub_eur(self, mock_convert):
        """Тест конвертации EUR транзакции в рубли"""
        mock_convert.return_value = 8500.0

        transaction = {'amount': 100.0, 'currency': 'EUR'}
        result = convert_to_rub(transaction)

        self.assertEqual(result, 8500.0)
        mock_convert.assert_called_once_with(100.0, 'EUR', 'RUB')

    def test_convert_to_rub_rub(self):
        """Тест RUB транзакции (без конвертации)"""
        transaction = {'amount': 1000.0, 'currency': 'RUB'}
        result = convert_to_rub(transaction)

        self.assertEqual(result, 1000.0)

    def test_convert_to_rub_unknown_currency(self):
        """Тест транзакции с неизвестной валютой"""
        transaction = {'amount': 500.0, 'currency': 'GBP'}
        result = convert_to_rub(transaction)

        self.assertEqual(result, 500.0)

    @patch('your_module.convert_currency')
    def test_convert_to_rub_different_amounts(self, mock_convert):
        """Тест конвертации транзакций с разными суммами"""
        mock_convert.return_value = 37500.0

        transaction = {'amount': 500.0, 'currency': 'USD'}
        result = convert_to_rub(transaction)

        self.assertEqual(result, 37500.0)
        mock_convert.assert_called_once_with(500.0, 'USD', 'RUB')


class TestIntegrationScenarios(unittest.TestCase):

    @patch('your_module.requests.request')
    def test_full_conversion_flow(self, mock_request):
        """Тест полного цикла конвертации через API"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': 91.5
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Конвертируем через convert_currency
        result = convert_currency(100, 'EUR', 'USD')
        self.assertEqual(result, 91.5)

    @patch('your_module.convert_currency')
    def test_convert_from_rub_to_usd_flow(self, mock_convert):
        """Тест потока конвертации из рублей в USD"""
        mock_convert.return_value = 135.0

        # Конвертируем через convert_from_rub
        result = convert_from_rub(10000, 'USD')
        self.assertEqual(result, 135.0)
        mock_convert.assert_called_with(10000, 'RUB', 'USD')


class TestErrorHandling(unittest.TestCase):

    @patch('your_module.requests.request')
    def test_convert_currency_json_decode_error(self, mock_request):
        """Тест обработки ошибки декодирования JSON"""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        result = convert_currency(100, 'USD', 'RUB')
        self.assertEqual(result, 100.0)

    @patch('your_module.requests.request')
    def test_convert_currency_http_error(self, mock_request):
        """Тест обработки HTTP ошибки"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_request.return_value = mock_response

        result = convert_currency(100, 'USD', 'RUB')
        self.assertEqual(result, 100.0)


class TestEdgeCases(unittest.TestCase):

    def test_convert_to_rub_missing_currency_key(self):
        """Тест обработки транзакции без ключа currency"""
        with self.assertRaises(KeyError):
            convert_to_rub({'amount': 100.0})

    def test_convert_to_rub_missing_amount_key(self):
        """Тест обработки транзакции без ключа amount"""
        with self.assertRaises(KeyError):
            convert_to_rub({'currency': 'USD'})

    @patch('your_module.convert_currency')
    def test_convert_to_rub_negative_amount(self, mock_convert):
        """Тест конвертации отрицательной суммы"""
        mock_convert.return_value = -7500.0

        transaction = {'amount': -100.0, 'currency': 'USD'}
        result = convert_to_rub(transaction)

        self.assertEqual(result, -7500.0)
        mock_convert.assert_called_once_with(-100.0, 'USD', 'RUB')

    def test_convert_from_rub_case_sensitivity(self):
        """Тест чувствительности к регистру валют"""
        result = convert_from_rub(1000, 'usd')  # lowercase
        self.assertEqual(result, 1000.0)  # Должна вернуть исходную сумму


if __name__ == '__main__':
    unittest.main()