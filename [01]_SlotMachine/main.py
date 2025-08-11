# The 'random' module is imported to allow for random selection of symbols.
import random

# Global constants are defined here. These are values that don't change throughout the program.
# Using all caps is a common convention for constants in Python.
MAX_LINES = 3  # The maximum number of lines a player can bet on.
MAX_BET = 100  # The maximum amount a player can bet per line.
MIN_BET = 1  # The minimum amount a player can bet per line.

ROWS = 3  # The number of rows on the slot machine grid.
COLS = 3  # The number of columns on the slot machine grid.

# A dictionary to store the count of each symbol.
# More 'D' symbols means they appear more frequently on the slot machine.
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

# A dictionary to store the value (payout multiplier) for each symbol.
# 'A' has the highest value, so it pays the most.
symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

# ---
# The functions that make the game work are defined below.
# ---


def deposit():
    """
    Asks the player for a deposit and validates the input.

    Returns:
        int: The validated deposit amount.
    """
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():  # Check if the input consists only of digits.
            amount = int(amount)
            if amount > 0:
                break  # Exit the loop if the amount is a valid positive number.
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount


def get_number_of_lines():
    """
    Asks the player for the number of lines to bet on and validates the input.

    Returns:
        int: The validated number of lines.
    """
    while True:
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            # Check if the number of lines is within the valid range.
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines


def get_bet():
    """
    Asks the player for their bet amount per line and validates the input.

    Returns:
        int: The validated bet amount.
    """
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            # Check if the bet amount is within the valid range.
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")
    return amount


def get_slot_machine_spin(rows, cols, symbols):
    """
    Generates a random spin for the slot machine.

    Args:
        rows (int): The number of rows on the slot machine.
        cols (int): The number of columns on the slot machine.
        symbols (dict): A dictionary of symbols and their counts.

    Returns:
        list: A list of lists representing the spun slot machine grid.
    """
    all_symbols = []
    # Create a list with all possible symbols based on their counts.
    # For example, if 'A' has a count of 2, it will be added to the list twice.
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    # Loop through each column to generate its symbols.
    for _ in range(cols):
        column = []
        # Create a copy of 'all_symbols' for each column to ensure symbols are chosen uniquely per column.
        current_symbols = all_symbols[:]
        # Loop through each row to pick a symbol for the current column.
        for _ in range(rows):
            # Randomly pick a symbol from the available symbols.
            value = random.choice(current_symbols)
            # Remove the chosen symbol to prevent it from being picked again in the same column.
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)  # Add the generated column to the list of columns.

    return columns


def check_winnings(columns, lines, bet, values):
    """
    Calculates the total winnings and identifies which lines won.

    Args:
        columns (list): A list of lists representing the slot machine grid.
        lines (int): The number of lines the player bet on.
        bet (int): The amount bet on each line.
        values (dict): A dictionary of symbol values.

    Returns:
        tuple: A tuple containing the total winnings and a list of winning lines.
    """
    winnings = 0
    winning_lines = []
    # Loop through each line the player bet on.
    for line in range(lines):
        # Get the symbol from the first column of the current line.
        symbol = columns[0][line]
        # Assume it's a winning line until proven otherwise.
        # This loop checks if all symbols in the current row are the same.
        for column in columns:
            symbol_to_check = column[line]
            # If any symbol doesn't match the first one, it's not a winning line.
            if symbol != symbol_to_check:
                break  # Exit the inner loop and move to the next line.
        else:
            # The 'else' block of a 'for' loop runs if the loop completes without a 'break'.
            # This means all symbols in the line matched.
            winnings += values[symbol] * bet  # Add the payout to the total winnings.
            winning_lines.append(line + 1)  # Record the winning line number.

    return winnings, winning_lines


def print_slot_machine(columns):
    """
    Prints the slot machine grid in a user-friendly format.

    Args:
        columns (list): A list of lists representing the slot machine grid.
    """
    # Loop through each row to print it. 'columns[0]' is used to get the number of rows.
    for row in range(len(columns[0])):
        # Loop through each column to print the symbol in the current row.
        # 'enumerate' provides both the index (i) and the item (column).
        for i, column in enumerate(columns):
            # Print a separator (' | ') between symbols, but not after the last one.
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()  # Print a newline to start the next row on a new line.


def spin(balance):
    """
    Runs a single round of the slot machine game.

    Args:
        balance (int): The player's current balance.

    Returns:
        int: The net change in the player's balance (winnings - total bet).
    """
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        # Check if the player has enough money to make the bet.
        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines}. Total bet is equal to: ${total_bet}.")

    # Generate the slot machine spin.
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    # Print the result of the spin.
    print_slot_machine(slots)
    # Check for any winnings.
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    # Print the winning lines. The '*' unpacks the list so it prints as separate items.
    print(f"You won on lines: ", *winning_lines)
    # Return the net change in balance.
    return winnings - total_bet


def main():
    """
    The main function that runs the entire game loop.
    """
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        spins = input("Press enter to play (q to quit) -> ")
        if spins == "q":
            break  # Exit the game loop if the player enters 'q'.
        balance += spin(balance)  # Play a round and update the balance.

    print(f"You left with ${balance}")


# The following line ensures that the 'main' function is called when the script is run.
if __name__ == "__main__":
    main()