import unittest
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestMainBasic(unittest.TestCase):

    def test_main_exists(self):
        """Просто проверяем что main импортируется и является функцией"""
        try:
            from src.main import main
            self.assertTrue(callable(main))
            print("✓ main успешно импортирована")
        except ImportError as e:
            self.fail(f"Не удалось импортировать main: {e}")

    def test_main_output(self):
        """Тестируем вывод при неверном вводе"""
        from src.main import main

        with unittest.mock.patch('builtins.input', return_value='5'):
            with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("Неверный ввод", output)

    def test_imports_work(self):
        """Проверяем что все модули импортируются"""
        modules_to_test = [
            'src.utils',
            'src.processing',
            'src.search_counter',
            'src.reader_scv_xlsx_files'
        ]

        for module_name in modules_to_test:
            try:
                __import__(module_name)
                print(f"✓ {module_name} импортирован успешно")
            except ImportError as e:
                self.fail(f"Не удалось импортировать {module_name}: {e}")


if __name__ == '__main__':
    unittest.main()