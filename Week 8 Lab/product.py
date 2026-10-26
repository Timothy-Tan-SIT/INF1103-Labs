class Product:

    def __init__(self, product_id, name, price, stock):
        # Private attributes
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

        self.__validate()

    # ----- Validation -----

    def __validate(self):
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

    @staticmethod
    def __check_stock(quantity):
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Stock quantity must be a whole number.")

        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

    # ----- Read-only access to the attributes -----

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    # ----- Behaviour -----

    def update_stock(self, quantity):
        # Sets the stock to a new quantity.
        # The Product decides what counts as a valid value.
        self.__check_stock(quantity)
        self.__stock = quantity

    def display_information(self):
        # One-line summary used when listing all products.
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def display_details(self):
        # Multi-line summary used when searching for one product.
        print("-" * 48)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print("-" * 48)