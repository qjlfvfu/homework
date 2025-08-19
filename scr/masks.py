def get_mask_card_number(card_number: int) -> int:
    """Функция которая возвращает строку после ввода  номера карты"""
    clean_card_number = card_number.replace(" ", "")
    if len(clean_card_number) != 16:
        return "Неверный ввод номера карты"
    masked_number = f"{clean_card_number[:4]} {clean_card_number[4:6]}** **** {clean_card_number[-4:]}"
    return masked_number


def get_mask_account(account_user: int) -> int:
    """Функция которая возвращает строку после ввода аккаунта"""
    masked_acc = f"**{account_user[:-4]}"
    return masked_acc
