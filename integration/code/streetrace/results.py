class ResultsModule:
    """Records race outcomes and applies side effects."""
    def __init__(self, race_module, inventory_module, reputation_module):
        self.race_module = race_module
        self.inventory = inventory_module
        self.reputation = reputation_module

    def record_result(self, race_id, winner_user_id):
        if race_id not in self.race_module.races:
            raise ValueError("Race not found.")
        
        race = self.race_module.races[race_id]
        if race.is_finished:
            raise ValueError("Race results already recorded.")

        winner = None
        for participant in race.participants:
            user = participant["user"]
            car = participant["car"]
            
            # Degrade parts for all participants
            degrade_amount = race.difficulty * 2
            for part in car.parts:
                self.inventory.degrade_part(part.part_id, degrade_amount)

            if user.user_id == winner_user_id:
                winner = user
        
        if winner is None:
            raise ValueError("Winner User ID was not a participant in the race.")

        # Reward winner with reputation points
        self.reputation.add_rep(winner.user_id, race.difficulty * 10)
        
        race.is_finished = True
        return winner
