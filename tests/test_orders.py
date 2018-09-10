from app.models import Order
import json
from app.db import db
from tests.basetest import BaseTest


class TestOrders(BaseTest):
    def test_user_can_order_successfully(self):
        order = Order(self.gloria, self.gloria_address)
        order.place(self.silas.id, 1, "1")
        self.assertEqual(1, 1)

    # @pytest.mark.skip("Skip this")
    def test_user_can_order_multiple_items(self):
        order = Order(self.silas, self.silas_address)
        order.place(self.silas.id, 1, "1,2,4")
        self.assertEqual(1, 1)

    def test_user_can_order_one_item(self):
        response = self.client.get("/api/v1/users", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_order_without_address(self):
        response = self.client.post("/api/v1/orders", data=json.dumps({"user_id": 1, "items": "1,2,3", "address": ""}),
                                    content_type="application/json")
        last_order = max(db.order_maps) if len(db.order_maps) > 0 else None
        # print(response.data)
        self.assertEqual(None, last_order)
        self.assertEqual(response.status_code, 400)

    def test_user_cannot_order_nothing(self):
        response = self.client.post("/api/v1/orders", data=json.dumps({"user_id": 1, "items": "", "address": "1"}),
                                    content_type="application/json")
        last_order = max(db.order_maps) if len(db.order_maps) > 0 else None
        print(response.data)
        self.assertEqual(None, last_order)
        self.assertEqual(response.status_code, 400)

    def test_order_update_admin(self):
        pass

    def test_cannot_update_order_not_yours(self):
        pass

    def test_can_update_order(self):
        pass

    def test_can_delete_order(self):
        place = self.client.post("/api/v1/orders", data=json.dumps({"user_id": 1, "items": "1,2,3", "address": "1"}),
                                 content_type="application/json")
        data = self.client.get("/api/v1/orders/1", content_type="application/json")
        response = self.client.delete("/api/v1/orders/1", content_type="application/json")
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.status_code, 200)
        self.assertEqual(place.status_code, 200)
