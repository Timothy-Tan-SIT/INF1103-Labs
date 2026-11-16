from typing import Any

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

# The JSON field that holds each product type's own value (see Product.to_dict()).
EXTRA_VALUE_FIELDS: dict[str, str] = {
    "physical": "weight",
    "digital": "download_size"
}


class ProductFactory:
    # Factory pattern: the one place that knows which concrete Product class to build.
    # The rest of the program asks the factory for a Product and only works with the
    # Product type, so it never needs to import PhysicalProduct or DigitalProduct.
    #
    # The factory itself still has to change when a new product type is added (an extra
    # elif). That is acceptable here: it is one small place, and the alternative
    # (a registry of types) would be more machinery than this application needs.

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, extra_value: float = 0.0) -> Product:
        # extra_value is the type-specific value: the weight in kg for a physical
        # product, or the download size in MB for a digital product.
        kind = product_type.strip().lower() if isinstance(product_type, str) else product_type

        if kind == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, extra_value)
        elif kind == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, extra_value)
        else:
            raise ValueError(f"Unknown product type: {product_type}")

    @staticmethod
    def create_from_dict(item: dict[str, Any], supplier: Supplier) -> Product:
        # Rebuilds a product from saved JSON data (the reverse of Product.to_dict()).
        # The knowledge of which JSON field holds the type-specific value lives here too,
        # so a new product type is still added in this one class.
        # Raises KeyError if a field is missing and ValueError if a value is invalid.
        # (Any is used only because JSON content is not known until runtime.)
        product_type = item["type"]

        if product_type not in EXTRA_VALUE_FIELDS:
            raise ValueError(f"Unknown product type: {product_type}")

        return ProductFactory.create(
            product_type, item["id"], item["name"], item["price"], item["stock"],
            supplier, item[EXTRA_VALUE_FIELDS[product_type]]
        )
