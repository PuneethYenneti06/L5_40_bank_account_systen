"""Bank account management module."""

import hashlib
import os
import secrets

SERVICE_FEE = 2.50
account_data = {}
transactions = []

def create_account(acc_id, name, initial_deposit=0):
    """Create a new account. Return False if the ID already exists."""
    if acc_id in account_data:
        return False
    account_data[acc_id] = {"name": name, "balance": initial_deposit}
    transactions.append(
        f"Created {acc_id} with initial balance {initial_deposit}"
    )
    return True


def deposit(acc_id, amount):
    """Add a positive amount to an account. Return True on success."""
    if acc_id not in account_data or amount <= 0:
        return False
    account_data[acc_id]["balance"] += amount
    return True

def withdraw(acc_id, amount):
    """Withdraw an amount plus the service fee. Return True on success."""
    if acc_id not in account_data:
        return False
    total = amount + SERVICE_FEE
    if account_data[acc_id]["balance"] < total:
        return False
    account_data[acc_id]["balance"] -= total
    return True

def compute_bonus(acc_id, rate):
    """Return the bonus for an account at the given rate."""
    return account_data[acc_id]["balance"] * rate


def get_hash(pin, salt=None):
    """Return a salted PBKDF2 hash of the PIN as 'salt:hash'."""
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, 100_000)
    return salt.hex() + ":" + digest.hex()


def generate_temp_pin():
    """Return a random 4-digit PIN."""
    return secrets.randbelow(9000) + 1000


def backup_data(filename="backup.txt"):
    """Write the account data to a backup file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(account_data))
    print("Backup complete:", filename)

def main():
    """Run a demo of the bank account system."""
    admin_token = os.environ.get("ADMIN_TOKEN")
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", 0.05))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token configured:", admin_token is not None)

if __name__ == "__main__":
    main()
