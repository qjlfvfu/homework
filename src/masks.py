import logging
import os
from typing import List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "masks.log")
logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_formater = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def get_mask_card_number(card_info: str) -> str:
    """Функция, которая возвращает строку после ввода номера карты"""
    parts: List[str] = card_info.split()
    card_number = parts[-1]
    if len(card_number) != 16:
        logger.error("Не то количество цифр в номере карты")
        return "Неверный ввод номера карты"
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked_number


def get_mask_account(account_info: str) -> str:
    """Функция, которая возвращает строку после ввода аккаунта"""
    parts = account_info.split()
    logger.info("разделяем данные")
    if len(parts) < 2:
        logger.warning("найдена только 1 часть?!")
        return account_info
    account_type = " ".join(parts[:-1])
    account_number = parts[-1]
    masked_number = "**" + account_number[-4:]
    if len(account_number) < 4:
        masked_number = (len(account_number) - 1) * "*" + account_number[-1:]
        logger.info("Это последние цифры ВАШЕГО аккаунта?")
    return f"{account_type} {masked_number}"
