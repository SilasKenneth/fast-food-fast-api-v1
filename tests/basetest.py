from unittest import TestCase
from app.db import db
from app import create_app


class BaseTest(TestCase):
    def setUp(self):
        self.app = create_app("testing")
        with self.app.app_context():
            from app.models import (User, Address, Product)
        self.client = self.app.test_client()
        self.gloria = User("gloria", "gloria@gmail.com", "gloria")
        self.silas = User("silas", "silaskenn@gmail.com", "Nyamwaro2012")
        self.daniel = User("danielotieno", "daniel@gmail.com", "dan")
        self.product1 = Product("Wet Fry", "Some yummy food", 120)
        self.product2 = Product("Boiled fish", "Some yummy Fish", 200)
        self.product3 = Product("Sushi", "Hot sushi from Japan", 300)
        self.product4 = Product("Koria", "Hot Dog stuff cooked", 400)
        self.silas_address = Address("Kisumu", "Kibuye", "0792333333")
        self.daniel_address = Address("Kisumu", "Kondele", "0700000000")
        self.gloria_address = Address("Kericho", "Kiserian", "0728828288")
        self.database = db
        self.multiple = {
            "user_id" : "1",
            "items": "1,2,3",
            "address": "1"
        }
        self.single_valid = {
            "user_id": "1",
            "items": "1",
            "address": "1"
        }
        self.sing_with_missing_address = {
            "address": "",
            "items": "1",
            "user_id": "1"
        }
        self.test_address = {
            "town": "Kisumu",
            "phone": "0791350402",
            "street": "Kondele"
        }
        self.item_without_name = {
            "name": "",
            "description": "Sushi from Japan",
            "price": 300
        }
        self.new_user = {
           "username":"jameskey",
           "email": "jameskey@gmail.com",
           "password": "SilasK@2019",
           "confirm_pass": "SilasK@2019"
        }
        self.new_user1 = {
           "username":"jameskeys",
           "email": "jameskey@gmail.com",
           "password": "SilasK@2019",
           "confirm_pass": "SilasK@2019"
        }
        self.user_test = {"username": "silaskenn", "password": "SilasK@2018"}
        self.ORDER_URL = "/api/v1/orders"
        self.MENU_URL = "/api/v1/menu"
        self.test_admin = User("admin", "admin@admin.com", "admin")
        self.database.add_menu_item(self.product2)
        self.database.add_menu_item(self.product3)
        self.database.add_menu_item(self.product4)
        self.silas.add_address(self.silas_address)
        self.database.add_user(self.silas)
        self.silas.add_address(self.silas_address)
        self.test_admin.is_admin = True

    def tearDown(self):
        self.database.drop()

