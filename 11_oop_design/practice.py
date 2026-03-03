"""
=============================================================================
PATTERN 11: OBJECT-ORIENTED DESIGN (OOP)
=============================================================================

HOW TO RECOGNIZE:
- "Design a system for..." or "Model this real-world thing in code"
- Interviewer asks you to define classes, relationships, and methods
- Focus is on encapsulation, inheritance, polymorphism, and abstraction
- You're expected to talk through your design BEFORE coding

KEY IDEA:
  Identify the core entities (nouns → classes), their attributes,
  and the actions they perform (verbs → methods). Use inheritance
  and composition to model relationships. Keep it simple — don't
  over-engineer. Interviewers want clean, extensible code.

APPROACH (use this framework every time):
  1. CLARIFY — Ask what features are in scope
  2. CORE OBJECTS — Identify the main classes (nouns in the problem)
  3. RELATIONSHIPS — Map out has-a / is-a between objects
  4. KEY METHODS — Define the critical actions
  5. CODE IT — Implement the classes, keep it clean

AMAZON FAVORITES (confirmed on Glassdoor):
  - Design a Parking Lot
  - Design a Deck of Cards / Blackjack
  - Design an Elevator System
  - Design a Pizza Ordering System
=============================================================================
"""

from abc import ABC, abstractmethod
from enum import Enum


# ---------------------------------------------------------------------------
# Problem 1: Design a Parking Lot
# ---------------------------------------------------------------------------
# Design an object-oriented parking lot system with the following requirements:
#
# - The parking lot has multiple floors
# - Each floor has spots of different sizes: SMALL, MEDIUM, LARGE
# - Vehicles come in types: MOTORCYCLE, CAR, BUS
#   - Motorcycles fit in any spot
#   - Cars fit in MEDIUM or LARGE spots
#   - Buses fit only in LARGE spots
# - The system can:
#   - Park a vehicle (returns a ticket or None if full)
#   - Remove a vehicle by ticket
#   - Check available spots per floor
#
# Source: Glassdoor — one of the most frequently reported Amazon OOP questions
#
# Hint: Think about enums for sizes/types, a Spot class, a Floor class,
#       and a ParkingLot class that ties it all together.
# ---------------------------------------------------------------------------

class VehicleSize(Enum):
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3


class SpotSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Vehicle:
    """Represents a vehicle entering the lot."""
    def __init__(self, license_plate: str, size: VehicleSize):
        pass  # YOUR CODE HERE


class ParkingSpot:
    """A single parking spot on a floor."""
    def __init__(self, spot_id: int, size: SpotSize):
        pass  # YOUR CODE HERE

    def can_fit(self, vehicle: Vehicle) -> bool:
        """Return True if this spot can fit the given vehicle."""
        pass  # YOUR CODE HERE

    def park(self, vehicle: Vehicle) -> None:
        pass  # YOUR CODE HERE

    def remove(self) -> None:
        pass  # YOUR CODE HERE


class ParkingFloor:
    """A single floor with a collection of spots."""
    def __init__(self, floor_number: int, small: int, medium: int, large: int):
        """Create a floor with the given number of each spot size."""
        pass  # YOUR CODE HERE

    def park_vehicle(self, vehicle: Vehicle) -> "ParkingSpot | None":
        """Find the smallest available spot that fits the vehicle."""
        pass  # YOUR CODE HERE

    def available_spots(self) -> dict[str, int]:
        """Return a count of available spots by size."""
        pass  # YOUR CODE HERE


class ParkingLot:
    """The top-level parking lot containing multiple floors."""
    def __init__(self, floors: list[ParkingFloor]):
        pass  # YOUR CODE HERE

    def park_vehicle(self, vehicle: Vehicle) -> str | None:
        """Park a vehicle and return a ticket string, or None if full."""
        pass  # YOUR CODE HERE

    def remove_vehicle(self, ticket: str) -> Vehicle | None:
        """Remove and return the vehicle for the given ticket."""
        pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 2: Design a Deck of Cards
# ---------------------------------------------------------------------------
# Design an OOP system for a standard 52-card deck that supports:
#
# - Creating a full deck of 52 cards (4 suits x 13 ranks)
# - Shuffling the deck
# - Drawing cards from the top
# - Resetting the deck back to a full, unshuffled state
# - Checking how many cards remain
#
# Source: Glassdoor — "Use object oriented programming to design a deck of cards"
#
# Hint: Use enums for Suit and Rank, a Card class, and a Deck class.
#       Think about what happens when you draw from an empty deck.
# ---------------------------------------------------------------------------

class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Card:
    """A single playing card."""
    def __init__(self, suit: Suit, rank: Rank):
        pass  # YOUR CODE HERE

    def __repr__(self) -> str:
        """Return e.g. 'ACE of SPADES'"""
        pass  # YOUR CODE HERE


class Deck:
    """A standard 52-card deck."""
    def __init__(self):
        pass  # YOUR CODE HERE

    def shuffle(self) -> None:
        pass  # YOUR CODE HERE

    def draw(self) -> Card:
        """Draw and return the top card. Raise if deck is empty."""
        pass  # YOUR CODE HERE

    def reset(self) -> None:
        """Reset the deck to a full, ordered 52-card deck."""
        pass  # YOUR CODE HERE

    def remaining(self) -> int:
        pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 3: Design an Elevator System
