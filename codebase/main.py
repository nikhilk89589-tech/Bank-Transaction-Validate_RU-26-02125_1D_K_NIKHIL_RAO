"""
PS 24 - Bank Transaction Validator
Reads transactions from a file, validates each one against banking rules,
prints Valid/Invalid with a reason, and shows a final summary.

Usage:  python bank_validator.py [input_file]
        (default input file: transactions.txt)
"""

import sys

OPENING_BALANCE = 10000
MAX_AMOUNT = 100000
INPUT_FILE = "transactions.txt"
OUTPUT_FILE = "valid_transactions.txt"


def fmt(number):
    """Show whole numbers without a decimal part (15000 instead of 15000.0)."""
    return str(int(number)) if number == int(number) else str(number)


def validate_transaction(tx_type, amount_text, balance):
    """
    Check one transaction.
    Returns (is_valid, reason, amount).
    Checks in order: type -> numeric -> positive -> limit -> balance.
    """
    if tx_type.lower() not in ("deposit", "withdraw"):
        return False, f"unknown type '{tx_type}'", None

    try:
        amount = float(amount_text)
    except ValueError:
        return False, f"amount '{amount_text}' is not a number", None

    if amount <= 0:
        return False, "amount must be positive", None

    if amount > MAX_AMOUNT:
        return False, f"exceeds limit of {MAX_AMOUNT}", None

    if tx_type.lower() == "withdraw" and amount > balance:
        return False, "insufficient balance", None

    return True, "", amount


def read_transactions(filename):
    """Read all lines from the file. Returns None if the file is missing."""
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
    except OSError as e:
        print(f"Error reading '{filename}': {e}")
    return None


def save_valid(valid_lines, filename):
    """Save valid transactions to a file."""
    try:
        with open(filename, "w") as f:
            for line in valid_lines:
                f.write(line + "\n")
    except OSError as e:
        print(f"Error saving '{filename}': {e}")


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE
    lines = read_transactions(filename)
    if lines is None:
        return

    balance = OPENING_BALANCE
    valid_count = 0
    invalid_count = 0
    valid_lines = []

    for number, line in enumerate(lines, start=1):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 2:
            print(f"Line {number}: Invalid – wrong format, expected Type,Amount.")
            invalid_count += 1
            continue

        tx_type, amount_text = parts
        is_valid, reason, amount = validate_transaction(tx_type, amount_text, balance)

        if is_valid:
            if tx_type.lower() == "deposit":
                balance += amount
            else:
                balance -= amount
            valid_count += 1
            valid_lines.append(f"{tx_type.capitalize()},{fmt(amount)}")
            print(f"Line {number}: Valid | Balance: {fmt(balance)}")
        else:
            invalid_count += 1
            print(f"Line {number}: Invalid – {reason}.")

    print(f"Valid: {valid_count} | Invalid: {invalid_count} | Final balance: {fmt(balance)}")
    save_valid(valid_lines, OUTPUT_FILE)


if __name__ == "__main__":
    main()
