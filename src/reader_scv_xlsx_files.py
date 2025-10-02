import pandas as pd


def reader_csv(file_path: str) -> list[dict]:
    """
    Функция для считывания финансовых операций из CSV.

    Args:
        file_path (str): Путь к файлу CSV

    Returns:
        list[dict]: Список словарей с транзакциями
    """
    df_csv = pd.read_csv(file_path)
    # Конвертируем DataFrame в список словарей
    transactions_csv = df_csv.to_dict("records")
    return transactions_csv


def reader_excel(file_path: str) -> list[dict]:
    """
    Функция для считывания финансовых операций из Excel.

    Args:
        file_path (str): Путь к файлу Excel

    Returns:
        list[dict]: Список словарей с транзакциями
    """
    df_xlsx = pd.read_excel(file_path)
    # Конвертируем DataFrame в список словарей
    transactions_exel = df_xlsx.to_dict("records")
    return transactions_exel
