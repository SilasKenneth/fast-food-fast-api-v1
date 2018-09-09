from flask_restful import Resource, reqparse
from app.models import User
from app.db import db

""" This is done in the next challenge"""


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, help="Provide a username")
    parser.add_argument("email", required=True, help="Missing required email")
    parser.add_argument("password", required=True, help="Missing password")

    def post(self):
        args = self.parser.parse_args()
        username = args.get("username")
        email = args.get("email")
        password = args.get("password")
        empty = lambda x: len(x.strip()) == 0
        if empty(username) or empty(email) or empty(password):
            return {"code": "400", "message": "All fields are required"}, 200
        new_user = User(username, email, password)
        db.add_user(new_user)
        return {"ok": True, "message": "User was successfully saved", "data": new_user.json}, 200

    def get(self, user_id=None):
        users = User.all()
        # print(users)
        if len(users) == 0:
            return {"code": "404", "message": "No user records exist in our database"}, 200
        if user_id is None:
            return {"ok": True, "data": users}, 200
        user = None
        for user in users:
            # print(user)
            if user.get("id", None)== user_id:
                return {"ok" : True, "code" : 200, "data" : user}, 200
        if user is None:
            return {"ok": False, "message": "The user you are looking for doesnt exist", "code": "404"}, 200
        return {"ok": True, "data": user.json}, 200

    def put(self, user_id):
        pass
