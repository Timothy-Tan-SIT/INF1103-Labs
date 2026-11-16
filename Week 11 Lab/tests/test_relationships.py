# Regression tests for the Lab 8 relationships and the Lab 7 hierarchy (they must still hold).

import inspect
import json
import tempfile
import unittest
from pathlib import Path

import inventory_manager
from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier
from tests.helpers import capture_output, make_digital, make_physical, make_supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


class TestRelationships(unittest.TestCase):
    def test_association_supplier_outlives_the_variable(self) -> None:
        supplier = make_supplier()
        product = PhysicalProduct("P1", "Lamp", 10.0, 1, supplier, 1.0)
        del supplier
        self.assertEqual(product.supplier.name, "Acme Supplies")

    def test_aggregation_product_survives_removal_and_can_move(self) -> None:
        guitar = make_physical()
        inventory_a, inventory_b = Inventory(), Inventory()
        inventory_a.add_product(guitar)

        removed = inventory_a.remove_product("P001")

        self.assertIs(removed, guitar)
        self.assertIsNone(inventory_a.find_product("P001"))
        self.assertTrue(inventory_b.add_product(guitar))
        self.assertIs(inventory_b.find_product("P001"), guitar)

    def test_composition_each_order_creates_its_own_lines(self) -> None:
        guitar = make_physical()
        order_1, order_2 = Order("O-1"), Order("O-2")
        order_1.add_order_line(guitar, 1)
        order_2.add_order_line(guitar, 1)

        self.assertIsNot(order_1.order_lines[0], order_2.order_lines[0])
        self.assertIs(order_1.order_lines[0].product, order_2.order_lines[0].product)

    def test_order_lines_cannot_be_added_from_outside(self) -> None:
        order = Order("O-1")
        order.order_lines.append(None)  # type: ignore[arg-type]
        self.assertEqual(order.order_lines, [])


class TestHierarchy(unittest.TestCase):
    def test_product_is_still_abstract(self) -> None:
        with self.assertRaises(TypeError):
            Product("X1", "Generic", 1.0, 1, make_supplier())  # type: ignore[abstract]

    def test_only_physical_products_can_be_shipped(self) -> None:
        self.assertIsInstance(make_physical(), CanBeShipped)
        self.assertNotIsInstance(make_digital(), CanBeShipped)
        self.assertEqual(make_physical().calculate_shipping_cost(), 14.0)

    def test_polymorphism_without_isinstance(self) -> None:
        inventory = Inventory()
        inventory.add_product(make_physical())
        inventory.add_product(make_digital())

        messages = [product.get_fulfilment_info() for product in inventory.products]

        self.assertEqual(messages, [
            "Physical product: requires physical shipping.",
            "Digital product: delivered digitally via download.",
        ])
        self.assertNotIn("isinstance", inspect.getsource(Inventory))

    def test_show_product_details_works_for_every_subclass(self) -> None:
        for product in (make_physical(), make_digital()):
            _, output = capture_output(lambda: show_product_details(product))
            self.assertIn(product.name, output)
            self.assertIn(product.get_fulfilment_info(), output)


class TestJsonPersistence(unittest.TestCase):
    def test_types_and_suppliers_survive_a_save_and_reload(self) -> None:
        shared = make_supplier()
        other = Supplier("S02", "Digital Depot", "hi@depot.example")
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P001", "Guitar", 500.0, 3, shared, 4.5))
        inventory.add_product(DigitalProduct("D001", "Game", 20.0, 100, shared, 350.0))
        inventory.add_product(DigitalProduct("D002", "App", 5.0, 9, other, 80.0))

        original_path = inventory_manager.file_path
        with tempfile.TemporaryDirectory() as folder:
            inventory_manager.file_path = Path(folder) / "inventory.json"
            try:
                capture_output(lambda: inventory_manager.save_inventory(inventory))
                saved = json.loads(inventory_manager.file_path.read_text())
                loaded, _ = capture_output(inventory_manager.load_inventory)
            finally:
                inventory_manager.file_path = original_path

        self.assertEqual([item["type"] for item in saved], ["physical", "digital", "digital"])
        assert isinstance(loaded, Inventory)
        guitar, game = loaded.find_product("P001"), loaded.find_product("D001")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertIsInstance(game, DigitalProduct)
        assert guitar is not None and game is not None
        self.assertIs(guitar.supplier, game.supplier)  # a shared supplier is still shared

    def test_missing_or_broken_files_start_an_empty_inventory(self) -> None:
        original_path = inventory_manager.file_path
        try:
            with tempfile.TemporaryDirectory() as folder:
                inventory_manager.file_path = Path(folder) / "inventory.json"

                loaded, output = capture_output(inventory_manager.load_inventory)
                self.assertIn("not found", output)

                for broken in ("", "not json", "{}", "null", '[{"id": "P1"}]'):
                    inventory_manager.file_path.write_text(broken)
                    loaded, _ = capture_output(inventory_manager.load_inventory)
                    assert isinstance(loaded, Inventory)
                    self.assertEqual(loaded.products, [], broken)
        finally:
            inventory_manager.file_path = original_path

    def test_saving_to_an_unwritable_place_does_not_crash(self) -> None:
        original_path = inventory_manager.file_path
        try:
            with tempfile.TemporaryDirectory() as folder:
                inventory_manager.file_path = Path(folder) / "no_such_folder" / "inventory.json"
                _, output = capture_output(lambda: inventory_manager.save_inventory(Inventory()))
        finally:
            inventory_manager.file_path = original_path
        self.assertIn("Could not save", output)


if __name__ == "__main__":
    unittest.main()
