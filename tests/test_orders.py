from app.models import Order
import json
from app.db import db
from tests.basetest import BaseTest


class TestOrders(BaseTest):
    def test_user_can_order_successfully(self):
        res = self.client.post(self.ORDER_URL,  data=json.dumps(self.single_valid), content_type="application/json")
        response = res.data
        response = json.loads(response)
        self.assertEqual(response.get("message", None), "You successfully placed the order thank you")
        self.assertEqual(res.status_code, 200)

    def test_user_can_order_multiple_items(self):
        result = self.client.post(self.ORDER_URL, data=json.dumps(self.multiple), content_type="application/json")
        response = json.loads(result.data)
        self.assertEqual(response.get("message", None), "You successfully placed the order thank you")

    def test_user_can_order_one_item(self):
        res = self.client.post(self.ORDER_URL,  data=json.dumps(self.single_valid), content_type="application/json")
        response = res.data
        response_obj = json.loads(response)
        self.assertEqual(response_obj.get("message", None), "You successfully placed the order thank you")
        self.assertEqual(res.status_code, 200)

    def test_user_cannot_order_without_address(self):
        response = self.client.post("/api/v1/orders", data=json.dumps({"user_id": 1, "items": "1,2,3", "address": ""}),
                                    content_type="application/json")
        last_order = max(db.order_maps) if len(db.order_maps) > 0 else None
        self.assertEqual(None, last_order)
        self.assertEqual(response.status_code, 400)

    def test_user_cannot_order_nothing(self):
        response = self.client.post("/api/v1/orders", data=json.dumps({"user_id": 1, "items": "", "address": "1"}),
                                    content_type="application/json")
        last_order = max(db.order_maps) if len(db.order_maps) > 0 else None
        self.assertEqual(None, last_order)
        self.assertEqual(response.status_code, 400)

    def test_order_update_admin(self):
        posted = self.client.post(self.ORDER_URL, data=json.dumps(self.single_valid), content_type="application/json")
        response = self.client.put(self.ORDER_URL+"/1", data=json.dumps({"status": "complete"}), content_type="application/json")
        response_obj = json.loads(response.data)
        posted_obj = json.loads(posted.data)
        self.assertEqual(posted.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(posted_obj.get("data", {}).get("status", None), "pending")
        self.assertEqual(response_obj.get("data", {}).get("status", None), "complete")

    def test_can_delete_order(self):
        place = self.client.post("/api/v1/orders", data=json.dumps({"user_id": "1", "items": "1,2,3", "address": "1"}),
                                 content_type="application/json")
        data = self.client.get("/api/v1/orders/1", content_type="application/json")
        response = self.client.delete("/api/v1/orders/1", content_type="application/json")
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.status_code, 200)
        self.assertEqual(place.status_code, 200)
