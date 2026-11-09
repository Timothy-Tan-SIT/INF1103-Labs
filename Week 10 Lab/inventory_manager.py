import json
from pathlib import Path
from typing import Any

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order

# inventory.json sits next to this script (also works with the Docker volume mount)
file_path: Path = Path(__file__).parent / "inventory.json"


# ---------------------------------------------------------------
# File Handling
# ---------------------------------------------------------------

def get_or_create_supplier(data: dict[str, Any], suppliers: dict[str, Supplier]) -> Supplier:
    # Products that share a supplier ID share ONE Supplier object after loading.
    # Raises KeyError / ValueError if the supplier data is incomplete or invalid.
    supplier_id = data["id"]
    key = supplier_id.strip().lower()

    if key not in suppliers:
        suppliers[key] = Supplier(supplier_id, data["name"], data["contact_email"])

    return suppliers[key]


def create_product_from_dict(item: dict[str, Any], suppliers: dict[str, Supplier]) -> Product:
    # Uses the saved "type" identifier to build the right Product subclass.
    # Raises ValueError / KeyError / TypeError if the entry is invalid.
    # (Any is used only because JSON content is not known until runtime; the
    # constructors validate every value.)
    supplier = get_or_create_supplier(item["supplier"], suppliers)
    product_type = item["type"]

    match product_type:
        case "physical":
            return PhysicalProduct(
                item["id"], item["name"], item["price"], item["stock"],
                supplier, item["weight"]
            )

        case "digital":
            return DigitalProduct(
                item["id"], item["name"], item["price"], item["stock"],
                supplier, item["download_size"]
            )

        case _:
            raise ValueError(f"Unknown product type: {product_type}")


def load_inventory() -> Inventory:
    # Loads inventory.json into an Inventory object of Product objects.
    # Returns an empty Inventory if the file is missing or unreadable.
    # Individual bad entries (e.g. old Lab 7 data with no "supplier") are skipped.

    inventory = Inventory()

    if not file_path.exists():
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory

    print("inventory.json found.")

    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Inventory must be a list of products.")

    except (json.JSONDecodeError, ValueError):
        print("inventory.json is empty or incorrectly formatted. Starting with an empty inventory.")
        return inventory

    suppliers: dict[str, Supplier] = {}
    skipped = 0

    for item in data:
        try:
            product = create_product_from_dict(item, suppliers)
        except (KeyError, TypeError, ValueError):
            skipped += 1
            continue

        if not inventory.add_product(product):
            skipped += 1

    print("Inventory loaded successfully.")

    if skipped > 0:
        print(f"Warning: {skipped} invalid or duplicate product(s) in the file were skipped.")

    return inventory


def save_inventory(inventory: Inventory) -> None:
    # Saves every Product in the Inventory to inventory.json.
    # Each product describes itself with to_dict(), including its type and supplier.

    data: list[dict[str, object]] = []
    for product in inventory.products:
        data.append(product.to_dict())

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Inventory saved successfully to {file_path.name}.")


# ---------------------------------------------------------------
# Menu Handlers (get user input, then call Inventory / Product / Order methods)
# ---------------------------------------------------------------

def read_float(prompt: str, error_message: str) -> float | None:
    # Asks for a decimal number and returns it, or None if the input is not valid.
    try:
        return float(input(prompt))
    except ValueError:
        print(error_message)
        return None


def read_int(prompt: str, error_message: str) -> int | None:
    # Asks for a whole number and returns it, or None if the input is not valid.
    try:
        return int(input(prompt))
    except ValueError:
        print(error_message)
        return None


def find_known_suppliers(inventory: Inventory) -> dict[str, Supplier]:
    # Collects the suppliers already used by products in the inventory.
    suppliers: dict[str, Supplier] = {}
    for product in inventory.products:
        suppliers[product.supplier.supplier_id.lower()] = product.supplier
    return suppliers


