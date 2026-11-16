import contextlib
import io
from collections.abc import Callable

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("S01", "Acme Supplies", "sales@acme.example")


def make_physical(price: float = 100.0) -> PhysicalProduct:
    return PhysicalProduct("P001", "Guitar", price, 3, make_supplier(), 4.5)


def make_digital(price: float = 50.0) -> DigitalProduct:
    return DigitalProduct("D001", "Puzzle Game", price, 100, make_supplier(), 350.0)


def capture_output(function: Callable[[], object]) -> tuple[object, str]:
    # Runs a function and returns (its return value, everything it printed).
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = function()
    return result, buffer.getvalue()
