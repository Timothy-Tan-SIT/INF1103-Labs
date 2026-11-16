import inspect
import unittest

from discount_strategy import (
    BulkDiscount, DiscountStrategy, NoDiscount, PercentageDiscount, StudentDiscount
)
from order import Order
from tests.helpers import make_digital, make_physical


class HalfPriceForTesting(DiscountStrategy):
    # A brand new strategy, defined here WITHOUT touching Order or any existing class.
    def apply(self, total: float) -> float:
        return total / 2


def make_order_worth_250(discount: DiscountStrategy | None = None) -> Order:
    order = Order("O-1", discount)
    order.add_order_line(make_physical(100.0), 2)   # 200
    order.add_order_line(make_digital(50.0), 1)     # 50
    return order


class TestStrategies(unittest.TestCase):
    def test_strategy_base_class_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()  # type: ignore[abstract]

    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self) -> None:
        self.assertEqual(PercentageDiscount(10).apply(250), 225)
        self.assertEqual(PercentageDiscount(0).apply(80), 80)
        self.assertEqual(PercentageDiscount(100).apply(80), 0)

    def test_bulk_discount_below_at_and_above_threshold(self) -> None:
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(199.99), 199.99)  # below: unchanged
        self.assertEqual(bulk.apply(200), 180)        # exactly at the threshold
        self.assertEqual(bulk.apply(250), 230)        # above

    def test_bulk_discount_never_goes_below_zero(self) -> None:
        self.assertEqual(BulkDiscount(0, 20).apply(5), 0)

    def test_student_discount_is_five_percent(self) -> None:
        self.assertEqual(StudentDiscount().apply(200), 190)

    def test_invalid_strategy_values_are_rejected(self) -> None:
        for make in (
            lambda: PercentageDiscount(-1),
            lambda: PercentageDiscount(101),
            lambda: PercentageDiscount("ten"),  # type: ignore[arg-type]
            lambda: BulkDiscount(-1, 20),
            lambda: BulkDiscount(200, -5),
        ):
            with self.assertRaises(ValueError):
                make()


class TestOrderUsesStrategy(unittest.TestCase):
    def test_order_without_a_strategy_uses_no_discount(self) -> None:
        order = make_order_worth_250()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250)

    def test_order_total_goes_through_the_strategy(self) -> None:
        order = make_order_worth_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_subtotal(), 250)
        self.assertEqual(order.calculate_total(), 230)

    def test_set_discount_changes_the_strategy_on_an_existing_order(self) -> None:
        order = make_order_worth_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)

        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)

    def test_set_discount_rejects_something_that_is_not_a_strategy(self) -> None:
        order = make_order_worth_250()
        with self.assertRaises(ValueError):
            order.set_discount("percentage")  # type: ignore[arg-type]

    def test_new_strategy_works_without_changing_order(self) -> None:
        order = make_order_worth_250(HalfPriceForTesting())
        self.assertEqual(order.calculate_total(), 125)

    def test_order_contains_no_discount_if_elif_logic(self) -> None:
        # Look at the code only: comments are allowed to talk about if/elif.
        source = "\n".join(
            line for line in inspect.getsource(Order).splitlines()
            if not line.strip().startswith("#")
        )
        self.assertNotIn("elif", source)
        self.assertNotIn("discount_type", source)
        self.assertNotIn("PercentageDiscount", source)
        self.assertNotIn("BulkDiscount", source)
        self.assertNotIn("StudentDiscount", source)

    def test_two_orders_can_share_one_strategy_object(self) -> None:
        # Association (not composition): the discount is used by orders, not owned.
        shared = PercentageDiscount(10)
        order_1 = make_order_worth_250(shared)
        order_2 = make_order_worth_250(shared)
        self.assertIs(order_1.discount, order_2.discount)

    def test_strategy_still_works_after_the_order_is_gone(self) -> None:
        shared = PercentageDiscount(10)
        order = make_order_worth_250(shared)
        del order
        self.assertEqual(shared.apply(100), 90)


if __name__ == "__main__":
    unittest.main()
