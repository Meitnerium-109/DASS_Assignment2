class ReputationModule:
    """Custom Module 1: Tracks Street Cred points."""
    def __init__(self):
        self.reputation = {}

    def get_rep(self, user_id):
        return self.reputation.get(user_id, 0)

    def add_rep(self, user_id, amount):
        current = self.get_rep(user_id)
        self.reputation[user_id] = current + amount
        return self.reputation[user_id]
