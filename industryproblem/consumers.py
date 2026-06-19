from abc import ABC, abstractmethod

class WaterConsumer(ABC):
    def __init__(self, cid, consumption):
        self.cid = cid
        self.consumption = consumption

    @abstractmethod
    def compute_bill(self, slabs):
        pass


class ResidentialConsumer(WaterConsumer):
    def compute_bill(self, slabs):
        return calculate(self.consumption, slabs)


class CommercialConsumer(WaterConsumer):
    def compute_bill(self, slabs):
        return calculate(self.consumption, slabs)


class IndustrialConsumer(WaterConsumer):
    def compute_bill(self, slabs):
        return calculate(self.consumption, slabs)


def calculate(units, slabs):
    amount = 0
    previous = 0

    for limit, rate in slabs:
        if units > limit:
            amount += (limit - previous) * rate
            previous = limit
        else:
            amount += (units - previous) * rate
            return amount

    amount += (units - previous) * slabs[-1][1]
    return amount