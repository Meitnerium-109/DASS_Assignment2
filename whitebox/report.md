# MoneyPoly White Box Testing Report

## 1.2 Code Quality Analysis
I ran `pylint` on the codebase iteratively and made the following fixes, tracked in git commits:
- **Iteration 1**: Added missing module, class, and function docstrings (`missing-*`).
- **Iteration 2**: Fixed long lines in `cards.py` to adhere to the 100 character limit.
- **Iteration 3**: Removed unused imports (`sys`, `os`, `math`) and unused variables (`old_position`).
- **Iteration 4**: Refactored `Player`, `Property`, and `Game` to resolve `R0902` (too many instance attributes) by grouping fields and using `@property` wrappers. Refactored `Game._apply_card` and `_move_and_resolve` to use dictionary handlers and solve `R0912` (too many branches).
- **Iteration 5**: Final logic cleanups: fixed minor `W0702` (bare except) in `ui.py`, `W0201` initialized variables, line lengths, and missing newlines.
**Final Pylint Score:** 10.00 / 10

## 1.3 White Box Test Cases
I created comprehensive automated tests using `pytest` in `test_moneypoly.py`. The tests cover standard branches, exceptions, edge cases (zero values), and structural behaviors layout.

**Test Cases Created:**
1. `test_player_money`: Validates the `add_money` and `deduct_money` paths, testing negative additions.
2. `test_player_movement`: Validates position updates and `move` wrapping around the board.
3. `test_property_rent`: Evaluates standard rent, mortgage rent (which should be 0), and the full-group multiplier.
4. `test_bank_operations`: Tests boundary condition checking `ValueError` on insufficient payouts.
5. `test_game_bankruptcy`: Triggers the `is_bankrupt` checks and handles returning items to `owner is None`.
6. `test_cards_deck`: Validates drawing logic and wrap-around reshuffle indices.
7. `test_game_jail_logic`: Creates mock interactive prompts to validate `Get Out of Jail` cards.
8. `test_taxes_and_cards`: Simulates direct card and space application (tax deduct).

**Bugs Discovered:**
- **Error 1:** In `PropertyGroup.all_owned_by()`, the method was returning `any(p.owner == player for p in self.properties)` instead of `all()`. This caused rent multipliers to apply even when players only owned a single property of a group!
- **Fix:** Switched `any` to `all` in `property.py`. (Committed as "Error 1: ...")
