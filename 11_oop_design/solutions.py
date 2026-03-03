"""
=============================================================================
PATTERN 11: OBJECT-ORIENTED DESIGN (OOP) — SOLUTIONS
=============================================================================

GENERAL TIPS FOR AMAZON OOP INTERVIEWS:
  1. ALWAYS clarify scope first — "Should I handle X?" avoids wasted time
  2. Start top-down: name your classes, then drill into attributes/methods
  3. Use enums for fixed categories (sizes, types, suits)
  4. Favor composition over inheritance unless there's a clear is-a
  5. Keep classes focused — Single Responsibility Principle
  6. Know your design patterns: Builder, Strategy, Observer, Factory

PATTERNS AMAZON LOVES TO SEE:
  - Enums for types/categories
  - Builder pattern (Pizza question)
  - Clean separation of concerns
  - Proper encapsulation (don't expose internals)
=============================================================================
"""

from abc import ABC, abstractmethod
from enum import Enum
import random


# ---------------------------------------------------------------------------
# Problem 1: Design a Parking Lot
# ---------------------------------------------------------------------------
# APPROACH:
#   Entities: Vehicle, ParkingSpot, ParkingFloor, ParkingLot
#   Key relationship: A Vehicle "fits in" a Spot based on size mapping.
#   We use enums for vehicle/spot sizes and a simple fit-check method.
#
# DESIGN DECISIONS:
#   - Ticket is a string "floor-spot_id" for easy lookup
#   - ParkingFloor handles spot allocation, ParkingLot delegates down
#   - Smallest-fit-first strategy (motorcycle → small, car → medium, etc.)
#
# TRICK TO REMEMBER: "Enums for types, fit-check maps sizes, ticket = key."
#
# COMMON MISTAKES:
#   - Forgetting that motorcycles fit in ANY spot, not just small
#   - Not handling the "lot full" case (return None, don't crash)
#   - Over-engineering with abstract vehicle hierarchies
# ---------------------------------------------------------------------------

class VehicleSize(Enum):
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3


class SpotSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


# Mapping: vehicle size → minimum spot size it needs
_VEHICLE_TO_MIN_SPOT = {
    VehicleSize.MOTORCYCLE: SpotSize.SMALL,
    VehicleSize.CAR: SpotSize.MEDIUM,
    VehicleSize.BUS: SpotSize.LARGE,
}


class Vehicle:
    """Represents a vehicle entering the lot."""
    def __init__(self, license_plate: str, size: VehicleSize):
        self.license_plate = license_plate
        self.size = size

    def __repr__(self) -> str:
        return f"Vehicle({self.license_plate}, {self.size.name})"


class ParkingSpot:
    """A single parking spot on a floor."""
    def __init__(self, spot_id: int, size: SpotSize):
        self.spot_id = spot_id
        self.size = size
        self.vehicle: Vehicle | None = None

    @property
    def is_available(self) -> bool:
        return self.vehicle is None

    def can_fit(self, vehicle: Vehicle) -> bool:
        """A vehicle fits if the spot size >= the vehicle's minimum spot size."""
        min_spot = _VEHICLE_TO_MIN_SPOT[vehicle.size]
        return self.is_available and self.size.value >= min_spot.value

    def park(self, vehicle: Vehicle) -> None:
        if not self.can_fit(vehicle):
            raise ValueError(f"Vehicle {vehicle} cannot fit in spot {self.spot_id}")
        self.vehicle = vehicle

    def remove(self) -> Vehicle | None:
        v = self.vehicle
        self.vehicle = None
        return v


class ParkingFloor:
    """A single floor with a collection of spots."""
    def __init__(self, floor_number: int, small: int, medium: int, large: int):
        self.floor_number = floor_number
        self.spots: list[ParkingSpot] = []
        spot_id = 0
        for _ in range(small):
            self.spots.append(ParkingSpot(spot_id, SpotSize.SMALL))
            spot_id += 1
        for _ in range(medium):
            self.spots.append(ParkingSpot(spot_id, SpotSize.MEDIUM))
            spot_id += 1
        for _ in range(large):
            self.spots.append(ParkingSpot(spot_id, SpotSize.LARGE))
            spot_id += 1

    def park_vehicle(self, vehicle: Vehicle) -> ParkingSpot | None:
        """Find the smallest available spot that fits the vehicle."""
        # Spots are already sorted by size (small, medium, large)
        for spot in self.spots:
            if spot.can_fit(vehicle):
                spot.park(vehicle)
                return spot
        return None

    def available_spots(self) -> dict[str, int]:
        result = {"SMALL": 0, "MEDIUM": 0, "LARGE": 0}
        for spot in self.spots:
            if spot.is_available:
                result[spot.size.name] += 1
        return result


