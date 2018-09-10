class Database(object):
    def __init__(self):
        self.users = {}
        self.order_maps = {}
        self.address_maps = {}
        self.products = {}
        self.emails = {}
        self.user_ids = {}

    def drop(self):
        """Method to clear the storage"""
        self.users = {}
        self.order_maps = {}
        self.address_maps = {}
        self.products = {}

    def add_user(self, user):
        """Method to add a user to the database"""
        self.users.update({user.username: user})
        self.emails.update({user.email: user.username})
        self.user_ids.update({user.id: user.username})

    def add_product(self, product):
        """Method to add a product to our database"""
        product.id = len(self.products) + 1
        self.products.update({len(self.products) + 1: product})

    def get_item(self, table):
        return getattr(self, table, [])


db = Database()
