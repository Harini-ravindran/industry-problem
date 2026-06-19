from abc import ABC, abstractmethod


def calculate_slab_bill(consumption, slabs):

    bill = 0
    previous_limit = 0

    for slab in slabs:

        limit = slab["upto"]
        rate = slab["rate"]

        if limit is None:
            bill += (consumption - previous_limit) * rate
            break

        if consumption > limit:
            bill += (limit - previous_limit) * rate
            previous_limit = limit
        else:
            bill += (consumption - previous_limit) * rate
            break

    return bill


class WaterConsumer(ABC):

    def __init__(self, customer_id, consumption, slabs):
        self.customer_id = customer_id
        self.consumption = consumption
        self.slabs = slabs

    @abstractmethod
    def compute_bill(self):
        pass


class ResidentialConsumer(WaterConsumer):

    def compute_bill(self):
        return calculate_slab_bill(
            self.consumption,
            self.slabs
        )


class CommercialConsumer(WaterConsumer):

    def compute_bill(self):
        return calculate_slab_bill(
            self.consumption,
            self.slabs
        )


class IndustrialConsumer(WaterConsumer):

    def compute_bill(self):
        return calculate_slab_bill(
            self.consumption,
            self.slabs
        )