class ParkingLot:
    """The top-level parking lot containing multiple floors."""
    def __init__(self, floors: list[ParkingFloor]):
        self.floors = floors
        self.tickets: dict[str, tuple[ParkingFloor, ParkingSpot]] = {}

    def park_vehicle(self, vehicle: Vehicle) -> str | None:
        """Park a vehicle and return a ticket string, or None if full."""
        for floor in self.floors:
            spot = floor.park_vehicle(vehicle)
            if spot is not None:
                ticket = f"{floor.floor_number}-{spot.spot_id}"
                self.tickets[ticket] = (floor, spot)
                return ticket
        return None  # lot is full

    def remove_vehicle(self, ticket: str) -> Vehicle | None:
        """Remove and return the vehicle for the given ticket."""
        if ticket not in self.tickets:
            return None
        floor, spot = self.tickets.pop(ticket)
        return spot.remove()


# ---------------------------------------------------------------------------
# Problem 2: Design a Deck of Cards
# ---------------------------------------------------------------------------
# APPROACH:
#   Card = (Suit, Rank). Deck = list of 52 Cards.
#   Draw pops from the end (top of deck). Shuffle uses random.shuffle.
#
# DESIGN DECISIONS:
#   - Enums for Suit and Rank give type safety and clean repr
#   - Draw from the end of the list (O(1) pop)
#   - Reset recreates the full ordered deck
#
# TRICK TO REMEMBER: "Enum × Enum = 52 cards. Pop = draw. Shuffle = random."
#
# COMMON MISTAKES:
#   - Not raising on draw from empty deck
#   - Using a set (cards need order for shuffling)
#   - Forgetting __repr__ — interviewers want readable output
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
        self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        return f"{self.rank.name} of {self.suit.name}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank


class Deck:
    """A standard 52-card deck."""
    def __init__(self):
        self._cards: list[Card] = []
        self.reset()

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def draw(self) -> Card:
        """Draw and return the top card. Raise if deck is empty."""
        if not self._cards:
            raise IndexError("Cannot draw from an empty deck")
        return self._cards.pop()

    def reset(self) -> None:
        """Reset the deck to a full, ordered 52-card deck."""
        self._cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def remaining(self) -> int:
        return len(self._cards)


# ---------------------------------------------------------------------------
# Problem 3: Design an Elevator System
# ---------------------------------------------------------------------------
# APPROACH:
#   Each Elevator has a current floor, a direction, and a set of destinations.
#   step() moves it one floor toward its next destination.
#   ElevatorSystem dispatches the nearest idle (or same-direction) elevator.
#
# DESIGN DECISIONS:
#   - Destinations stored as a sorted set for efficient next-floor lookup
#   - Direction is recalculated each step based on remaining destinations
#   - Dispatch strategy: pick the elevator with min distance to requested floor
#
# TRICK TO REMEMBER: "Sorted destinations, step one floor at a time,
#   dispatch nearest."
#
# COMMON MISTAKES:
#   - Forgetting to go IDLE when no destinations remain
#   - Not handling direction changes mid-trip
#   - Over-complicating dispatch (start with nearest-idle, then optimize)
# ---------------------------------------------------------------------------

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


class Elevator:
    """A single elevator car."""
    def __init__(self, elevator_id: int, min_floor: int = 0, max_floor: int = 10):
        self.elevator_id = elevator_id
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.current_floor = 0
        self.direction = Direction.IDLE
        self._destinations: set[int] = set()

    def request_floor(self, floor: int) -> None:
        """Add a destination floor (pressed from inside the elevator)."""
        if self.min_floor <= floor <= self.max_floor and floor != self.current_floor:
            self._destinations.add(floor)
            self._update_direction()

    def _update_direction(self) -> None:
        """Recalculate direction based on next destination."""
        if not self._destinations:
            self.direction = Direction.IDLE
            return
        # Pick the closest destination in the current direction,
        # or just the closest overall if idle
        if self.direction == Direction.UP or self.direction == Direction.IDLE:
            above = [f for f in self._destinations if f > self.current_floor]
            below = [f for f in self._destinations if f < self.current_floor]
            if above:
                self.direction = Direction.UP
            elif below:
                self.direction = Direction.DOWN
            else:
                # We're already at a destination
                self.direction = Direction.IDLE
        else:  # DOWN
            below = [f for f in self._destinations if f < self.current_floor]
            above = [f for f in self._destinations if f > self.current_floor]
            if below:
                self.direction = Direction.DOWN
            elif above:
                self.direction = Direction.UP
            else:
                self.direction = Direction.IDLE

    def step(self) -> None:
        """Move the elevator one floor toward its next destination."""
        if self.direction == Direction.IDLE:
            return

        self.current_floor += self.direction.value

        # If we've arrived at a destination, remove it
        if self.current_floor in self._destinations:
            self._destinations.discard(self.current_floor)

        self._update_direction()

    @property
    def is_idle(self) -> bool:
        return self.direction == Direction.IDLE and not self._destinations


