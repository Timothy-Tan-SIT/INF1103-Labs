class Inventory:
    # Manages a collection of Product objects.

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        # Adds a Product object. Returns False if the ID already exists.
        if self.search_product(product.product_id) is not None:
            return False

        self.__products.append(product)
        return True

    def search_product(self, product_id):
        # Returns the Product with the given ID or None.
        for product in self.__products:
            if product.product_id.lower() == product_id.strip().lower():
                return product
        return None

    def update_stock(self, product_id, new_stock):
        # Updates the stock of a product. Returns False if it is not found.
        # Raises ValueError (from Product) if new_stock is invalid.
        product = self.search_product(product_id)

        if product is None:
            return False

        product.update_stock(new_stock)
        return True

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)

        if len(self.__products) == 0:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()

        print("-" * 48)

    def get_products(self):
        # Returns a copy of the product list (used by the save function).
        return list(self.__products)