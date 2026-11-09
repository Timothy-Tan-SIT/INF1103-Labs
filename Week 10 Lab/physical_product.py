from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    # A physical product IS-A Product (single class inheritance)
    # and CAN BE SHIPPED (interface).

    # Simple shipping rule: a flat base fee plus a fee per kilogram.
    BASE_SHIPPING_FEE: float = 5.00
    FEE_PER_KG: float = 2.00

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)

        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise ValueError("Weight must be a number.")

        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        self.__weight: float = weight

    @property
    def weight(self) -> float:
        return self.__weight

    # ----- Overridden methods (reuse the parent, then add weight) -----

    def display_information(self) -> None:
        super().display_information()
        print(f"    Weight: {self.__weight} kg")

    def display_details(self) -> None:
        super().display_details()
        print(f"Weight: {self.__weight} kg")

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    # ----- Abstract method from Product -----

    def get_fulfilment_info(self) -> str:
        return "Physical product: requires physical shipping."

    # ----- Abstract method from CanBeShipped -----

    def calculate_shipping_cost(self) -> float:
        return self.BASE_SHIPPING_FEE + self.FEE_PER_KG * self.__weight