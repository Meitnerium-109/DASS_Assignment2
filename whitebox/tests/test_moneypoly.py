import pytest
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup
from moneypoly.game import Game
from moneypoly.board import Board

@pytest.fixture
def board(): return Board()
@pytest.fixture
def game(): return Game()
@pytest.mark.parametrize("amt", range(-20, 20))
def test_wb_financial(amt):
    p = Player("p1")
    if amt < 0:
        with pytest.raises(ValueError): p.add_money(amt)
        with pytest.raises(ValueError): p.deduct_money(amt)
    else:
        p.add_money(amt)
        assert p.balance == 1500 + amt

@pytest.mark.parametrize("steps", range(1, 41))
def test_wb_movement(steps):
    p = Player("p1")
    p.move(steps)
    assert p.position == steps % 40

@pytest.mark.parametrize("rent", range(10, 50))
def test_wb_rent(rent):
    p = Player("p1")
    prop = Property({"name": "A", "position": 1, "price": 100, "base_rent": rent})
    prop.owner = p
    group = PropertyGroup("Red", "red")
    group.add_property(prop)
    assert group.all_owned_by(p) is True
    assert prop.get_rent() == rent * 2

