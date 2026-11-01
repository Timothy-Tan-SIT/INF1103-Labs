from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    # A physical product IS-A Product (single class inheritance)
    # and CAN BE SHIPPED (interface).

    # Simple shipping rule: a flat base fee plus a fee per kilogram.
    BASE_SHIPPING_FEE = 5.00
    FEE_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)

        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise ValueError("Weight must be a number.")

        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    # ----- Overridden methods (reuse the parent, then add weight) -----

    def display_information(self):
        super().display_information()
        print(f"    Weight: {self.__weight} kg")

    def display_details(self):
        super().display_details()
        print(f"Weight: {self.__weight} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    # ----- Abstract method from Product -----

    def get_fulfilment_info(self):
        return "Physical product: requires physical shipping."

    # ----- Abstract method from CanBeShipped -----

    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING_FEE + self.FEE_PER_KG * self.__weight
