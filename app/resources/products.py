from flask_restful import Resource, reqparse
from app.models import Product
from app.db import db
from app.utils import empty

class MenuResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True,
                        help="Missing menu item name")
    parser.add_argument("description", required=True,
                        help="Missing menu item description")
    parser.add_argument("price", required=True, help="Missing prices")

    def post(self, product_id=None):
        """A method to create a new product or
        modify one if it a product_id is specified"""
        args = MenuResource.parser.parse_args()
        product_name = args.get("name", "")
        product_description = args.get("description", "")
        unit_price = args.get("price", "")
        if empty(product_name) or empty(product_description) or empty(unit_price):
            return {"ok" : False, "code": 403, "message": "Please provide"
                                                          "a price, a name and"
                                                          " a description"}, 403
        def valid(number):
            if not isinstance(number, str):
                return False
            if not str(number).isnumeric():
                return False
            number = int(number)
            if number <= 0:
                return False
            return True
        if not valid(unit_price):
            return {"message": "The menu item should have a valid"
                               "price", "ok": False, "code": 403}, 403
        pro = Product(product_name, product_description, unit_price)
        db.add_menu_item(pro)
        return {"ok": True, "message": "The menu item was saved successfully",
                "data": pro.json}, 200

    def get(self, product_id=None):
        """Get all products or a single product if
        product_id is not None
        """
        if product_id is not None:
            order = Product.get_by_id(product_id)
            if order is None:
                return {"message": "The menu item with the id %s does not exists"% product_id}
            return {"data": order}
        products = db.menu
        if len(products) == 0:
            return {"ok": True, "code": "404",
                    "message": "No menu items are currently "
                               "available in our database"}
        res = []
        for product in products:
            res.append(products[product].json)
        return res
