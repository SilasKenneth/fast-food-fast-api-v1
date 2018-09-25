import datetime
import os

import jwt
from flask_restful import Resource, reqparse

from app.db import db
from app.models import User
from app.utils import validate_username, validate_email, validate_password, empty


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

        if empty(username) or empty(email) or empty(password):
            return {"code": "400", "message": "All fields are required"}, 200
        if not validate_email(email):
            return {"message": "You have entered an invalid email address"}
        if not validate_username(username):
            return {"message": "Invalid username, a username should contain"
                               "and be between 6 to 12 characters long"}, 400
        if not validate_password(password):
            return {"message": "Please provide a valid password"
                               "a valid password contains the following"
                               "atleast one special character,"
                               "atleast one lowercase and atleast a number"
                               "and atleast should be between 6 to 12 characters"
                               "long"}
        new_user = User(username, email, password)
        db.add_user(new_user)
        db.emails.update({new_user.email: new_user.username})
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
        args = self.parser.parse_args()
        username = args.get("username", "")
        password = args.get("password", "")
        key = os.getenv("JWT_SECRET_KEY", "Hacker")
        if empty(username) or empty(password):
            return {"message": "Please provide a username or email"
                               "and a password"}
        if not users:
            return {"ok": False, "code": 403, "message": "Invalid login credentials"}, 403
        if username in db.users:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
                "iat": datetime.datetime.utcnow(),
                "data": db.users.get(username).json
            }
            token = jwt.encode(payload=payload, key=key)
            return {"token": token, "message": "You are successfuly logged in"}, 200
        if username in db.emails:
            user = db.users.get(db.emails.get(username, None), None)
            if user is None:
                return {"message": "Invalid login credentials"}, 403
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
                "iat": datetime.datetime.utcnow(),
                "data": db.users.get(username).json
            }
            token = jwt.encode(payload=payload, key=key)
            return {"token": token, "message": "You are successfully logged in"}, 200
        return {"message": "Invalid login credentials"}, 403