class ElevatorSystem:
    """Manages multiple elevators and dispatches requests."""
    def __init__(self, num_elevators: int, num_floors: int):
        self.num_floors = num_floors
        self.elevators = [
            Elevator(i, min_floor=0, max_floor=num_floors)
            for i in range(num_elevators)
        ]

    def call_elevator(self, floor: int, direction: Direction) -> Elevator:
        """Dispatch the best elevator: nearest idle, or nearest same-direction."""
        best = None
        best_dist = float("inf")

        for elev in self.elevators:
            dist = abs(elev.current_floor - floor)
            # Prefer idle elevators, then same-direction
            if elev.is_idle and dist < best_dist:
                best = elev
                best_dist = dist
            elif elev.direction == direction and dist < best_dist:
                best = elev
                best_dist = dist

        # Fallback: just pick the nearest elevator regardless
        if best is None:
            best = min(self.elevators, key=lambda e: abs(e.current_floor - floor))

        best.request_floor(floor)
        return best

    def step_all(self) -> None:
        """Advance all elevators by one step."""
        for elev in self.elevators:
            elev.step()

    def status(self) -> list[dict]:
        """Return current status of all elevators."""
        return [
            {
                "id": e.elevator_id,
                "floor": e.current_floor,
                "direction": e.direction,
                "destinations": sorted(e._destinations),
            }
            for e in self.elevators
        ]


# ---------------------------------------------------------------------------
# Problem 4: Design a Pizza Ordering System
# ---------------------------------------------------------------------------
# APPROACH:
#   Use the BUILDER PATTERN. PizzaBuilder accumulates config, then build()
#   creates an immutable Pizza. Order holds a list of Pizzas and computes
#   the total price.
#
# DESIGN DECISIONS:
#   - Pizza is effectively immutable (attributes set once in __init__)
#   - Builder methods return self for fluent chaining
#   - Price = base price by size + $1.50 per topping
#     - SMALL: $8, MEDIUM: $12, LARGE: $15
#   - Builder validates that size and base are set before build()
#
# TRICK TO REMEMBER: "Builder = set().set().add().build(). Return self
#   for chaining. Validate in build()."
#
# WHY BUILDER PATTERN:
#   - Pizza has many optional parts (toppings)
#   - Construction is step-by-step, not all-at-once
#   - Avoids telescoping constructors (Pizza(size, base, t1, t2, t3...))
#
# COMMON MISTAKES:
#   - Forgetting to return self from builder methods (breaks chaining)
#   - Not validating required fields in build()
#   - Making Pizza mutable after creation
# ---------------------------------------------------------------------------

