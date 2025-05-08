class Wallet:
    def __init__(self, address):
        self.address = address
        self.balance = 0

    def update_balance(self, amount):
        """Update the wallet balance."""
        self.balance += amount
        print(f"New balance for {self.address}: {self.balance}")
