import json

from unittest import TestCase

from tests.basetest import BaseTest
from app.models import (User)
import string
import random


class TestModel(BaseTest, TestCase):

    def test_can_add_user(self):
        random_user = "jadedness"
        user_test = {"username":random_user, "email": random_user + "@gmail.com", "password": "SilasK@2018"}
        user_test.update({"confirm_pass": "SilasK@2018"})
        self.user_test.update({"username": random_user})
        try_post = self.client.post("/api/v1/users/signup", data=json.dumps(user_test), content_type="application/json")
        try_login = self.client.post("/api/v1/users/login", data=json.dumps(self.user_test), content_type="application/json")
        try_post_obj = json.loads(try_post.data)
        try_login_obj = json.loads(try_login.data)
        self.assertEqual(try_post.status_code, 200)
        self.assertEqual(try_post_obj.get("message", None), "User was successfully saved login to get started")
        self.assertEqual(try_login_obj.get("message", None), "You are successfully logged in")
        # print(after_save.data)

    def test_can_add_menu_item_admin(self):
        response = self.client.post("/api/v1/menu", data=json.dumps(self.product1.json), content_type="application/json")
        print(response.data)
    def test_can_add_address(self):
        address = self.silas_address
        self.silas.add_address(address)
        # To be done
