from product import Product


class OrderLine:
    # One product and the quantity of it requested in an order.
    #
    # Relationships:
    #   Order <#>--- OrderLine is COMPOSITION: an OrderLine belongs to exactly one Order,
    #   and is created by that Order (call Order.add_order_line(), never OrderLine()
    #   directly from other code).
    #   OrderLine ---> Product is an ASSOCIATION: the line refers to a Product but does
    #   not own it. The Product can exist on its own and be in an Inventory.

    def __init__(self, product: Product, quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Order quantity must be a whole number.")

        if quantity <= 0:
            raise ValueError("Order quantity must be at least 1.")

        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print(
            f"{self.__product.name} ({self.__product.product_id}) | "
            f"${self.__product.price:.2f} x {self.__quantity} = "
            f"${self.calculate_subtotal():.2f}"
        )