import json
from unittest import TestCase

from tests.basetest import BaseTest


class TestModel(BaseTest, TestCase):

    def test_can_add_user(self):
        random_user = "jadedness"
        user_test = {"username": random_user, "email": random_user + "@gmail.com", "password": "SilasK@2018"}
        user_test.update({"confirm_pass": "SilasK@2018"})
        self.user_test.update({"username": random_user})
        try_post = self.client.post("/api/v1/auth/signup", data=json.dumps(user_test), content_type="application/json")
        try_login = self.client.post("/api/v1/auth/login", data=json.dumps(self.user_test),
                                     content_type="application/json")
        try_post_obj = json.loads(try_post.data)
        try_login_obj = json.loads(try_login.data)
        print(try_login_obj)
        self.assertEqual(try_post.status_code, 200)
        self.assertEqual(try_post_obj.get("message", None), "User was successfully saved login to get started")
        self.assertEqual(try_login_obj.get("message", None), "You are successfully logged in")

    def test_can_add_menu_item_admin(self):
        response = self.client.post("/api/v1/menu", data=json.dumps(self.product1.json),
                                    content_type="application/json")
        response_obj = json.loads(response.data)
        self.assertEqual(response_obj.get("message", None), "The menu item was saved successfully")
        self.assertEqual(response.status_code, 200)

    def test_cannot_add_item_without_name(self):
        response = self.client.post(self.MENU_URL, data=json.dumps(self.item_without_name),
                                    content_type="application/json")
        response_obj = json.loads(response.data)
        self.assertEqual(response_obj.get("message", None), "Please providea price, a name and a description")
        self.assertEqual(response.status_code, 403)

    def test_can_add_address(self):
        response = self.client.post("/api/v1/addresses", data=json.dumps(self.silas_address.json),
                                    content_type="application/json")
        response_obj = json.loads(response.data)
        self.assertEqual(response_obj.get("message", None), "The address was successfully added")
        self.assertEqual(response.status_code, 200)
    def test_existing_email(self):
        response = self.client.post("/api/v1/auth/signup", data=json.dumps(self.new_user),
                                    content_type="application/json")
        response1 = self.client.post("/api/v1/auth/signup", data=json.dumps(self.new_user1),
                                    content_type="application/json")
        response2 = self.client.post("/api/v1/auth/signup", data=json.dumps(self.new_user),
                                    content_type="application/json"
                                     )
        response_obj = json.loads(response.data)
        response_obj1 = json.loads(response1.data)
        response_obj2 = json.loads(response2.data)
        self.assertEqual(response_obj.get("message", None), "User was successfully saved login to get started")
        self.assertEqual(response_obj1.get("message", None), "The email already in use")
        self.assertEqual(response_obj2.get("message", None), "The username already in user")
        self.assertEqual(response.status_code, 200)
    def test_existing_menu_item(self):
        response = self.client.post("/api/v1/menu", data=json.dumps(self.product1.json),
                                    content_type="application/json")
        response1 = self.client.post("/api/v1/menu", data=json.dumps(self.product1.json),
                                    content_type="application/json")
        response_obj = json.loads(response.data)
        response_obj1 = json.loads(response1.data)
        self.assertEqual(response_obj.get("message", None), "The menu item was saved successfully")
        self.assertEqual(response_obj.get("message", None), "The menu item was saved successfully")
        self.assertEqual(response.status_code, 200)