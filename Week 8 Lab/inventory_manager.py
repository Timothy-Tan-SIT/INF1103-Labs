import json
from pathlib import Path

from product import Product
from inventory import Inventory

file_path = Path(__file__).parent / "inventory.json"


# ---------------------------------------------------------------
# File Handling
# ---------------------------------------------------------------

def load_inventory():
    # Loads inventory.json into an Inventory object of Product objects.
    # Returns an empty Inventory if the file is missing or unreadable.

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

        loaded = Inventory()
        for item in data:
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            loaded.add_product(product)

        print("Inventory loaded successfully.")
        return loaded

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("inventory.json is empty or incorrectly formatted. Starting with an empty inventory.")
        return inventory


def save_inventory(inventory):
    # Saves every Product in the Inventory to inventory.json.

    data = []
    for product in inventory.get_products():
        data.append({
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        })

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Inventory saved successfully to {file_path.name}.")


# ---------------------------------------------------------------
# Menu Handlers (get user input, then call Inventory methods)
# ---------------------------------------------------------------

def handle_add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip()

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    product_name = input("Product Name: ").strip()

    try:
        price = float(input("Price: "))
    except ValueError:
        print("Please enter a valid price.")
        return

    try:
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Please enter a valid stock quantity.")
        return

    try:
        product = Product(product_id, product_name, price, stock)
    except ValueError as error:
        # The Product class rejects invalid values (negative price, empty name, ...)
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

    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Please enter a valid stock quantity.")
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