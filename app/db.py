class Database(object):
    def __init__(self):
        self.users = {}
        self.order_maps = {}
        self.address_maps = {}
        self.menu = {}
        self.emails = {}
        self.user_ids = {}

    def drop(self):
        """Method to clear the storage"""
        self.users = {}
        self.order_maps = {}
        self.address_maps = {}
        self.menu = {}

    def add_user(self, user):
        """Method to add a user to the database"""
        self.users.update({user.username: user})
        self.emails.update({user.email: user.username})
        self.user_ids.update({user.id: user.username})

    def add_menu_item(self, menu_item):
        """Method to add a product to our database"""
        menu_item.id = len(self.menu) + 1
        self.menu.update({len(self.menu) + 1: menu_item})

    def get_item(self, table):
        return getattr(self, table, [])


db = Database()
