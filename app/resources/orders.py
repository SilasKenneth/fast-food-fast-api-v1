from flask_restful import Resource, reqparse
from app.db import db
from app.models import Order, User, Product, Address

class OrderResource(Resource):
    parser = reqparse.RequestParser()
    def get(self, order_id=None):
        if order_id is None:
            orders = Order.all()
            if not orders:
                return {"ok": False, "code": "404", "message": "No orders are available yet"}, 200
            return {"ok": True, "code": "200", "data": [data.json for data in orders]}
        who_bought = db.order_maps.get(order_id, None)
        username = db.users.get(who_bought, None)
        # If the order is not associated to any user then it doesn't exist
        if who_bought is None or username is None:
            return {"ok": False, "code": "404", "message": "The order requested for doesn't exist in our database"}, 200
        # Find where a given order belongs to in an index that maps orders to users and positions in the user's order list
        order_batch = db.users.get(username).orders
        return order_batch, 200
    def post(self, order_id=None):
        empty = lambda x: len(x.strip()) == 0
        if order_id is None:
            self.parser.add_argument("user_id", required=True, help="You cannot place an order anonymously")
            self.parser.add_argument("address", required=True, help="Please specify an address to ship your order to")
            self.parser.add_argument("items", required=True, help="You cannot order nothing please specify some items")
            args = self.parser.parse_args()
            user_id = args.get("user_id")
            address = args.get("address")
            items = args.get("items")
            if empty(user_id) or empty(address) or empty(items):
                return {"ok" : False, "code": "400", "message":"Please make sure you have no missing requirements for an order"}, 200
            user = User.get_by_id(int(user_id))
            if user is None:
                return {"ok" : False, "code": "400", "message" : "Could not recognize the person who's trying to place the order"}, 200
            add = Address.find_by_id(address)
            print(add)
            if add is None:
                return {"ok" : False, "code" : "404", "message" : "Could not find the specified address first add an address"}, 200
            items = items.split(",")
            products = [Product.get_by_id(int(item)) for item in items]
        else:
            self.parser.add_argument("status", required=True, help="Please specify whether to accept, reject or mark order as complete")
            order = Order.get_by_id(order_id)
            if order is None:
                return {"code": "404", "ok" : False, "message" : "Couldn't find the order specified try another"}, 200

