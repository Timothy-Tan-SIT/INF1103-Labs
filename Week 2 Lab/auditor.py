inventory = 0
entryFailed = 0
while True:

    userInput = input(
        'Enter a positive integer below 500 or type "quit" to exit the program: '
    )

    if userInput.lower() == "quit":
        print(
            f"Closing program.\nTotal units processed: {inventory}\nFailed Entries: {entryFailed}"
        )
        break

#Check whether input is an integer
    try:
        number = int(userInput)

#Check whether input is negative or 0
        if number <= 0:
            print("Please key in a positive number.")
            entryFailed += 1

#Case where inventory exceeds 500; Terminates session
        elif inventory + number > 500:
            print(
                "Adding this amount would exceed the 500-unit limit.\nTerminating session now."
            )
            break

#Accepted integer input
        else:
            inventory += number
            print(f"Inventory count is currently: {inventory}")

#Non integer inputs filtered here
    except ValueError:
        print("Please input a valid response.")
        entryFailed += 1