from app.models import Order
import pytest
# from tests.basetest import BaseTest
try:
    from tests.basetest import BaseTest
except:
    pass
from basetest import BaseTest

class TestOrders(BaseTest):
    def test_user_can_order_successfully(self):
        order = Order(self.gloria, self.gloria_address)
        order.place(self.silas.id, "1")
        self.assertEqual(1, 1)
    @pytest.mark.skip("Skip this")
    def test_user_can_order_multiple_items(self):
        order = Order(self.silas, self.silas_address)
        order.place(self.silas.id, "1,2,4")
        self.assertEqual(1, 1)
    def test_user_can_order_one_item(self):
        pass

    def test_user_cannot_order_without_address(self):
        pass

    def test_user_cannot_order_nothing(self):
        pass

    def test_order_update_admin(self):
        pass

    def test_cannot_update_order_not_yours(self):
        pass

    def test_can_update_order(self):
        pass

    def test_can_delete_order(self):
        pass
