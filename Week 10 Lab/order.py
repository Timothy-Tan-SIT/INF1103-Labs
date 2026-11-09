from order_line import OrderLine
from product import Product


class Order:
    # A customer order, made up of OrderLine objects.
    #
    # Relationship: Order <#>--- OrderLine is COMPOSITION.
    # The Order creates and manages its own OrderLine objects (see add_order_line).
    # The lines belong to this order only and are never handed out to be reused in
    # another order: if the Order goes away, so do its lines.

    def __init__(self, order_id: str) -> None:
        if not isinstance(order_id, str) or order_id.strip() == "":
            raise ValueError("Order ID cannot be empty.")

        self.__order_id: str = order_id.strip()
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        # A copy of the list, so outside code cannot add or remove lines directly.
        return list(self.__order_lines)

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

    def calculate_total(self) -> float:
        # Asks each OrderLine for its own subtotal.
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 48)

        if len(self.__order_lines) == 0:
            print("No items in this order.")
        else:
            for order_line in self.__order_lines:
                order_line.display_information()

        print("-" * 48)
        print(f"Total: ${self.calculate_total():.2f}")