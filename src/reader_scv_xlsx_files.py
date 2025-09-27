import csv
import pandas as pd


def reader_csv():
    """Функция считывает данные с csv файла"""
    df_csv=pd.read_csv("transactions.csv")
    return df_csv


def reader_excel():
    """Функция считывает данные с html файла"""
    df_xlsx= pd.read_excel("transactions_excel.xlsx")
    return df_xlsx