import json
from typing import List, Any

from src.classification import Category


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
