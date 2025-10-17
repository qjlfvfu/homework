
class Product:
    name = str
    description = str
    price=float
    quantity=int
    """Класс описания свойств продукта"""
    def __init__(self,name,description,quantity,price):
        self.name=name
        self.quantity=quantity
        self.description=description
        self.price=price


class Category:
    """Класс категорий продукта"""
    products = []
    total_categories=0
    total_products=0
    def __init__(self,name,products,description):
        self.name=name
        self.products=products
        self.description=description
            # Автоматически обновляем атрибуты класса при создании объекта
        Category.total_categories += 1
        Category.total_products += len(products)


if __name__=="__main__":
    print(Product)



