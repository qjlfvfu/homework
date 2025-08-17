from typing import Union
from masks import get_mask_account
from datetime import datetime
def get_date(date_str):
     ''' Функция превращает вводимую дату в форматированую '''
     dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
     # Форматируем datetime в строку с нужным форматом
     return dt.strftime("%d.%m.%Y")


def account(account_info:Union[str,int] ) -> str :
    '''Функция считывает информацию о счете\карте маскируя их по разному'''
    if  "счет" in account_info.lower():
        account_number = account_info.split()[-1]
        masked_account = f"**{account_number[:-4]}"
        return f"Счет {masked_account}"
    else:
        masked_number = f"{account_info[:4]} {account_info[4:6]}** **** {account_info[-4:]}"
        return masked_number