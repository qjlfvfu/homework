import json
from typing import List, Any


def test_init(sausage):
    assert sausage.name=='Колбаса'
    assert sausage.description == 'Краковская колбаса прямо из под собаки'
    assert sausage.quantity == 25
    assert sausage.price == 1.40


def test_category_init(list_category):
    assert list_category.total_products == 3
    assert list_category.name =="Мясо"
    assert list_category.description == "Грустно но вкусно"
    assert list_category.total_categories == 1



def read_test(filename: str = "products.json") -> List[Any]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print(f"Предупреждение: Данные в {filename} не являются списком")
                return []
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в {filename}: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при чтении {filename}: {e}")
        return []