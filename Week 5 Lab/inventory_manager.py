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


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    # Starting products stored as a list of dictionaries
    inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
    ]

    display_all(inventory)


if __name__ == "__main__":
    main()