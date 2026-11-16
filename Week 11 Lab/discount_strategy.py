import math
from abc import ABC, abstractmethod


def _check_number(value: float, name: str) -> None:
    # Shared validation: a real, finite number (not a bool, text, NaN or infinity).
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a number.")


class DiscountStrategy(ABC):
    # Strategy pattern: the shared contract for every way of discounting an order total.
    # Order only calls apply(); it does not know (or care) which strategy it was given.

    @abstractmethod
    def apply(self, total: float) -> float:
        # Takes an order total and returns the discounted total.
        pass


class NoDiscount(DiscountStrategy):
    # Returns the total unchanged.

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    # Takes a percentage off the total, e.g. PercentageDiscount(10) takes 10% off.

    def __init__(self, percentage: float) -> None:
        _check_number(percentage, "Percentage")

        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")

        self.__percentage: float = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total - total * self.__percentage / 100


class BulkDiscount(DiscountStrategy):
    # Takes a fixed amount off any total at or above a threshold,
    # e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more.

    def __init__(self, threshold: float, amount: float) -> None:
        _check_number(threshold, "Threshold")
        _check_number(amount, "Discount amount")

        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")

        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")

        self.__threshold: float = threshold
        self.__amount: float = amount

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)
        return total


class StudentDiscount(DiscountStrategy):
    # The fourth strategy: a fixed 5% student discount.
    # Adding this class needed no change to Order (Open/Closed Principle).

    RATE_PERCENT: float = 5.0

    def apply(self, total: float) -> float:
        return total - total * self.RATE_PERCENT / 100
