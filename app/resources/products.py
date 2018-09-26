from flask_restful import Resource, reqparse
from app.models import Product
from app.db import db


class MenuResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True,
                        help="Missing menu item name")
    parser.add_argument("description", required=True,
                        help="Missing menu item description")
    parser.add_argument("unit_price", required=True, help="Missing prices")

    def post(self, product_id=None):
        """A method to create a new product or
        modify one if it a product_id is specified"""
        args = MenuResource.parser.parse_args()
        product_name = args.get("name")
        product_description = args.get("description")
        unit_price = args.get("price")
        pro = Product(product_name, product_description, unit_price)
        db.add_menu_item(pro)
        return {"ok": True, "message": "The menu item was saved successfully ",
                "data": pro.json}, 200

    def get(self, product_id=None):
        """Get all products or a single product if
        product_id is not None
        """
        products = db.products
        if len(products) == 0:
            return {"ok": True, "code": "404",
                    "message": "No menu items are currently "
                               "available in our database"}
        res = []
        for product in products:
            res.append(products[product].json)
        return res
