import json
import logging
import os
from typing import Dict, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "utils.log")
# Настройка логгера
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_formater = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s-%(lineno)d")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает данные из JSON-файла.

    Args:
        file_path (str): Путь до JSON-файла

    Returns:
        List[Dict]: Список словарей с данными транзакций или пустой список
    """
    try:
        logger.info("Запускаем чтение файла")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info("считываем файл")
                return data
            else:
                return []
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return []
    except json.JSONDecodeError:
        print(f"Файл {file_path} содержит невалидный JSON или пуст")
        return []
    except Exception as e:
        logger.error(f"Произошла ошибка при чтении файла: {e}")
        return []
