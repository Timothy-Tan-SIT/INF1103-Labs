from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    # A customer order, made up of OrderLine objects.
    #
    # Relationships:
    #   Order <#>--- OrderLine is COMPOSITION: the Order creates and manages its lines.
    #   Order ------> DiscountStrategy is an ASSOCIATION: the discount is something the
    #   order USES, not a part of it, so two orders can share the same strategy object.
    #
    # Strategy pattern: the Order is GIVEN a discount strategy and only calls apply().
    # There is no if/elif about discount types here.

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        if not isinstance(order_id, str) or order_id.strip() == "":
            raise ValueError("Order ID cannot be empty.")

        self.__order_id: str = order_id.strip()
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = NoDiscount()

        if discount is not None:
            self.set_discount(discount)

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        # A copy of the list, so outside code cannot add or remove lines directly.
        return list(self.__order_lines)

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        # Swaps the strategy, e.g. when a customer qualifies for a different discount.
        if not isinstance(discount, DiscountStrategy):
            raise ValueError("Discount must be a DiscountStrategy.")

        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order itself creates the OrderLine: it is never passed in from outside.
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        # Removes the first line for the given product ID. The line is destroyed with
        # the removal; the Product it referred to is not affected.
        for order_line in self.__order_lines:
            if order_line.product.product_id.lower() == product_id.strip().lower():
                self.__order_lines.remove(order_line)
                return True
        return False

    def calculate_subtotal(self) -> float:
        # The total of the order lines before any discount.
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        # Adds up the line subtotals, then lets the strategy decide the final amount.
        return self.__discount.apply(self.calculate_subtotal())

    def display_information(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 48)

        if len(self.__order_lines) == 0:
            print("No items in this order.")
        else:
            for order_line in self.__order_lines:
                order_line.display_information()

        subtotal = self.calculate_subtotal()
        total = self.calculate_total()

        print("-" * 48)
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Discount: -${subtotal - total:.2f}")
        print(f"Total: ${total:.2f}")
