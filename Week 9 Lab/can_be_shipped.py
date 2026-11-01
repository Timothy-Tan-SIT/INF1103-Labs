from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    # Interface-style abstract base class.
    # Any class that "signs this contract" must be able to calculate a shipping cost.
    # It holds no attributes and no shipping logic: that is up to each implementing class.

    @abstractmethod
    def calculate_shipping_cost(self):
        # Returns the cost of shipping this object.
        pass
