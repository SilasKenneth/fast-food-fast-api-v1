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
            return {"ok": True, "code": "200", "data": [data.json1() for data in orders]}, 200
        who_bought = db.order_maps.get(order_id, None)
        user = db.users.get(who_bought, None)
        # If the order is not associated to any user then it doesn't exist
        if who_bought is None or user is None:
            return {"ok": False, "code": "404", "message": "The order requested for doesn't exist in our database"}, 200
        """
        Find where a given order belongs to in an index that maps orders to users and positions in the user's order
        list
        """
        order_batch = user.orders
        res = []
        for order in order_batch:
            if order.id == order_id:
                res.append(order.json)
        return res, 200

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
                return {"ok": False, "code": "400",
                        "message": "Please make sure you have no missing requirements for an order"}, 200
            user = User.get_by_id(int(user_id))
            if user is None:
                return {"ok": False, "code": "400",
                        "message": "Could not recognize the person who's trying to place the order"}, 200
            add = Address.find_by_id(int(address))
            print(add)
            if add is None:
                return {"ok": False, "code": "404",
                        "message": "Could not find the specified address first add an address"}, 200
            items = items.split(",")

            def found(y):
                return Product.get_by_id(int(y))

            products = [found(item) for item in items if item is not None]
            products = [x for x in products if x is not None]
            prods = [product for product in products]
            if not prods:
                return {"code": "404", "ok": False,
                        "message": "The products you specified don't exist or you just never specified any please "
                                   "check again"}, 200
            order = Order(db.users[user].id, add)
            total = 0.00
            for p in prods:
                total += float(p.unit_price)
            order.items = prods
            order.total = total
            db.order_maps.update({order.id: user})
            db.users[user].orders.append(order)
        else:
            self.parser.add_argument("status", required=True,
                                     help="Please specify whether to accept, reject or mark order as complete")
            order = Order.get_by_id(order_id)
            if order is None:
                return {"code": "404", "ok": False, "message": "Couldn't find the order specified try another"}, 200
