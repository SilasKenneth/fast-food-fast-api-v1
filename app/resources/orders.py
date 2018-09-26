from flask_restful import Resource, reqparse
from app.db import db
from app.models import Order, User, Product, Address
from app.utils import empty

class OrderResource(Resource):
    parser = reqparse.RequestParser()

    def get(self, order_id=None):
        """The method to get orders from the database or a
        single order if order_id is specified"""
        if order_id is None:
            orders = Order.all()
            if not orders:
                return {"ok": False, "code": "404",
                        "message": "No orders are available yet"}, 200
            return {"ok": True, "code": "200",
                    "data": [data.json1() for data in orders]}, 200
        who_bought = db.order_maps.get(order_id, None)
        user = db.users.get(who_bought, None)
        # If the order is not associated to any user then it doesn't exist
        if who_bought is None or user is None:
            return {"ok": False, "code": "404",
                    "message": "The order requested for "
                               "doesn't exist in our database"}, 200
        """Find where a given order belongs to in an index that
        maps orders to users and positions in the users order list"""
        order_batch = user.orders
        res = []
        for order in order_batch:
            if order is not None:
                if order.id == order_id:
                    res.append(order.json)
        return res, 200

    def post(self, order_id=None):
        """A method to create a new order or modify an existing order"""

        if order_id is None or order_id == 0:
            self.parser.add_argument("user_id", required=True,
                                     help="You cannot place an order "
                                          "anonymously")
            self.parser.add_argument("address", required=True,
                                     help="Please specify an address to ship "
                                          "your order to")
            self.parser.add_argument("items", required=True,
                                     help="You cannot order nothing "
                                          "please specify some items")
            args = self.parser.parse_args()
            user_id = args.get("user_id")
            address = args.get("address")
            items = args.get("items")
            if empty(user_id) or empty(address) or empty(items):
                return {"ok": False, "code": "400",
                        "message": "Please make sure you have no missing "
                                   "requirements for an order"}, 400
            user = User.get_by_id(int(user_id))
            if user is None:
                return {"ok": False, "code": "400",
                        "message": "Could not recognize the person who's "
                                   "trying to place the order"}, 400
            add = Address.find_by_id(int(address))
            print(add)
            if add is None:
                return {"ok": False, "code": "404",
                        "message": "Could not find the specified address "
                                   "first add an address"}, 400
            items = items.split(",")

            def found(y):
                return Product.get_by_id(int(y))

            products = [found(item) for item in items if item is not None]
            products = [x for x in products if x is not None]
            prods = [product for product in products]
            if not prods:
                return {"code": "404", "ok": False,
                        "message": "The products you specified don't exist or "
                                   "you just never specified any please "
                                   "check again"}, 400
            order = Order(db.users[user].id, add)
            total = 0.00
            for p in prods:
                total += float(p.unit_price)
            order.items = prods
            order.total = total
            db.order_maps.update({order.id: user})
            db.users[user].orders.append(order)
            return {"code": 200, "ok": True,
                    "message": "You successfully placed "
                               "the order thank you", "data": order.json}
        else:
            parser = reqparse.RequestParser()
            parser.add_argument("status", required=True,
                                help="Please specify whether to accept, "
                                     "reject or mark order as complete")
            args = parser.parse_args()
            status = args.get("status")
            if len(status.strip()) == 0:
                return {"code": 400, "ok": False,
                        "message": "Please specify a valid status"}, 400
            order = db.order_maps.get(order_id)
            if order is None:
                return {"code": "404", "ok": False,
                        "message": "Couldn't find the order specified "
                                   "try another"}, 400
            for i in range(len(db.users[order].orders)):
                if db.users[order].orders[i] is not None:
                    if db.users[order].orders[i].id == order_id:
                        db.users[order].orders[i].status = status
                        return {"code": 200, "ok": True,
                                "message": "The order was successfully "
                                           "updated",
                                "data": db.users[order].orders[i].json}, 200
            return {"code": 400, "ok": False,
                    "message": "Could not find the order specified"}, 400

    def delete(self, order_id):
        """Cancel an order with a delete request"""
        user = db.order_maps.get(order_id, None)
        who = db.users.get(user, None)
        if not user or not who:
            return {"code": "404", "ok": False,
                    "message": "Incorrect order id specified. Try again"}, 400
        for i in range(len(who.orders)):
            if who.orders[i].id == order_id:
                copy = who.orders[i]
                who.orders[i] = None
                return {"code": 200, "ok": True,
                        "message": "The order was succcessfully deleted",
                        "data": copy.json}, 200
        return {"code": 400, "ok": False,
                "message": "Could not find the order specified. "
                           "Please try another"}, 400
