import pytest
from streetrace import (
    RegistrationModule,
    CrewManagementModule,
    InventoryModule,
    RaceManagementModule,
    ResultsModule,
    MissionPlanningModule,
    ReputationModule,
    PoliceModule,
)

@pytest.fixture
def system():
    """Sets up the entire StreetRace Manager system modules."""
    reg = RegistrationModule()
    crew = CrewManagementModule(reg)
    inv = InventoryModule(crew)
    race = RaceManagementModule(crew)
    rep = ReputationModule()
    results = ResultsModule(race, inv, rep)
    police = PoliceModule()
    mission = MissionPlanningModule(police)
    
    return {
        "reg": reg, "crew": crew, "inv": inv,
        "race": race, "rep": rep, "results": results,
        "police": police, "mission": mission
    }

def test_registration_and_crew(system):
    """Tests that crew can only be assigned to registered users."""
    user = system["reg"].register_user("Dom", "u1")
    member = system["crew"].register_crew_member("u1", "Letty", "m1")
    system["crew"].assign_role("m1", "driver")
    
    assert member.role == "driver"
    assert member in user.crew

    with pytest.raises(ValueError):
        system["crew"].register_crew_member("invalid_user", "Brian", "m2")

def test_inventory_and_repair(system):
    """Tests parts degrading and being repaired by mechanics."""
    user = system["reg"].register_user("Mia", "u2")
    car = system["reg"].register_car("u2", "Skyline", "c1")
    
    part = system["inv"].add_part_to_car(car, "Nitrous", "p1")
    system["inv"].degrade_part("p1", 50)
    assert part.durability == 50
    
    # Cannot repair without a mechanic
    with pytest.raises(ValueError, match="mechanic"):
        system["inv"].repair_car(user, car)
        
    # Hire a mechanic and try again
    system["crew"].register_crew_member("u2", "Tej", "m3")
    system["crew"].assign_role("m3", "mechanic")
    
    system["inv"].repair_car(user, car)
    assert part.durability == 100

def test_race_integration(system):
    """Tests the interaction between Race, Results, Inventory, and Reputation."""
    u1 = system["reg"].register_user("Dom", "u1")
    c1 = system["reg"].register_car("u1", "Charger", "c1")
    system["inv"].add_part_to_car(c1, "Engine", "p1")
    
    u2 = system["reg"].register_user("Brian", "u2")
    c2 = system["reg"].register_car("u2", "Supra", "c2")
    system["inv"].add_part_to_car(c2, "Exhaust", "p2")
    
    # Needs a driver to enter race
    race1 = system["race"].create_race("r1", difficulty=10)
    
    with pytest.raises(ValueError, match="driver"):
        system["race"].enter_race("r1", u1, c1)
        
    system["crew"].register_crew_member("u1", "Dom", "m1")
    system["crew"].assign_role("m1", "driver")
    system["crew"].register_crew_member("u2", "Brian", "m2")
    system["crew"].assign_role("m2", "driver")
    
    # Enter race
    system["race"].enter_race("r1", u1, c1)
    system["race"].enter_race("r1", u2, c2)
    
    # Record Results (Dom wins)
    system["results"].record_result("r1", winner_user_id="u1")
    
    # Verify Effects
    assert system["rep"].get_rep("u1") == 100 # difficulty 10 * 10
    assert system["rep"].get_rep("u2") == 0
    
    # Verify part durability degradation
    # difficulty 10 * 2 = 20 degradation
    assert c1.parts[0].durability == 80
    assert c2.parts[0].durability == 80

def test_mission_and_police_integration(system):
    """Tests mission completion, heat tracking, and bust logic."""
    u1 = system["reg"].register_user("Dom", "u1")
    mission = system["mission"].plan_mission("m1", "Heist", heat_cost=60)
    
    # Requires spotter
    with pytest.raises(ValueError, match="spotter"):
        system["mission"].execute_mission("m1", u1)
        
    system["crew"].register_crew_member("u1", "Roman", "c1")
    system["crew"].assign_role("c1", "spotter")
    
    system["mission"].execute_mission("m1", u1)
    assert system["police"].heat_level == 60
    assert mission["completed"] is True
    
    # Plan another high heat mission
    system["mission"].plan_mission("m2", "Street Race", heat_cost=50)
    system["mission"].execute_mission("m2", u1)
    assert system["police"].is_busted() is True
    
    system["mission"].plan_mission("m3", "Truck Hijack", heat_cost=10)
    
    # Should be busted and unable to do missions
    with pytest.raises(ValueError, match="Busted"):
        system["mission"].execute_mission("m3", u1)
