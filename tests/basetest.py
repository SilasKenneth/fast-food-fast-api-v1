from unittest import TestCase
from app.db  import Database, db
from app.models import (User, Address, Order, Product)
from app import create_app

class BaseTest(TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.gloria = User("gloria", "gloria@gmail.com", "gloria")
        self.silas = User("silas", "silaskenn@gmail.com", "Nyamwaro2012")
        self.daniel = User("danielotieno", "daniel@gmail.com", "dan")
        self.product1 = Product("Wet Fry", "Some yummy food", 120)
        self.product2 = Product("Boiled fish", "Some yummy Fish", 200)
        self.product3 = Product("Sushi", "Hot sushi from Japan", 300)
        self.product4 = Product("Sushi", "Hot Dog stuff cooked", 400)
        self.silas_address = Address("Kisumu", "Kibuye", "0792333333")
        self.daniel_address = Address("Kisumu", "Kondele", "0700000000")
        self.gloria_address = Address("Kericho", "Kiserian", "0728828288")
        self.silas.add_address(self.silas_address)
        self.daniel.add_address(self.daniel_address)
        self.database = db
        self.database.add_user(self.gloria)
        self.database.add_user(self.silas)
        self.database.add_user(self.daniel)
        self.test_admin = User("admin", "admin@admin.com", "admin")
        self.test_admin.is_admin = True
    def tearDown(self):
        self.database.drop()

