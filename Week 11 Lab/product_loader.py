import csv

from inventory import Inventory
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

# Columns: product_type, product_id, name, price, stock_quantity [, extra_value]
# extra_value is optional: the weight (kg) for physical products or the download
# size (MB) for digital products. If a row leaves it out, 0 is used.
REQUIRED_COLUMNS: int = 5


def create_product_from_row(row: list[str], supplier: Supplier) -> Product:
    # Turns one CSV row into a Product through the factory.
    # Raises ValueError (with a simple message) if anything in the row is invalid.
    if len(row) < REQUIRED_COLUMNS:
        raise ValueError(f"expected at least {REQUIRED_COLUMNS} columns but found {len(row)}")

    product_type, product_id, name = row[0], row[1], row[2]

    try:
        price = float(row[3])
    except ValueError:
        raise ValueError(f"price '{row[3]}' is not a number") from None

    try:
        stock_quantity = int(row[4])
    except ValueError:
        raise ValueError(f"stock quantity '{row[4]}' is not a whole number") from None

    extra_value = 0.0
    if len(row) > REQUIRED_COLUMNS and row[5].strip() != "":
        try:
            extra_value = float(row[5])
        except ValueError:
            raise ValueError(f"extra value '{row[5]}' is not a number") from None

    # The factory raises ValueError for an unknown type; the product classes raise it
    # for rule violations (price not above zero, negative stock, ...).
    return ProductFactory.create(
        product_type, product_id, name, price, stock_quantity, supplier, extra_value
    )


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    # Reads products from a CSV file and adds them to the inventory.
    # A missing file does not crash the program, and one bad row does not stop the
    # rest of the file from loading.
    loaded = 0

    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    except OSError:
        print(f"Products file could not be opened: {path}")
    else:
        with file:
            try:
                reader = csv.reader(file)
                next(reader, None)  # skip the header row

                for row in reader:
                    if not row:
                        continue  # ignore blank lines

                    try:
                        product = create_product_from_row(row, supplier)

                        if not inventory.add_product(product):
                            raise ValueError(f"duplicate product ID '{product.product_id}'")
                    except ValueError as error:
                        print(f"Skipping row {reader.line_num}: {error}")
                    else:
                        loaded += 1

            except (csv.Error, UnicodeDecodeError):
                print("The file could not be read properly. Stopped loading.")

        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
