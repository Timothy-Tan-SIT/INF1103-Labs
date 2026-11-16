import tempfile
import unittest
from pathlib import Path

from inventory import Inventory
from product_loader import load_products
from tests.helpers import capture_output, make_supplier

LAB_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "products.csv"

    def write_csv(self, text: str) -> str:
        self.path.write_text(text)
        return str(self.path)

    def load(self, path: str) -> tuple[Inventory, list[str]]:
        inventory = Inventory()
        _, output = capture_output(lambda: load_products(path, inventory, make_supplier()))
        return inventory, output.splitlines()

    def test_lab_file_loads_three_products_and_skips_two_bad_rows(self) -> None:
        inventory, lines = self.load(self.write_csv(LAB_CSV))
        ids = [product.product_id for product in inventory.products]
        self.assertEqual(ids, ["P001", "D001", "P003"])  # valid rows after the bad ones still load

    def test_lab_file_messages_and_their_order(self) -> None:
        _, lines = self.load(self.write_csv(LAB_CSV))
        self.assertEqual(lines, [
            "Skipping row 4: Unknown product type: service",
            "Skipping row 5: price 'abc' is not a number",
            "3 products loaded.",
            "Load attempt finished.",
        ])

    def test_missing_file_is_handled_without_crashing(self) -> None:
        missing = str(Path(self.folder.name) / "not_here.csv")
        inventory, lines = self.load(missing)
        self.assertEqual(inventory.products, [])
        self.assertEqual(lines, [
            f"Products file not found: {missing}",
            "Load attempt finished.",  # finally runs; the else block did not
        ])

    def test_a_folder_instead_of_a_file_is_handled(self) -> None:
        inventory, lines = self.load(self.folder.name)
        self.assertEqual(inventory.products, [])
        self.assertEqual(lines[-1], "Load attempt finished.")

    def test_finally_runs_when_the_file_loads_too(self) -> None:
        _, lines = self.load(self.write_csv(LAB_CSV))
        self.assertEqual(lines[-1], "Load attempt finished.")

    def test_row_with_too_few_columns_is_skipped(self) -> None:
        inventory, lines = self.load(self.write_csv(
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Lamp\n"
            "physical,P002,Chair,10,2\n"))
        self.assertEqual([p.product_id for p in inventory.products], ["P002"])
        self.assertIn("Skipping row 2: expected at least 5 columns but found 3", lines)

    def test_invalid_rule_values_are_skipped(self) -> None:
        inventory, lines = self.load(self.write_csv(
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Free Lamp,0,5\n"
            "physical,P002,Lamp,10,-3\n"
            "physical,P003,Lamp,10,2.5\n"
            "physical,P004,Lamp,10,2\n"))
        self.assertEqual([p.product_id for p in inventory.products], ["P004"])
        self.assertIn("Skipping row 2: Price must be greater than zero.", lines)
        self.assertIn("Skipping row 3: Stock quantity cannot be negative.", lines)
        self.assertIn("Skipping row 4: stock quantity '2.5' is not a whole number", lines)

    def test_duplicate_ids_are_reported_and_skipped(self) -> None:
        inventory, lines = self.load(self.write_csv(
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Lamp,10,2\n"
            "digital,p001,Game,10,2\n"))
        self.assertEqual(len(inventory.products), 1)
        self.assertIn("Skipping row 3: duplicate product ID 'p001'", lines)
        self.assertIn("1 products loaded.", lines)

    def test_blank_lines_are_ignored_and_optional_extra_value_is_used(self) -> None:
        inventory, lines = self.load(self.write_csv(
            "product_type,product_id,name,price,stock_quantity,extra_value\n"
            "\n"
            "physical,P001,Lamp,10,2,3.5\n"))
        self.assertEqual(len(inventory.products), 1)
        self.assertEqual(inventory.products[0].weight, 3.5)  # type: ignore[attr-defined]
        self.assertEqual([line for line in lines if line.startswith("Skipping")], [])

    def test_empty_file_loads_nothing_and_does_not_crash(self) -> None:
        inventory, lines = self.load(self.write_csv(""))
        self.assertEqual(inventory.products, [])
        self.assertEqual(lines, ["0 products loaded.", "Load attempt finished."])

    def test_file_that_is_not_text_is_handled(self) -> None:
        self.path.write_bytes(b"\xff\xfe\x00\x80 not valid utf-8 \xff")
        inventory, lines = self.load(str(self.path))
        self.assertEqual(inventory.products, [])
        self.assertEqual(lines[-1], "Load attempt finished.")


if __name__ == "__main__":
    unittest.main()