def ask_for_supplier(inventory: Inventory) -> Supplier | None:
    # Reuses a known supplier (same ID) or creates a new independent Supplier object.
    # Returns None if the user enters invalid details.
    known = find_known_suppliers(inventory)

    supplier_id = input("Supplier ID: ").strip()

    if supplier_id.lower() in known:
        supplier = known[supplier_id.lower()]
        print(f"Existing supplier found: {supplier.name}")
        return supplier

    supplier_name = input("Supplier Name: ").strip()
    contact_email = input("Supplier Contact Email: ").strip()

    try:
        return Supplier(supplier_id, supplier_name, contact_email)
    except ValueError as error:
        print(error)
        return None


def handle_add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Choose product type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip()

    if inventory.find_product(product_id) is not None:
        print("Product ID already exists.")
        return

    product_name = input("Product Name: ").strip()

    price = read_float("Price: ", "Please enter a valid price.")
    if price is None:
        return

    stock = read_int("Stock Quantity: ", "Please enter a valid stock quantity.")
    if stock is None:
        return

    supplier = ask_for_supplier(inventory)
    if supplier is None:
        return

    try:
        product: Product
        if product_type == "1":
            weight = read_float("Weight (kg): ", "Please enter a valid weight.")
            if weight is None:
                return
            product = PhysicalProduct(product_id, product_name, price, stock, supplier, weight)

        else:
            size = read_float("Download Size (MB): ", "Please enter a valid download size.")
            if size is None:
                return
            product = DigitalProduct(product_id, product_name, price, stock, supplier, size)

    except ValueError as error:
        # The product classes reject invalid values (negative price, empty name, ...)
        print(error)
        return

    inventory.add_product(product)
    print("Product added successfully!")


def handle_update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    new_stock = read_int("New Stock Quantity: ", "Please enter a valid stock quantity.")
    if new_stock is None:
        return

    try:
        inventory.update_stock(product_id, new_stock)
    except ValueError as error:
        print(error)
        return

    print("Stock updated successfully!")


def handle_search_product(inventory: Inventory) -> None:
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    product.display_details()
    print(f"Fulfilment: {product.get_fulfilment_info()}")

    # Only products that signed the CanBeShipped contract can calculate shipping.
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")

    print("-" * 48)


def handle_remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")

    product_id = input("Enter Product ID: ").strip()
    removed = inventory.remove_product(product_id)

    if removed is None:
        print("Product not found.")
        return

    # Aggregation: the Product object still exists, it is just no longer in this inventory.
    print(f"Removed {removed.name} ({removed.product_id}) from the inventory.")


def handle_create_order(inventory: Inventory, orders: list[Order]) -> None:
    print("\nCreate Order")

    order_id = input("Order ID: ").strip()

    try:
        order = Order(order_id)
    except ValueError as error:
        print(error)
        return

    # The Order creates its own OrderLine objects through add_order_line().
    while True:
        product_id = input("Product ID (leave blank to finish): ").strip()

        if product_id == "":
            break

        product = inventory.find_product(product_id)

        if product is None:
            print("Product not found.")
            continue

        quantity = read_int("Quantity: ", "Please enter a valid quantity.")
        if quantity is None:
            continue

        try:
            order.add_order_line(product, quantity)
        except ValueError as error:
            print(error)

    if len(order.order_lines) == 0:
        print("No items added. Order cancelled.")
        return

    orders.append(order)
    order.display_information()
    print("Order created successfully!")


# ---------------------------------------------------------------
# Menu System / Main Program
# ---------------------------------------------------------------

def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Save Inventory")
    print("8. Exit")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()
    orders: list[Order] = []  # orders only exist while the program is running

    while True:
        show_menu()
        option = input("Enter option: ").strip()

        match option:
            case "1":
                inventory.display_all_products()

            case "2":
                handle_add_product(inventory)

            case "3":
                handle_update_stock(inventory)

            case "4":
                handle_search_product(inventory)

            case "5":
                handle_remove_product(inventory)

            case "6":
                handle_create_order(inventory, orders)

            case "7":
                print("Saving inventory...")
                save_inventory(inventory)

            case "8":
                print("Saving inventory before exit...")
                save_inventory(inventory)
                print("Thank you for using Inventory Management System.")
                print("Program terminated.")
                break

            case _:
                print("Invalid option. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()