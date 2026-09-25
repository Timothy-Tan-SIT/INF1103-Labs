import json
from pathlib import Path
file_path = Path(__file__).parent / "inventory.txt"


def get_valid_input():
    # Handles input and validation.
    # Returns a valid integer or 'quit'.

    userInput = input('Enter a positive integer below 500 or type "quit" to exit the program: ')

    # Check if user wants to quit
    match userInput.lower():
        case "quit":
            return "quit"

    # Check whether input is an integer
    try:
        number = int(userInput)

        # Check whether number is positive
        match number:
            case n if n <= 0:
                print("Please key in a positive number.")
                return None

            case _:
                return number

    except ValueError:
        print("Please input a valid response.")
        return None


def process_delivery(current_total, newValue):
    # Calculates and returns the new inventory total.
    return current_total + newValue


def calculate_tax(amount):
    # Calculates 10% tax on a specific delivery.
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    # Prints the final summary.
    print(
        f"Closing program.\n"
        f"Total units processed: {total_units}\n"
        f"Failed Entries: {failed_attempts}"
    )


def load_inventory():
    # Loads inventory total and transaction history from inventory.txt.

    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        total_units = data["total"]
        transaction_history = data["history"]

        return total_units, transaction_history

    except FileNotFoundError:
        # If the file does not exist, start with empty inventory.
        return 0, []

    except (json.JSONDecodeError, KeyError):
        # If the file is empty or incorrectly formatted,
        # start with empty inventory.
        return 0, []


def save_inventory(total_units, transaction_history):
    # Saves inventory total and transaction history to inventory.txt.

    data = {
        "total": total_units,
        "history": transaction_history
    }

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# Main program

inventory, transaction_history = load_inventory()
entryFailed = 0

print(f"Current inventory loaded: {inventory}")
print(f"Previous transactions: {transaction_history}")

while True:

    newValue = get_valid_input()

    # Determine what happened with the input
    match newValue:

        # User chose to quit
        case "quit":
            save_inventory(inventory, transaction_history)
            generate_report(inventory, entryFailed)
            break

        # Invalid input
        case None:
            entryFailed += 1

        # Valid integer input
        case number:

            # Check whether inventory would exceed 500
            newTotal = process_delivery(inventory, number)

            match newTotal:
                case total if total > 500:
                    print(
                        "Adding this amount would exceed the 500-unit limit."
                        "\nTerminating session now."
                    )
                    break

                case _:
                    inventory = newTotal

                    # Add valid transaction to history
                    transaction_history.append(number)

                    tax = calculate_tax(number)

                    print(f"Inventory count is currently: {inventory}")
                    print(f"Tax for this delivery: ${tax:.2f}")