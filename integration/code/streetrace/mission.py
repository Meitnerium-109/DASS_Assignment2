class MissionPlanningModule:
    """Plans specific high-stakes missions."""
    def __init__(self, police_module):
        self.police = police_module
        self.missions = {}

    def plan_mission(self, mission_id, target, heat_cost):
        if mission_id in self.missions:
            raise ValueError("Mission ID already exists.")
        self.missions[mission_id] = {"target": target, "heat_cost": heat_cost, "completed": False}
        return self.missions[mission_id]

    def execute_mission(self, mission_id, user):
        if mission_id not in self.missions:
            raise ValueError("Mission not found.")
        
        mission = self.missions[mission_id]
        if mission["completed"]:
            raise ValueError("Mission already completed.")

        # Spotter Role required for Missions
        has_spotter = any(m.role == "spotter" for m in user.crew)
        if not has_spotter:
            raise ValueError("Missions require a spotter in your crew to watch out for cops.")

        if self.police.is_busted():
            raise ValueError("You cannot execute missions right now; Heat is too high! You are Busted!")

        # Execute
        self.police.increase_heat(mission["heat_cost"])
        mission["completed"] = True
        return True
