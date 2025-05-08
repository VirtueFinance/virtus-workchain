import hashlib
import json
import time
import random

# Block Class: Represents a single block in the Virtus WorkChain blockchain
class Block:
    def __init__(self, index, transactions, task_certificates, previous_hash):
        """
        Initialize a new block.
        
        Args:
            index (int): Block height in the chain
            transactions (list): List of transactions in the block
            task_certificates (list): List of task completion certificates
            previous_hash (str): Hash of the previous block
        """
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.task_certificates = task_certificates
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculate the SHA-256 hash of the block.
        
        Returns:
            str: Hexadecimal hash of the block
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "task_certificates": self.task_certificates,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

# VirtusWorkChain Class: Manages the blockchain and its operations
class VirtusWorkChain:
    def __init__(self):
        """
        Initialize the Virtus WorkChain blockchain with a genesis block.
        """
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Number of leading zeros required in hash for PoW
        self.pending_transactions = []
        self.pending_task_certificates = []
        self.min_task_certificates_per_block = 5  # Minimum certificates required to mine
        self.mining_reward = 5  # Reward for mining a block

    def create_genesis_block(self):
        """
        Create the first block (genesis block) of the blockchain.
        
        Returns:
            Block: Genesis block
        """
        return Block(0, [], [], "0")

    def get_latest_block(self):
        """
        Get the most recent block in the chain.
        
        Returns:
            Block: Latest block
        """
        return self.chain[-1]

    def mine_block(self, miner_address):
        """
        Mine a new block using Proof-of-Work.
        
        Args:
            miner_address (str): Address of the miner to receive the reward
        
        Raises:
            ValueError: If there are insufficient task certificates
        """
        # Add miner reward transaction
        reward_tx = {"from": "network", "to": miner_address, "amount": self.mining_reward}
        self.pending_transactions.append(reward_tx)

        # Check for sufficient task certificates
        if len(self.pending_task_certificates) < self.min_task_certificates_per_block:
            raise ValueError(f"Need at least {self.min_task_certificates_per_block} task certificates to mine")
        
        # Take the required number of task certificates
        task_certificates = self.pending_task_certificates[:self.min_task_certificates_per_block]
        self.pending_task_certificates = self.pending_task_certificates[self.min_task_certificates_per_block:]

        # Create a new block
        block = Block(len(self.chain), self.pending_transactions, task_certificates, self.get_latest_block().hash)

        # Proof-of-Work: Find a nonce that satisfies the difficulty
        print(f"Mining block #{block.index}...")
        start_time = time.time()
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        
        end_time = time.time()
        print(f"Block mined! Hash: {block.hash} (Time: {end_time - start_time:.2f}s)")
        
        # Add block to chain and clear pending transactions
        self.chain.append(block)
        self.pending_transactions = []

    def add_transaction(self, sender, recipient, amount):
        """
        Add a transaction to the pending list.
        
        Args:
            sender (str): Sender's address
            recipient (str): Recipient's address
            amount (int): Amount to transfer
        """
        transaction = {"from": sender, "to": recipient, "amount": amount}
        self.pending_transactions.append(transaction)
        print(f"Transaction added: {sender} -> {recipient} ({amount} tokens)")

    def add_task_certificate(self, certificate):
        """
        Add a task certificate to the pending list.
        
        Args:
            certificate (dict): Task certificate data
        """
        self.pending_task_certificates.append(certificate)
        print(f"Task certificate added: Task ID {certificate['task_id']}")

    def is_chain_valid(self):
        """
        Validate the integrity of the blockchain.
        
        Returns:
            bool: True if valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False

            # Check if the chain is continuous
            if current_block.previous_hash != previous_block.hash:
                print(f"Chain broken at block {i}")
                return False

            # Check minimum task certificates
            if len(current_block.task_certificates) < self.min_task_certificates_per_block:
                print(f"Insufficient task certificates at block {i}")
                return False

        return True

    def get_balance(self, address):
        """
        Calculate the balance of an address.
        
        Args:
            address (str): Address to check
        
        Returns:
            int: Total balance
        """
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx["from"] == address:
                    balance -= tx["amount"]
                if tx["to"] == address:
                    balance += tx["amount"]
        return balance

# Task Functions: Handle task completion and certificate generation
def generate_task_certificate(task_id, user_address, task_data):
    """
    Generate a task completion certificate after validation.
    
    Args:
        task_id (str): Unique task identifier
        user_address (str): User's address
        task_data (str): Data submitted for the task
    
    Returns:
        dict: Task certificate if valid, None otherwise
    """
    if validate_task(task_data):
        certificate = {
            "task_id": task_id,
            "user_address": user_address,
            "timestamp": time.time(),
            "signature": hashlib.sha256(f"{task_id}{user_address}{time.time()}".encode()).hexdigest()
        }
        return certificate
    return None

def validate_task(task_data):
    """
    Validate task data (placeholder for real validation logic).
    
    Args:
        task_data (str): Submitted task data
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Simulate task validation (e.g., checking accuracy or completeness)
    return random.choice([True, True, False])  # 66% chance of success for demo

# Main Execution: Demonstrate the blockchain in action
if __name__ == "__main__":
    # Initialize the blockchain
    blockchain = VirtusWorkChain()
    print("Virtus WorkChain initialized with genesis block.")

    # Simulate users completing tasks and generating certificates
    users = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
    for i in range(10):
        user = random.choice(users)
        task_id = f"task_{i}"
        certificate = generate_task_certificate(task_id, user, f"Data for {task_id}")
        if certificate:
            blockchain.add_task_certificate(certificate)

    # Add some transactions
    blockchain.add_transaction("Alice", "Bob", 50)
    blockchain.add_transaction("Bob", "Charlie", 30)

    # Mine the first block
    blockchain.mine_block("miner1")

    # Add more tasks and transactions
    for i in range(10, 15):
        user = random.choice(users)
        task_id = f"task_{i}"
        certificate = generate_task_certificate(task_id, user, f"Data for {task_id}")
        if certificate:
            blockchain.add_task_certificate(certificate)

    blockchain.add_transaction("Charlie", "Dave", 20)
    blockchain.add_transaction("Dave", "Eve", 10)

    # Mine another block
    blockchain.mine_block("miner2")

    # Validate the blockchain
    print("\nValidating blockchain...")
    is_valid = blockchain.is_chain_valid()
    print(f"Is blockchain valid? {is_valid}")

    # Check balances
    print("\nUser balances:")
    for user in users:
        balance = blockchain.get_balance(user)
        print(f"{user}: {balance} tokens")

    # Display the blockchain
    print("\nBlockchain state:")
    for block in blockchain.chain:
        print(f"Block #{block.index}:")
        print(f"  Hash: {block.hash}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Transactions: {block.transactions}")
        print(f"  Task Certificates: {len(block.task_certificates)} certificates")
