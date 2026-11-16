import unittest

from digital_product import DigitalProduct
from order_line import OrderLine
from physical_product import PhysicalProduct
from tests.helpers import make_digital, make_physical, make_supplier


class TestProductValidation(unittest.TestCase):
    def test_price_must_be_greater_than_zero(self) -> None:
        for bad_price in (0, 0.0, -1, -0.01):
            with self.assertRaises(ValueError) as context:
                PhysicalProduct("P1", "Lamp", bad_price, 1, make_supplier(), 1.0)
            self.assertEqual(str(context.exception), "Price must be greater than zero.")

            with self.assertRaises(ValueError):
                DigitalProduct("D1", "Game", bad_price, 1, make_supplier(), 1.0)

    def test_price_must_be_a_real_number(self) -> None:
        for bad_price in ("12", True, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                PhysicalProduct("P1", "Lamp", bad_price, 1, make_supplier(), 1.0)  # type: ignore[arg-type]

    def test_stock_cannot_be_negative_when_creating(self) -> None:
        with self.assertRaises(ValueError):
            PhysicalProduct("P1", "Lamp", 10.0, -1, make_supplier(), 1.0)

    def test_zero_stock_is_allowed(self) -> None:
        self.assertEqual(PhysicalProduct("P1", "Lamp", 10.0, 0, make_supplier(), 1.0).stock, 0)

    def test_stock_cannot_be_negative_when_updating(self) -> None:
        for product in (make_physical(), make_digital()):
            with self.assertRaises(ValueError):
                product.update_stock(-1)

    def test_a_rejected_stock_update_changes_nothing(self) -> None:
        product = make_digital()
        original = product.stock
        with self.assertRaises(ValueError):
            product.update_stock(-5)
        self.assertEqual(product.stock, original)

    def test_digital_product_does_not_override_the_stock_rule(self) -> None:
        # Liskov: the stock rule is Product's promise, and subclasses keep it as is.
        self.assertNotIn("update_stock", DigitalProduct.__dict__)
        self.assertNotIn("update_stock", PhysicalProduct.__dict__)

    def test_weight_and_download_size_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError):
            PhysicalProduct("P1", "Lamp", 10.0, 1, make_supplier(), -1.0)
        with self.assertRaises(ValueError):
            DigitalProduct("D1", "Game", 10.0, 1, make_supplier(), -1.0)


class TestOrderLineValidation(unittest.TestCase):
    def test_quantity_must_be_greater_than_zero(self) -> None:
        for bad_quantity in (0, -1):
            with self.assertRaises(ValueError) as context:
                OrderLine(make_physical(), bad_quantity)
            self.assertEqual(str(context.exception), "Quantity must be greater than zero.")

    def test_quantity_must_be_a_whole_number(self) -> None:
        for bad_quantity in (1.5, "2", True):
            with self.assertRaises(ValueError):
                OrderLine(make_physical(), bad_quantity)  # type: ignore[arg-type]

    def test_valid_quantity_gives_the_right_subtotal(self) -> None:
        self.assertEqual(OrderLine(make_physical(100.0), 3).calculate_subtotal(), 300.0)


if __name__ == "__main__":
    unittest.main()
