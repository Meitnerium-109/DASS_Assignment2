class PoliceModule:
    """Custom Module 2: Tracks Police Heat Level globally."""
    def __init__(self):
        self.heat_level = 0
        self.max_heat = 100

    def increase_heat(self, amount):
        self.heat_level = min(self.max_heat, self.heat_level + amount)
        return self.heat_level

    def is_busted(self):
        return self.heat_level >= self.max_heat

    def lay_low(self):
        """Reduces the heat level completely."""
        self.heat_level = 0
