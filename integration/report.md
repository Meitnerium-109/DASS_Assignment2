# Integration Testing Report: StreetRace Manager

## Module Implementations
We implemented the StreetRace Manager backend according to the specifications, broken down into the following cohesive modules:
- `registration.py`: Manages `User` and `Car` creation.
- `crew.py`: Manages `CrewMember` hiring and assigning roles.
- `inventory.py`: Adds `Part` to cars and manages part repairing.
- `race.py`: Tracks `Race` instances and validates participants.
- `results.py`: Records race outcomes and propagates part degradation.
- `mission.py`: Plans and executes high-stakes missions.
- **Custom Module 1 (`reputation.py`)**: Manages the reputation tracking. Wins yield rep points.
- **Custom Module 2 (`police.py`)**: Tracks the global Heat Level. Executing missions increases heat; at max heat, the player is Busted.

## Integration Test Design
We created `test_streetrace_integration.py` containing test scenarios that evaluate how these decoupled modules interact when simulating game mechanics:

### 1. Registration & Crew Integration
- Defines a test flow where users register, hire crew, and assign roles. It ensures `ValueError` are properly thrown when crew are added to non-existent users, verifying the data-binding between `RegistrationModule` and `CrewManagementModule`.

### 2. Inventory & Repair
- Tests the degradation of car parts that exist in `InventoryModule` on a `Car` instance originated from `RegistrationModule`.
- Tests the business rule checking for a `mechanic` role assigned via `CrewManagementModule` before permitting a part repair in the `InventoryModule`.

### 3. Race & Results
- Models the end-to-end race loop:
  1. Register users and cars.
  2. Assign "driver" roles to crew members (`CrewManagementModule`).
  3. Enter race (`RaceManagementModule`), which checks for the driver.
  4. Record the outcome (`ResultsModule`).
  5. Verify that `InventoryModule` appropriately degrades participants' car parts.
  6. Verify that `ReputationModule` appropriately increments the winner's points.

### 4. Mission & Police Integration
- Ensures that attempting a mission in `MissionPlanningModule` parses the crew to look for the "spotter" role.
- Exceeding the maximum logic threshold in `PoliceModule` correctly throws business exceptions when the player attempts to enter another race or mission, preventing execution until heat dies down.

## Results
All Integration tests pass successfully, confirming that the StreetRace Manager domain logic perfectly enforces rules across decoupled module domains.
