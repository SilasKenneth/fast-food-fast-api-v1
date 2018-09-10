import json

from unittest import TestCase

from tests.basetest import BaseTest
from app.models import (User)
import string
import random


class TestModel(BaseTest, TestCase):

    def test_can_add_user(self):
        random_user = "jadedness"
        user_test = User(random_user, random_user + "@gmail.com", "silas")
        try_post = self.client.post("/api/v1/users", data=json.dumps(user_test.json), content_type="application/json")
        after_save = self.client.get("/api/v1/users/" + str(user_test.id), content_type="application/json")
        tester = self.client.get("/api/v1/users/2", content_type="application/json")
        print(tester.data)
        self.assertEqual(user_test.username, user_test.username)
        self.assertEqual(try_post.status_code, 200)
        self.assertEqual(after_save.status_code, 200)
        # print(after_save.data)

    def test_can_add_product_if_admin(self):
        # This will be done after the auth module
        pass

    def test_can_delete_product(self):
        pass

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
        # To be done

    def test_can_delete_address(self):
        pass

    def test_can_update_address(self):
        pass
