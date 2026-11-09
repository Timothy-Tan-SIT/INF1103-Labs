from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    # Abstract base class for every product.
    # Manages the data common to all products. It cannot be instantiated directly:
    # a product must be a PhysicalProduct or a DigitalProduct.
    #
    # Relationship: Product --- Supplier is an ASSOCIATION. The Supplier is created
    # independently and handed to the Product; the Product only keeps a reference.

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier) -> None:
        # Private attributes (name mangled by the double underscore)
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock_quantity
        self.__supplier: Supplier = supplier

        self.__validate()

    # ----- Validation (private helper) -----

    def __validate(self) -> None:
        # Raises ValueError if any attribute holds an invalid value.
        if not isinstance(self.__product_id, str) or self.__product_id.strip() == "":
            raise ValueError("Product ID cannot be empty.")

        if not isinstance(self.__name, str) or self.__name.strip() == "":
            raise ValueError("Product name cannot be empty.")

        if isinstance(self.__price, bool) or not isinstance(self.__price, (int, float)):
            raise ValueError("Price must be a number.")

        if self.__price < 0:
            raise ValueError("Price cannot be negative.")

        self.__check_stock(self.__stock)

        if not isinstance(self.__supplier, Supplier):
            raise ValueError("Product needs a Supplier object.")

    @staticmethod
    def __check_stock(quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Stock quantity must be a whole number.")

        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

    # ----- Read-only access to the attributes -----

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    # ----- Behaviour shared by all products -----

    def update_stock(self, quantity: int) -> None:
        # Sets the stock to a new quantity.
        # Expectation set by Product (and kept by every subclass): the quantity must be
        # a whole number that is not negative, otherwise ValueError is raised.
        self.__check_stock(quantity)
        self.__stock = quantity

    def display_supplier_information(self) -> None:
        # Asks the associated Supplier to display itself.
        self.__supplier.display_information()

    def display_information(self) -> None:
        # One-line summary used when listing all products.
        # Subclasses extend this by calling super().display_information() first.
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def display_details(self) -> None:
        # Multi-line summary used when searching for one product.
        # Subclasses extend this by calling super().display_details() first.
        print("-" * 48)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.name} ({self.__supplier.supplier_id})")

    def to_dict(self) -> dict[str, object]:
        # The data common to every product, ready to be written to JSON.
        # Subclasses extend this with their own type and attributes.
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict()
        }

    # ----- Abstract behaviour: every subclass MUST implement this -----

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        # Returns a message explaining how this product reaches the customer.
        pass