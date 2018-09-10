from flask_restful import Resource, reqparse
from app.models import Address, User
from app.db import db
from flask import jsonify


class AddressResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("town", required=True, help="Missing the town name")
    parser.add_argument("street", required=True,
                        help="Please specify a street its required")
    parser.add_argument("phone", required=True,
                        help="Please specify a phone number")

    def get(self, address_id=None):
        """Get all addresses or just a single one if
         the address_id is specified"""
        if address_id is None:
            users = db.users
        else:
            address = Address.find_by_id(address_id)
            if address is None:
                return {"code": "404", "message": "The address was not "
                                                  " found in our database"}, \
                       200
            return {"ok": True, "code": "200", "data": address.json}, 200

        res = []
        if not users:
            return {"code": "404", "message": "No addresses were "
                                              "found in the database"}, 200
        for user in users:
            res += users[user].addresses
        if len(res) == 0:
            return {"code": "404", "message": "No addresses were "
                                              "found in the database"}, 200
        return {"ok": True, "data": [address.json for address in res]}, 200

    def post(self, address_id=None):
        args = self.parser.parse_args()
        town = args.get("town")
        street = args.get("street")
        phone = args.get("phone")

        def empty(st):
            return len(st.strip()) == 0

        if empty(town) or empty(street) or empty(phone):
            return {"code": "500", "message": "Please provide all the details "
                                              "needed don't leave blanks"}, 200
        address = Address(town, street, phone)
        user = User.get_by_id(1)
        if user is None:
            return {"code": "404", "message": "Please become a "
                                              "valid user", "ok": False}
        db.users[db.users[user].username].add_address(address)
        db.address_maps.update({address.id: db.users[user].username})
        return {"code": "231", "message": "The address was successfully "
                                          "added", "data": address.json}