# ---------------------------------------------------------------------------
# Design an OOP elevator system for a building with the following requirements:
#
# - A building has N floors and M elevators
# - Each elevator tracks its current floor and direction (UP, DOWN, IDLE)
# - Users can request an elevator from any floor (external button)
# - Users inside an elevator can select a destination floor
# - The system dispatches the nearest suitable elevator
#
# Source: Glassdoor — "Design an elevator system (Object oriented design)"
#
# Hint: Think about Direction enum, Elevator class (with a request queue),
#       and an ElevatorSystem that dispatches requests.
# ---------------------------------------------------------------------------

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


class Elevator:
    """A single elevator car."""
    def __init__(self, elevator_id: int, min_floor: int = 0, max_floor: int = 10):
        pass  # YOUR CODE HERE

    def request_floor(self, floor: int) -> None:
        """Add a destination floor (pressed from inside the elevator)."""
        pass  # YOUR CODE HERE

    def step(self) -> None:
        """Move the elevator one step: go to next floor or go idle."""
        pass  # YOUR CODE HERE

    @property
    def is_idle(self) -> bool:
        pass  # YOUR CODE HERE


class ElevatorSystem:
    """Manages multiple elevators and dispatches requests."""
    def __init__(self, num_elevators: int, num_floors: int):
        pass  # YOUR CODE HERE

    def call_elevator(self, floor: int, direction: Direction) -> Elevator:
        """Dispatch the best elevator to the requesting floor."""
        pass  # YOUR CODE HERE

    def step_all(self) -> None:
        """Advance all elevators by one step."""
        pass  # YOUR CODE HERE

    def status(self) -> list[dict]:
        """Return current status of all elevators."""
        pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Design a Pizza Ordering System
# ---------------------------------------------------------------------------
# Design an OOP system for ordering pizzas with the following requirements:
#
# - Pizzas have a size (SMALL, MEDIUM, LARGE), a base (THIN, THICK, STUFFED),
#   and a list of toppings
# - Use the BUILDER PATTERN to construct pizzas step by step
# - An Order can contain multiple pizzas
# - The system should calculate the total price
#
# Source: Glassdoor — "Given a pizza with 'size, toppings, and a base'...
#         how would you represent this 'pizza' in code?"
#
# Hint: This is testing if you know the Builder pattern. The interviewer
#       wants to see Pizza, PizzaBuilder, and Order classes.
# ---------------------------------------------------------------------------

