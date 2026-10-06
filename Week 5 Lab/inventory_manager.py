import json
import os
from pathlib import Path

# Folder where inventory.json lives.
# Locally this is the script's folder; in Docker, set DATA_DIR to the mounted volume.
data_dir = Path(os.environ.get("DATA_DIR", Path(__file__).parent))
file_path = data_dir / "inventory.json"


# ---------------------------------------------------------------
# Data Persistence Functions
# ---------------------------------------------------------------

def load_inventory():
    # Loads the product list from inventory.json.
    # Returns an empty list if the file is missing or unreadable.

    if not file_path.exists():
        print("inventory.json not found. Starting with an empty inventory.")
        return []

    print("inventory.json found.")

    try:
        with open(file_path, "r") as file:
            inventory = json.load(file)

        if not isinstance(inventory, list):
            raise ValueError("Inventory must be a list of products.")

        print("Inventory loaded successfully.")
        return inventory

    except (json.JSONDecodeError, ValueError):
        print("inventory.json is empty or incorrectly formatted. Starting with an empty inventory.")
        return []


def save_inventory(inventory):
    # Saves the product list to inventory.json.

    data_dir.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as file:
        json.dump(inventory, file, indent=4)

    print(f"Inventory saved successfully to {file_path.name}.")


# ---------------------------------------------------------------
# Data Manipulation Functions
# ---------------------------------------------------------------

def find_product(inventory, product_id):
    # Returns the product dictionary with the given ID, or None.
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip()

    if product_id == "":
        print("Product ID cannot be empty.")
        return

    # Check whether ID already exists
    if find_product(inventory, product_id) is not None:
        print("Product ID already exists.")
        return

    product_name = input("Product Name: ").strip()

    if product_name == "":
        print("Product name cannot be empty.")
        return

    # Validate price
    try:
        price = float(input("Price: "))

        if price < 0:
            print("Price cannot be negative.")
            return

    except ValueError:
        print("Please enter a valid price.")
        return

    # Validate stock
    try:
        stock = int(input("Stock Quantity: "))

        if stock < 0:
            print("Stock quantity cannot be negative.")
            return

    except ValueError:
        print("Please enter a valid stock quantity.")
        return

    new_product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory.append(new_product)
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    try:
        new_stock = int(input("New Stock Quantity: "))

        if new_stock < 0:
            print("Stock quantity cannot be negative.")
            return

    except ValueError:
        print("Please enter a valid stock quantity.")
        return

    product["stock"] = new_stock
    print("Stock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)

    if len(inventory) == 0:
        print("No products in inventory.")
    else:
        for product in inventory:
            print(
                f"ID: {product['id']} | Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
            )

    print("-" * 48)


# ---------------------------------------------------------------
# Menu System
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
                display_all(inventory)

            case "2":
                add_product(inventory)

            case "3":
                update_stock(inventory)

            case "4":
                search_product(inventory)

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