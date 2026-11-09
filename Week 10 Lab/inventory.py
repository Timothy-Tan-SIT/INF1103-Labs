from product import Product


class Inventory:
    # Manages a collection of Product objects.
    #
    # Relationship: Inventory <>--- Product is an AGGREGATION.
    # The Inventory keeps references to products but does not create them or own their
    # lifecycle: a Product exists before it is added, and survives being removed
    # (it can even be added to a different Inventory).
    #
    # It only calls methods every Product has (it never checks for a subclass),
    # so any Product subclass can be substituted (Liskov Substitution Principle).

    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        # A copy of the list, so outside code cannot change the collection directly.
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        # Adds an existing Product object. Returns False if the ID already exists.
        if self.find_product(product.product_id) is not None:
            return False

        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        # Removes the matching Product reference from this inventory.
        # The Product itself is NOT destroyed: it is returned, so it can still be used
        # or added to another Inventory. Returns None if no product matches.
        product = self.find_product(product_id)

        if product is None:
            return None

        self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        # Returns the Product with the given ID (case-insensitive), or None.
        for product in self.__products:
            if product.product_id.lower() == product_id.strip().lower():
                return product
        return None

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        # Updates the stock of a product. Returns False if it is not found.
        # Raises ValueError (from Product) if new_stock is invalid.
        product = self.find_product(product_id)

        if product is None:
            return False

        product.update_stock(new_stock)
        return True

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)

        if len(self.__products) == 0:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()

        print("-" * 48)