class PizzaSize(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class PizzaBase(Enum):
    THIN = "Thin Crust"
    THICK = "Thick Crust"
    STUFFED = "Stuffed Crust"


class Pizza:
    """An immutable pizza. Created only through PizzaBuilder."""
    def __init__(self, size: PizzaSize, base: PizzaBase, toppings: list[str]):
        pass  # YOUR CODE HERE

    def price(self) -> float:
        """Calculate price: base price by size + $1.50 per topping."""
        pass  # YOUR CODE HERE

    def __repr__(self) -> str:
        pass  # YOUR CODE HERE


class PizzaBuilder:
    """Builder pattern for constructing a Pizza step by step."""
    def __init__(self):
        pass  # YOUR CODE HERE

    def set_size(self, size: PizzaSize) -> "PizzaBuilder":
        pass  # YOUR CODE HERE

    def set_base(self, base: PizzaBase) -> "PizzaBuilder":
        pass  # YOUR CODE HERE

    def add_topping(self, topping: str) -> "PizzaBuilder":
        pass  # YOUR CODE HERE

    def build(self) -> Pizza:
        """Build and return the Pizza. Raise if size or base not set."""
        pass  # YOUR CODE HERE


class Order:
    """An order containing one or more pizzas."""
    def __init__(self):
        pass  # YOUR CODE HERE

    def add_pizza(self, pizza: Pizza) -> None:
        pass  # YOUR CODE HERE

    def total(self) -> float:
        pass  # YOUR CODE HERE

    def summary(self) -> str:
        pass  # YOUR CODE HERE


# ===========================================================================
# TESTS — run with: python -m pytest 11_oop_design/practice.py -v
# ===========================================================================
import unittest


class TestParkingLot(unittest.TestCase):
    def test_park_and_remove_car(self):
        floor = ParkingFloor(1, small=1, medium=2, large=1)
        lot = ParkingLot([floor])
        car = Vehicle("ABC-123", VehicleSize.CAR)
        ticket = lot.park_vehicle(car)
        self.assertIsNotNone(ticket)
        removed = lot.remove_vehicle(ticket)
        self.assertEqual(removed.license_plate, "ABC-123")

    def test_motorcycle_fits_any_spot(self):
        floor = ParkingFloor(1, small=1, medium=0, large=0)
        lot = ParkingLot([floor])
        moto = Vehicle("MOTO-1", VehicleSize.MOTORCYCLE)
        ticket = lot.park_vehicle(moto)
        self.assertIsNotNone(ticket)

    def test_bus_needs_large_spot(self):
        floor = ParkingFloor(1, small=2, medium=2, large=0)
        lot = ParkingLot([floor])
        bus = Vehicle("BUS-1", VehicleSize.BUS)
        ticket = lot.park_vehicle(bus)
        self.assertIsNone(ticket)

    def test_lot_full(self):
        floor = ParkingFloor(1, small=0, medium=1, large=0)
        lot = ParkingLot([floor])
        car1 = Vehicle("CAR-1", VehicleSize.CAR)
        car2 = Vehicle("CAR-2", VehicleSize.CAR)
        lot.park_vehicle(car1)
        ticket2 = lot.park_vehicle(car2)
        self.assertIsNone(ticket2)

    def test_available_spots(self):
        floor = ParkingFloor(1, small=2, medium=3, large=1)
        lot = ParkingLot([floor])
        car = Vehicle("CAR-1", VehicleSize.CAR)
        lot.park_vehicle(car)
        avail = floor.available_spots()
        self.assertEqual(avail["MEDIUM"], 2)


class TestDeckOfCards(unittest.TestCase):
    def test_full_deck(self):
        deck = Deck()
        self.assertEqual(deck.remaining(), 52)

    def test_draw_reduces_count(self):
        deck = Deck()
        card = deck.draw()
        self.assertIsInstance(card, Card)
        self.assertEqual(deck.remaining(), 51)

    def test_draw_all(self):
        deck = Deck()
        for _ in range(52):
            deck.draw()
        self.assertEqual(deck.remaining(), 0)

    def test_draw_from_empty_raises(self):
        deck = Deck()
        for _ in range(52):
            deck.draw()
        with self.assertRaises(Exception):
            deck.draw()

    def test_reset(self):
        deck = Deck()
        for _ in range(10):
            deck.draw()
        deck.reset()
        self.assertEqual(deck.remaining(), 52)

    def test_shuffle_changes_order(self):
        deck1 = Deck()
        deck2 = Deck()
        deck2.shuffle()
        # Extremely unlikely to stay in same order after shuffle
        cards1 = [deck1.draw() for _ in range(52)]
        cards2 = [deck2.draw() for _ in range(52)]
        self.assertNotEqual(
            [str(c) for c in cards1],
            [str(c) for c in cards2],
        )


class TestElevatorSystem(unittest.TestCase):
    def test_elevator_starts_idle(self):
        system = ElevatorSystem(num_elevators=2, num_floors=10)
        for s in system.status():
            self.assertEqual(s["direction"], Direction.IDLE)
            self.assertEqual(s["floor"], 0)

    def test_request_floor(self):
        system = ElevatorSystem(num_elevators=1, num_floors=10)
        elev = system.call_elevator(floor=0, direction=Direction.UP)
        elev.request_floor(5)
        # Step until the elevator reaches floor 5
        for _ in range(10):
            system.step_all()
        self.assertEqual(elev.current_floor, 5)

    def test_dispatch_nearest(self):
        system = ElevatorSystem(num_elevators=2, num_floors=10)
        # Move elevator 0 to floor 5
        system.call_elevator(floor=0, direction=Direction.UP)
        system.status()  # both at 0
        elev = system.call_elevator(floor=0, direction=Direction.UP)
        # The one dispatched should be at floor 0 (nearest)
        self.assertEqual(elev.current_floor, 0)


class TestPizzaOrdering(unittest.TestCase):
    def test_build_pizza(self):
        pizza = (
            PizzaBuilder()
            .set_size(PizzaSize.LARGE)
            .set_base(PizzaBase.THIN)
            .add_topping("Pepperoni")
            .add_topping("Mushrooms")
            .build()
        )
        self.assertEqual(pizza.size, PizzaSize.LARGE)
        self.assertEqual(pizza.base, PizzaBase.THIN)
        self.assertEqual(len(pizza.toppings), 2)

    def test_pizza_price(self):
        pizza = (
            PizzaBuilder()
            .set_size(PizzaSize.MEDIUM)
            .set_base(PizzaBase.THICK)
            .add_topping("Olives")
            .build()
        )
        # Medium = $12.00 + 1 topping * $1.50 = $13.50
        self.assertAlmostEqual(pizza.price(), 13.50)

    def test_builder_raises_without_size(self):
        with self.assertRaises(ValueError):
            PizzaBuilder().set_base(PizzaBase.THIN).build()

    def test_order_total(self):
        p1 = (
            PizzaBuilder()
            .set_size(PizzaSize.SMALL)
            .set_base(PizzaBase.THIN)
            .build()
        )
        p2 = (
            PizzaBuilder()
            .set_size(PizzaSize.LARGE)
            .set_base(PizzaBase.STUFFED)
            .add_topping("Pepperoni")
            .add_topping("Sausage")
            .add_topping("Bacon")
            .build()
        )
        order = Order()
        order.add_pizza(p1)
        order.add_pizza(p2)
        # Small = $8.00, Large = $15.00 + 3*$1.50 = $19.50 → total = $27.50
        self.assertAlmostEqual(order.total(), 27.50)


if __name__ == "__main__":
    unittest.main()
