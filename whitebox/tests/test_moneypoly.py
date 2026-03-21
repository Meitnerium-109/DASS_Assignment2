import pytest
from inspect import signature

from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup
from moneypoly.bank import Bank
from moneypoly.dice import Dice
from moneypoly.game import Game
from moneypoly.board import Board
from moneypoly.config import STARTING_BALANCE, GO_SALARY
from moneypoly.cards import CHANCE_CARDS

@pytest.fixture(autouse=True)
def mock_input(monkeypatch):
    """Prevent tests from hanging on input prompts."""
    monkeypatch.setattr("builtins.input", lambda prompt="": "s")

def test_player_money():
    player = Player("Alice", balance=1500)
    player.add_money(500)
    assert player.balance == 2000
    
    player.deduct_money(200)
    assert player.balance == 1800

    # Edge cases
    with pytest.raises(ValueError):
        player.add_money(-50)
    
    with pytest.raises(ValueError):
        player.deduct_money(-10)

def test_player_movement():
    player = Player("Alice", balance=1500)
    pos = player.move(5)
    assert pos == 5
    assert player.position == 5

    # Wrap around Board logic
    player.position = 38
    pos = player.move(4)
    assert pos == 2
    # The game handles GO_SALARY explicitly, not player class directly?
    # Actually wait! The Go salary is handled in Game logic!
    # So `player.move` doesn't change `balance`. Let's test that it shouldn't.

def test_property_rent():
    group = PropertyGroup("Brown", "brown")
    prop1 = Property({"name": "Mediterranean", "position": 1, "price": 60, "base_rent": 2}, group=group)
    prop2 = Property({"name": "Baltic", "position": 3, "price": 60, "base_rent": 4}, group=group)
    
    p1 = Player("P1", balance=1500)
    prop1.owner = p1
    
    # Assert get_rent correctly checks properties list of the group
    # Wait, the multiplier logic checks `group.owns_all(self.owner)`
    assert group.all_owned_by(p1) == (len(group.properties) == len([p for p in group.properties if p.owner == p1]))


def test_bank_operations():
    bank = Bank()
    # Payout beyond funds
    with pytest.raises(ValueError):
        bank.pay_out(9999999) 

def test_game_bankruptcy():
    game = Game(["P1", "P2"])
    p1 = game.players[0]
    p1.balance = -10
    
    assert p1.is_bankrupt() == True
    
    # Assign property to simulate release on bankruptcy
    prop = game.board.get_property_at(1)
    prop.owner = p1
    p1.add_property(prop)
    
    game._check_bankruptcy(p1)
    assert prop.owner is None
    assert p1.is_eliminated == True
    assert p1 not in game.players

def test_cards_deck():
    from moneypoly.cards import CardDeck
    test_cards = [{"action": "collect", "value": 10}, {"action": "pay", "value": 15}]
    deck = CardDeck(test_cards)
    
    assert deck.cards_remaining() == 2
    c1 = deck.draw()
    c2 = deck.draw()
    assert c1["action"] == "collect"
    assert c2["action"] == "pay"
    
    # Cycles back
    assert deck.cards_remaining() == 2
    c3 = deck.draw()
    assert c3["action"] == "collect"

    deck.reshuffle()
    assert len(deck) == 2

def test_game_jail_logic():
    game = Game(["P1", "P2"])
    p1 = game.players[0]
    
    # Send to jail
    game._move_and_resolve(p1, 0) # Just setting up
    p1.go_to_jail()
    assert p1.in_jail == True
    
    # Uses card if available
    p1.get_out_of_jail_cards = 1
    # We must patch confirm to return True
    import moneypoly.ui as ui_module
    original_confirm = ui_module.confirm
    ui_module.confirm = lambda prompt: True
    
    try:
        game.play_turn()
        # Used card, rolled, so should be out of jail
        assert p1.get_out_of_jail_cards == 0
        assert p1.in_jail == False
        assert p1.position != 10 # Should have moved
    finally:
        ui_module.confirm = original_confirm

def test_taxes_and_cards():
    game = Game(["P1", "P2"])
    p1 = game.players[0]
    p1.position = 0

    # Land on Income Tax (position 4)
    game._move_and_resolve(p1, 4)
    # Deducts $200
    assert p1.balance == 1300
    
    # Land on free parking
    game._move_and_resolve(p1, 16) # Position 20
    assert p1.balance == 1300 # Unchanged
    
    # Apply card directly
    game._apply_card(p1, {"action": "collect", "value": 50, "description": ""})
    assert p1.balance == 1350

