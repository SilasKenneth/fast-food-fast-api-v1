import datetime
from app.db import db
from werkzeug.security import generate_password_hash


class Base(object):
    def update(self):
        setattr(self, "date_updated", datetime.datetime.utcnow())


class User(Base):
    """The user model class"""
    def __init__(self, username, email, password):
        """Constructor for the user class"""
        self.username = username
        self.id = db.users.get(username).id \
            if self.username in db.users else len(db.users) + 1
        self.password = generate_password_hash(password)
        self.email = email
        self.date_created = datetime.datetime.utcnow()
        self.last_update = datetime.datetime.utcnow()
        self.addresses = []
        self.is_admin = False
        self.orders = []

    def update_address(self, user_id, new_address):
        """Update a given user's address"""

        if len(self.addresses) < user_id:
            # In this case the address Id doesn't exist
            return False
        self.addresses[id - 1] = new_address
        return True

    def add_address(self, address):
        """Add an address to a given user"""
        self.addresses.append(address)
        db.address_maps.update({address.id: self.username})

    @property
    def json(self):
        """Return a JSON Serializable version of the class"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "addresses": [address.json for address in self.addresses
                          if isinstance(address, Address)]
        }

    @property
    def json_without_id(self):
        """Get A JSON Serializable version of the class without the ID field"""
        res = self.json
        del res['id']
        return res

    @classmethod
    def get_by_id(cls, user_id):
        """Get a user by an ID"""
        users = db.users
        if users is None:
            return None
        for user in users:
            if users[user].id == user_id:
                return user
        return None

    @classmethod
    def get_by_email(cls, email):
        """Get a user by email"""
        users = db.users
        if users is None:
            return None
        if email in db.emails:
            return db.users.get(db.emails.get(email, None), None)
        return None

    def delete(self):
        """Delete a user from the database"""
        del db.user_ids[self.id]
        del db.emails[self.email]
        del db.users[self.username]

    @classmethod
    def all(cls):
        """Get all users from the database"""
        users = db.get_item("users")
        # print(users)
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
        self.id = len(db.address_maps) + 1 if len(db.address_maps) > 0 else 1
        self.town = town
        self.street = street
        self.phone = phone

    @property
    def json(self):
        """Return a json serializable version of the class"""
        return {
            "id": str(self.id),
            "town": str(self.town),
            "street": str(self.street),
            "phone": str(self.phone)
        }

    @classmethod
    def find_by_id(cls, address_id):
        """Get an address by id"""
        addresses = db.address_maps
        users = db.users
        # print(addresses)
        if addresses is None:
            return None
        if address_id in addresses:
            owner = addresses[address_id]
            # print(owner)
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
    """The order model class"""

    def __init__(self, order_by, address, items=None):
        """Constructor of the order class"""
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
        """Return a JSON serializable version of the class"""
        return {
            "id": self.id,
            "order_by": self.ordered_by,
            "date_ordered": str(self.date_made),
            "address": self.address.json,
            "items": [item.json for item in self.items],
            "total": str(self.total),
            "status": str(self.status)
        }

    def json1(self):
        """Return a dictionary representation of the class without items"""
        return {
            "id": self.id,
            "order_by": self.ordered_by,
            "date_ordered": str(self.date_made).split(" ")[0],
            "total": str(self.total),
            "status": self.status
        }

    def place(self, user_id, address_id, products):
        """A method to process the placing of orders"""
        user = User.get_by_id(user_id)
        if user is None:
            return "user_not_exist"
        if products is None:
            return "no_products_selected"
        if len(products) == 0:
            return "no_products_selected"
        self.items = products

    @classmethod
    def get_by_id(cls, order_id):
        """A method to get an order based on it's id"""
        order_exist = db.order_maps.get(order_id)
        if order_exist is None:
            return None
        orders = db.users.get(order_exist, None)
        if orders is None:
            return None
        orders = orders.orders
        for order in orders:
            if order.id == order_id:
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
    """The product model class"""
    def __init__(self, product_name, product_description, unit_price):
        """Constructor for the product model"""
        self.id = len(db.menu) + 1
        self.product_name = product_name
        self.product_description = product_description
        self.last_update = datetime.datetime.utcnow()
        self.unit_price = unit_price

    @property
    def json(self):
        """Make the class json serializable"""
        return {
            "id": self.id,
            "name": self.product_name,
            "description": self.product_description,
            "price": self.unit_price
        }

    @classmethod
    def get_by_id(cls, product_id):
        """Get an item by it's id"""
        products = db.menu
        if len(products) == 0:
            return None
        for product in products:
            if products[product].id == product_id:
                return products[product]
        return None

    @classmethod
    def all(cls):
        """A method to fetch all menu items from the data structure"""
        products = db.menu
        if len(products) == 0:
            return None
        return [product.json for product in products]
