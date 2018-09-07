from flask_restful import Resource, reqparse
from app.models import Product
from app.db import db


class ProductResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("product_name", required=True, help="Missing product name")
    parser.add_argument("product_description", required=True, help="Missing product description")
    parser.add_argument("unit_price", required=True, help="Missing prices")

    def post(self):
        args = ProductResource.parser.parse_args()
        product_name = args.get("product_name")
        product_description = args.get("product_description")
        unit_price = args.get("unit_price")
        pro = Product(product_name, product_description, unit_price)
        db.add_product(pro)
        return {"ok": True, "message": "The product was saved successfully ", "data": pro.json}, 200

    def get(self):
        products = db.products
        if len(products) == 0:
            return {"ok": True, "code": "404", "message": "No rrecords"}
        res = []
        print(products)
        for product in products:
            res.append(products[product].json)
        return res
