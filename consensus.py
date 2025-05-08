import random
import hashlib
import time

class ProofOfStake:
    def __init__(self):
        self.stakers = {}  # {public_key: stake_amount}
        self.min_stake = 10  # Minimum tokens to stake

    def add_staker(self, public_key, amount):
        """Add or update a staker's token stake."""
        if amount < self.min_stake:
            raise ValueError(f"Stake must be at least {self.min_stake} tokens")
        if public_key in self.stakers:
            self.stakers[public_key] += amount
        else:
            self.stakers[public_key] = amount
        print(f"Staker {public_key[:8]}... staked {amount} tokens")

    def remove_staker(self, public_key, amount):
        """Remove or reduce a staker's stake."""
        if public_key not in self.stakers or self.stakers[public_key] < amount:
            raise ValueError("Insufficient stake")
        self.stakers[public_key] -= amount
        if self.stakers[public_key] == 0:
            del self.stakers[public_key]
        print(f"Staker {public_key[:8]}... unstaked {amount} tokens")

    def select_validator(self):
        """Select a validator based on stake weight."""
        if not self.stakers:
            raise ValueError("No stakers available")
        total_stake = sum(self.stakers.values())
        selection = random.uniform(0, total_stake)
        current = 0
        for public_key, stake in self.stakers.items():
            current += stake
            if current >= selection:
                return public_key
        return list(self.stakers.keys())[-1]  # Fallback

    def calculate_reward(self, validator):
        """Calculate staking reward for the validator."""
        stake = self.stakers.get(validator, 0)
        base_reward = 2  # Base reward per block
        reward = base_reward * (stake / 100)  # Reward scales with stake
        return reward
