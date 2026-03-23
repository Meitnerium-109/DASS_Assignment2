import pytest
from streetrace import RegistrationModule, CrewManagementModule, InventoryModule, RaceManagementModule, ResultsModule, MissionPlanningModule, ReputationModule, PoliceModule

@pytest.fixture
def system():
    reg = RegistrationModule()
    crew = CrewManagementModule(reg)
    inv = InventoryModule(crew)
    race = RaceManagementModule(crew)
    rep = ReputationModule()
    results = ResultsModule(race, inv, rep)
    police = PoliceModule()
    mission = MissionPlanningModule(police)
    return {"reg": reg, "crew": crew, "inv": inv, "race": race, "rep": rep, "results": results, "police": police, "mission": mission}

@pytest.mark.parametrize("i", range(1, 41))
def test_integration_reg_scale(system, i):
    uid = f"u{i}"; uname = f"User{i}"
    user = system["reg"].register_user(uname, uid)
    assert user.user_id == uid

@pytest.mark.parametrize("i", range(1, 41))
def test_integration_crew_scale(system, i):
    system["reg"].register_user("U", "u1")
    cname = f"Crew{i}"; cid = f"c{i}"; role = ["driver", "mechanic", "spotter"][i % 3]
    system["crew"].register_crew_member("u1", cname, cid)
    member = system["crew"].assign_role(cid, role)
    assert member.role == role

@pytest.mark.parametrize("i", range(1, 41))
def test_integration_inv_scale(system, i):
    u = system["reg"].register_user("U", "u1")
    c = system["reg"].register_car("u1", "Car", "car1")
    pid = f"p{i}"
    system["inv"].add_part_to_car(c, "Engine", pid)
    system["inv"].degrade_part(pid, (i*3)%100 + 1)
    system["crew"].register_crew_member("u1", "Mech", "m1")
    system["crew"].assign_role("m1", "mechanic")
    system["inv"].repair_car(u, c)
    assert c.parts[0].durability == 100

@pytest.mark.parametrize("i", range(1, 31))
def test_integration_mission_scale(system, i):
    u = system["reg"].register_user("U", "u1")
    system["crew"].register_crew_member("u1", "Spot", "m1")
    system["crew"].assign_role("m1", "spotter")
    mid = f"m{i}"; diff = 2
    system["mission"].plan_mission(mid, "Heist", diff)
    system["mission"].execute_mission(mid, u)
    assert system["police"].heat_level > 0

