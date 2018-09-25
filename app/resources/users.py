from flask_restful import Resource, reqparse
from app.models import User
from app.db import db
from flask_jwt_extended import (JWTManager, jwt_required)



class SignUpResource(Resource):
    """The resource class for the User model"""
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, help="Provide a username")
    parser.add_argument("email", required=True, help="Missing required email")
    parser.add_argument("password", required=True, help="Missing password")
    parser.add_argument("confirm_pass", required=True, help="Missing password confirmation")

    def post(self):
        """Create a new user to the database"""
        args = self.parser.parse_args()
        username = args.get("username", "")
        email = args.get("email", "")
        password = args.get("password", "")

        def empty(x):
            return len(x.strip()) == 0

        if empty(username) or empty(email) or empty(password):
            return {"code": "400", "message": "All fields are required"}, 200
        new_user = User(username, email, password)
        db.add_user(new_user)
        return {"ok": True, "message": "User was successfully saved login to get started",
                "data": new_user.json}, 200


class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, help="Please provide a username"
                                                        "or email address")
    parser.add_argument("password", required=True, help="Missing password")

    def post(self):
        """Get all users or a single user from the database if
        user_id is None the return all users otherwise
        just return the user with the specified user_id
        """
        users = User.all()
        # print(users)
        user = None
        if not users:
            return {"ok": False, "code":403, "message":"Invalid login credentials"}, 403
        for user in users:
            # print(user)
            if user.get("id", None) == user_id:
                return {"ok": True, "code": 200, "data": user}, 200
        if user is None:
            return {"ok": False, "message": "The user you are looking "
                                            "for doesnt exist",
                    "code": "404"}, 200
        return {"ok": True, "data": user.json}, 200