class PizzaSize(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class PizzaBase(Enum):
    THIN = "Thin Crust"
    THICK = "Thick Crust"
    STUFFED = "Stuffed Crust"


_SIZE_PRICES = {
    PizzaSize.SMALL: 8.00,
    PizzaSize.MEDIUM: 12.00,
    PizzaSize.LARGE: 15.00,
}

_TOPPING_PRICE = 1.50


class Pizza:
    """An immutable pizza. Created only through PizzaBuilder."""
    def __init__(self, size: PizzaSize, base: PizzaBase, toppings: list[str]):
        self.size = size
        self.base = base
        self.toppings = list(toppings)  # defensive copy

    def price(self) -> float:
        """Calculate price: base price by size + $1.50 per topping."""
        return _SIZE_PRICES[self.size] + len(self.toppings) * _TOPPING_PRICE

    def __repr__(self) -> str:
        top_str = ", ".join(self.toppings) if self.toppings else "Plain"
        return f"{self.size.value} {self.base.value} Pizza [{top_str}] — ${self.price():.2f}"


class PizzaBuilder:
    """Builder pattern for constructing a Pizza step by step."""
    def __init__(self):
        self._size: PizzaSize | None = None
        self._base: PizzaBase | None = None
        self._toppings: list[str] = []

    def set_size(self, size: PizzaSize) -> "PizzaBuilder":
        self._size = size
        return self

    def set_base(self, base: PizzaBase) -> "PizzaBuilder":
        self._base = base
        return self

    def add_topping(self, topping: str) -> "PizzaBuilder":
        self._toppings.append(topping)
        return self

    def build(self) -> Pizza:
        """Build and return the Pizza. Raise if size or base not set."""
        if self._size is None:
            raise ValueError("Pizza size is required")
        if self._base is None:
            raise ValueError("Pizza base is required")
        return Pizza(self._size, self._base, self._toppings)


class Order:
    """An order containing one or more pizzas."""
    def __init__(self):
        self._pizzas: list[Pizza] = []

    def add_pizza(self, pizza: Pizza) -> None:
        self._pizzas.append(pizza)

    def total(self) -> float:
        return sum(p.price() for p in self._pizzas)

    def summary(self) -> str:
        lines = [f"  {i+1}. {p}" for i, p in enumerate(self._pizzas)]
        lines.append(f"  TOTAL: ${self.total():.2f}")
        return "Order:\n" + "\n".join(lines)


# ===========================================================================
# TESTS — run with: python -m pytest 11_oop_design/solutions.py -v
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

    def test_multiple_floors(self):
        f1 = ParkingFloor(1, small=0, medium=1, large=0)
        f2 = ParkingFloor(2, small=0, medium=1, large=0)
        lot = ParkingLot([f1, f2])
        c1 = Vehicle("C1", VehicleSize.CAR)
        c2 = Vehicle("C2", VehicleSize.CAR)
        t1 = lot.park_vehicle(c1)
        t2 = lot.park_vehicle(c2)
        self.assertIsNotNone(t1)
        self.assertIsNotNone(t2)
        self.assertNotEqual(t1, t2)


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
        with self.assertRaises(IndexError):
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
        cards1 = [deck1.draw() for _ in range(52)]
        cards2 = [deck2.draw() for _ in range(52)]
        self.assertNotEqual(
            [str(c) for c in cards1],
            [str(c) for c in cards2],
        )

    def test_all_cards_unique(self):
        deck = Deck()
        cards = [deck.draw() for _ in range(52)]
        card_strs = [str(c) for c in cards]
        self.assertEqual(len(card_strs), len(set(card_strs)))


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
        for _ in range(10):
            system.step_all()
        self.assertEqual(elev.current_floor, 5)

    def test_goes_idle_after_arriving(self):
        elev = Elevator(0, min_floor=0, max_floor=10)
        elev.request_floor(3)
        for _ in range(5):
            elev.step()
        self.assertTrue(elev.is_idle)
        self.assertEqual(elev.current_floor, 3)

    def test_dispatch_nearest(self):
        system = ElevatorSystem(num_elevators=2, num_floors=10)
        elev = system.call_elevator(floor=0, direction=Direction.UP)
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

    def test_pizza_price_small_plain(self):
        pizza = PizzaBuilder().set_size(PizzaSize.SMALL).set_base(PizzaBase.THIN).build()
        self.assertAlmostEqual(pizza.price(), 8.00)

    def test_pizza_price_medium_one_topping(self):
        pizza = (
            PizzaBuilder()
            .set_size(PizzaSize.MEDIUM)
            .set_base(PizzaBase.THICK)
            .add_topping("Olives")
            .build()
        )
        self.assertAlmostEqual(pizza.price(), 13.50)

    def test_builder_raises_without_size(self):
        with self.assertRaises(ValueError):
            PizzaBuilder().set_base(PizzaBase.THIN).build()

    def test_builder_raises_without_base(self):
        with self.assertRaises(ValueError):
            PizzaBuilder().set_size(PizzaSize.SMALL).build()

    def test_order_total(self):
        p1 = PizzaBuilder().set_size(PizzaSize.SMALL).set_base(PizzaBase.THIN).build()
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
        self.assertAlmostEqual(order.total(), 27.50)

    def test_order_summary(self):
        pizza = PizzaBuilder().set_size(PizzaSize.SMALL).set_base(PizzaBase.THIN).build()
        order = Order()
        order.add_pizza(pizza)
        summary = order.summary()
        self.assertIn("Order:", summary)
        self.assertIn("$8.00", summary)


if __name__ == "__main__":
    unittest.main()
