class Part:
    def __init__(self, name, part_id, durability=100):
        self.name = name
        self.part_id = part_id
        self.durability = durability

class InventoryModule:
    """Manages inventory of car parts and repairs."""
    def __init__(self, crew_module):
        self.parts = {}
        self.crew_module = crew_module

    def add_part_to_car(self, car, name, part_id):
        if part_id in self.parts:
            raise ValueError("Part ID already exists.")
        part = Part(name, part_id)
        self.parts[part_id] = part
        car.parts.append(part)
        return part

    def degrade_part(self, part_id, amount):
        """Degrades a part's durability, e.g., after a race."""
        if part_id not in self.parts:
            raise ValueError("Part not found.")
        part = self.parts[part_id]
        part.durability = max(0, part.durability - amount)
        return part

    def repair_car(self, user, car):
        """Repairs all parts on a car back to 100 durability. Requires a mechanic."""
        has_mechanic = any(m.role == "mechanic" for m in user.crew)
        if not has_mechanic:
            raise ValueError("Cannot repair car: User does not have a mechanic assigned to their crew.")
        
        repaired = []
        for part in car.parts:
            if part.durability < 100:
                part.durability = 100
                repaired.append(part)
        return repaired
