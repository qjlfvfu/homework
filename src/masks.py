from typing import List


def get_mask_card_number(card_info: str) -> str:
    """Функция, которая возвращает строку после ввода номера карты"""
    parts: List[str] = card_info.split()
    card_number = parts[-1]
    if len(card_number) != 16:
        return "Неверный ввод номера карты"
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked_number


def get_mask_account(account_info: str) -> str:
    """Функция, которая возвращает строку после ввода аккаунта"""
    parts = account_info.split()
    account_number = parts[-1]
    masked_acc = f"**{account_number[:-4]}"
    account_type = " ".join(parts[:-1])
    return f"{account_type} {masked_acc}"
