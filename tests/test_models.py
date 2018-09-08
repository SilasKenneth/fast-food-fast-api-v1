from basetest import BaseTest
from unittest import TestCase
try:
    from tests.basetest import BaseTest
except:
    pass
from app.models import (User, Product, Address,Order)
from app.db import db
import string
import random
class TestModel(BaseTest, TestCase):
    
    def test_can_add_user(self):
        random_user = "".join([random.choice(string.ascii_lowercase) for i in range(10)])
        user_test = User(random_user, random_user + "gmail.com", "silas")
        db.add_user(user_test)
        user_after_add = User.get_by_email(user_test.email)
        self.assertNotEqual(user_after_add, None)
        self.assertEqual(user_after_add.username, user_test.username)

    def test_can_add_product_if_admin(self):
        pass

    def test_can_delete_product(self):
        product = Product("Sushi", "Some nice sushi from Japan", 1002)
        

    def test_can_update_product(self):
        pass

    def test_can_update_user(self):
        pass

    def test_can_udpate_product(self):
        pass

    def test_can_not_update_product_not_admin(self):
        pass

    def test_can_add_address(self):
        address = self.silas_address
        self.silas.add_address(address)
        self.assertEqual(1, 1)

    def test_can_delete_address(self):
        pass

    def test_can_update_address(self):
        pass