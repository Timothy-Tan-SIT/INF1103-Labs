import json
from pathlib import Path

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory

file_path = Path(__file__).parent / "inventory.json"


# ---------------------------------------------------------------
# File Handling
# ---------------------------------------------------------------

def create_product_from_dict(item):
    # Uses the saved "type" identifier to build the right Product subclass.
    # Raises ValueError / KeyError / TypeError if the entry is invalid.
    product_type = item["type"]

    match product_type:
        case "physical":
            return PhysicalProduct(
                item["id"], item["name"], item["price"], item["stock"], item["weight"]
            )

        case "digital":
            return DigitalProduct(
                item["id"], item["name"], item["price"], item["stock"], item["download_size"]
            )

        case _:
            raise ValueError(f"Unknown product type: {product_type}")


def load_inventory():
    # Loads inventory.json into an Inventory object of Product objects.
    # Returns an empty Inventory if the file is missing or unreadable.
    # Individual bad entries (e.g. old Lab 6 data with no "type") are skipped.

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

    skipped = 0
    for item in data:
        try:
            product = create_product_from_dict(item)
        except (KeyError, TypeError, ValueError):
            skipped += 1
            continue

        if not inventory.add_product(product):
            skipped += 1

    print("Inventory loaded successfully.")

    if skipped > 0:
        print(f"Warning: {skipped} invalid or duplicate product(s) in the file were skipped.")

    return inventory


def save_inventory(inventory):
    # Saves every Product in the Inventory to inventory.json.
    # Each product describes itself with to_dict(), including its type.

    data = []
    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Inventory saved successfully to {file_path.name}.")


# ---------------------------------------------------------------
# Menu Handlers (get user input, then call Inventory / Product methods)
# ---------------------------------------------------------------

def read_number(prompt, number_type, error_message):
    # Asks for a number and returns it, or None if the input is not valid.
    try:
        return number_type(input(prompt))
    except ValueError:
        print(error_message)
        return None


def handle_add_product(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Choose product type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip()

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    product_name = input("Product Name: ").strip()

    price = read_number("Price: ", float, "Please enter a valid price.")
    if price is None:
        return

    stock = read_number("Stock Quantity: ", int, "Please enter a valid stock quantity.")
    if stock is None:
        return

    try:
        if product_type == "1":
            weight = read_number("Weight (kg): ", float, "Please enter a valid weight.")
            if weight is None:
                return
            product = PhysicalProduct(product_id, product_name, price, stock, weight)

        else:
            size = read_number("Download Size (MB): ", float, "Please enter a valid download size.")
            if size is None:
                return
            product = DigitalProduct(product_id, product_name, price, stock, size)

    except ValueError as error:
        # The product classes reject invalid values (negative price, empty name, ...)
        print(error)
        return

    inventory.add_product(product)
    print("Product added successfully!")


def handle_update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    new_stock = read_number("New Stock Quantity: ", int, "Please enter a valid stock quantity.")
    if new_stock is None:
        return

    try:
        inventory.update_stock(product_id, new_stock)
    except ValueError as error:
        print(error)
        return

    print("Stock updated successfully!")


def handle_search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

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


# ---------------------------------------------------------------
# Menu System / Main Program
# ---------------------------------------------------------------

def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        show_menu()
        option = input("Enter option: ").strip()

        match option:
            case "1":
                inventory.display_all()

            case "2":
                handle_add_product(inventory)

            case "3":
                handle_update_stock(inventory)

            case "4":
                handle_search_product(inventory)

            case "5":
                print("Saving inventory...")
                save_inventory(inventory)

            case "6":
                print("Saving inventory before exit...")
                save_inventory(inventory)
                print("Thank you for using Inventory Management System.")
                print("Program terminated.")
                break

            case _:
                print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
