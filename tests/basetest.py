from unittest import TestCase
from app.db import  db
from app import create_app


class BaseTest(TestCase):
    def setUp(self):
        self.app = create_app("testing")
        with self.app.app_context():
            from app.models import (User, Address, Product, Order)
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
        self.test_admin = User("admin", "admin@admin.com", "admin")
        self.database.add_product(self.product1)
        self.database.add_product(self.product2)
        self.database.add_product(self.product3)
        self.database.add_product(self.product4)
        self.database.add_user(self.silas)
        self.silas.add_address(self.silas_address)
        self.test_admin.is_admin = True

    def tearDown(self):
        self.database.drop()

