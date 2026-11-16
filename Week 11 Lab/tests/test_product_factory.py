import unittest
from pathlib import Path

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from tests.helpers import make_supplier

PROJECT_FOLDER = Path(__file__).resolve().parent.parent


class TestProductFactory(unittest.TestCase):
    def test_creates_a_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, make_supplier(), 1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.weight, 1.5)  # type: ignore[attr-defined]

    def test_creates_a_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, make_supplier(), 800)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.download_size, 800)  # type: ignore[attr-defined]

    def test_factory_returns_the_product_type(self) -> None:
        for kind in ("physical", "digital"):
            product = ProductFactory.create(kind, "X1", "Thing", 5.0, 1, make_supplier())
            self.assertIsInstance(product, Product)

    def test_type_is_not_case_or_space_sensitive(self) -> None:
        product = ProductFactory.create("  Physical ", "P1", "Lamp", 25.0, 10, make_supplier())
        self.assertIsInstance(product, PhysicalProduct)

    def test_unknown_type_raises_value_error_with_a_clear_message(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Installation", 30.0, 5, make_supplier())
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_create_from_dict_rebuilds_each_type(self) -> None:
        for kind, field, value in (("physical", "weight", 2.5), ("digital", "download_size", 90.0)):
            product = ProductFactory.create(kind, "X1", "Thing", 5.0, 2, make_supplier(), value)
            rebuilt = ProductFactory.create_from_dict(product.to_dict(), make_supplier())
            self.assertIs(type(rebuilt), type(product))
            self.assertEqual(getattr(rebuilt, field), value)

    def test_create_from_dict_rejects_unknown_type_and_missing_fields(self) -> None:
        data = ProductFactory.create("physical", "X1", "Thing", 5.0, 2, make_supplier(), 1.0).to_dict()

        with self.assertRaises(ValueError):
            ProductFactory.create_from_dict({**data, "type": "service"}, make_supplier())

        del data["weight"]
        with self.assertRaises(KeyError):
            ProductFactory.create_from_dict(data, make_supplier())

    def test_other_files_do_not_create_products_directly(self) -> None:
        # Only the factory (and the product classes themselves) may call the constructors.
        for name in ("inventory_manager.py", "product_loader.py", "order.py",
                     "order_line.py", "inventory.py"):
            source = (PROJECT_FOLDER / name).read_text()
            self.assertNotIn("PhysicalProduct(", source, name)
            self.assertNotIn("DigitalProduct(", source, name)


if __name__ == "__main__":
    unittest.main()
