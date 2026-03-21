class Race:
    def __init__(self, race_id, difficulty):
        self.race_id = race_id
        self.difficulty = difficulty
        self.participants = []  # List of dicts: {'user': user, 'car': car}
        self.is_finished = False

class RaceManagementModule:
    """Sets up races and handles entries."""
    def __init__(self, crew_module):
        self.races = {}
        self.crew_module = crew_module

    def create_race(self, race_id, difficulty):
        if race_id in self.races:
            raise ValueError("Race ID already exists.")
        race = Race(race_id, difficulty)
        self.races[race_id] = race
        return race

    def enter_race(self, race_id, user, car):
        if race_id not in self.races:
            raise ValueError("Race not found.")
        
        # Business Rule: User must have a driver assigned
        has_driver = any(m.role == "driver" for m in user.crew)
        if not has_driver:
            raise ValueError("User must have a crew member assigned as a driver to enter a race.")
        
        if car not in user.cars:
            raise ValueError("The provided car does not belong to the user.")

        race = self.races[race_id]
        if race.is_finished:
            raise ValueError("Cannot enter a finished race.")
            
        race.participants.append({"user": user, "car": car})
        return True
