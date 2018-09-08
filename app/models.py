import datetime
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class Base(object):
    def update(self):
        setattr(self, "date_updated", datetime.datetime.utcnow())


class User(Base):
    def __init__(self, username, email, password):
        self.username = username
        self.id = db.users.get(username).id if self.username in db.users else len(db.users) + 1
        self.password = generate_password_hash(password)
        self.email = email
        self.date_created = datetime.datetime.utcnow()
        self.last_update = datetime.datetime.utcnow()
        self.addresses = []
        self.is_admin = False
        self.orders = []

    def update_address(self, id, new_address):
        if len(self.addresses) < id:  # In this case the address Id doesn't exist
            return False
        self.addresses[id - 1] = new_address
        return True

    def add_address(self, address):
        self.addresses.append(address)

    @property
    def json(self):
        dummy_address = Address("Fake town", "Fake street", "01929292")
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "addresses": [address.json for address in self.addresses if type(address) == type(dummy_address)]
        }

    @property
    def json_without_id(self):
        res = self.json
        del res['id']
        return res

    @classmethod
    def get_by_id(cls, user_id):
        users = db.users
        if users is None:
            return None
        for user in users:
            if users[user].id == user_id:
                return user
        return None

    @classmethod
    def get_by_email(cls, email):
        users = db.get_item("users")
        if users is None:
            return None
        if email in db.get_item("emails"):
            return db.users.get(db.emails.get(email, None), None)
        return None

    def save(self):
        if self.email in db.emails:
            return "user_already_exist"

    def delete(self):
        del db.user_ids[self.id]
        del db.emails[self.email]
        del db.users[self.username]

    @classmethod
    def all(cls):
        users = db.get_item("users")
        print(users)
        if users == []:
            return []
        res = []
        for user in users:
            res.append(users[user].json)
        return res


class Address(Base):
    """ This is the address model to cater for user addresses. """

    def __init__(self, town, street, phone):
        """ Constructor for the model class"""
        self.id = max(db.address_maps) + 1 if len(db.address_maps) > 0 else 1
        self.town = town
        self.street = street
        self.phone = phone

    @property
    def json(self):
        return {
            "id": str(self.id),
            "town": str(self.town),
            "street": str(self.street),
            "phone": str(self.phone)
        }

    @classmethod
    def find_by_id(cls, address_id):
        addresses = db.address_maps
        users = db.users
        print(addresses)
        if addresses is None:
            return None
        if address_id in addresses:
            owner = addresses[address_id]
            print(owner)
            if owner not in users:
                return None
            current_addresses = users[owner].addresses
            if current_addresses is None:
                return None
            if len(current_addresses) == 0:
                return None
            for address in current_addresses:
                if address.id == address_id:
                    return address
        return None


class Order(object):
    def __init__(self, order_by, address):
        self.id = max(db.order_maps) + 1 if len(db.order_maps) > 0 else 1
        self.ordered_by = order_by
        self.date_made = datetime.datetime.utcnow()
        self.last_update = datetime.datetime.utcnow()
        self.address = address
        self.items = []
        self.total = 0.00
        self.status = "pending"

    @property
    def json(self):
        return {
            "id": self.id,
            "order_by": self.ordered_by,
            "date_ordered": str(self.date_made),
            "address": self.address.json,
            "items" : [item.json for item in self.items],
            "total" : str(self.total),
            "status" : str(self.status)
        }

    def json1(self):
        return {
            "id": self.id,
            "order_by": self.ordered_by,
            "date_ordered": str(self.date_made).split(" ")[0],
            "total" : str(self.total),
            "status" : self.status
        }

    def place(self, user_id, address_id, products):
        user = User.get_by_id(user_id)
        if user is None:
            return "user_not_exist"
        if products is None:
            return "no_products_selected"
        if len(products) == 0:
            return "no_products_selected"
        clean_products = []
        self.items = products

    @classmethod
    def get_by_id(cls, id):
        order_exist = db.order_maps.get(id)
        if order_exist is None:
            return None
        orders = db.users.get(order_exist, None)
        if orders is None:
            return None
        orders = orders.orders
        for order in orders:
            if order.id == id:
                return order
        return None

    @classmethod
    def all(cls):
        """A method to get all orders from the database"""
        users = db.users
        if not users:
            return None
        res = []
        for user in users:
            res += users[user].orders
        return res


class Product(object):

    def __init__(self, product_name, product_description, unit_price):
        """Constructor for the product model"""
        self.id = len(db.products) + 1
        self.product_name = product_name
        self.product_description = product_description
        self.last_update = datetime.datetime.utcnow()
        self.unit_price = unit_price

    @property
    def json(self):
        """Make the class json serializable"""
        return {
            "id": self.id,
            "product_name": self.product_name,
            "product_description": self.product_description,
            "unit_price": self.unit_price
        }

    @classmethod
    def get_by_id(cls, id):
        products = db.products
        if len(products) == 0:
            return None
        for product in products:
            if products[product].id == id:
                return products[product]
        return None

    @classmethod
    def all(cls):
        products = db.products
        if len(products) == 0:
            return None
        return [product.json for product in products]
