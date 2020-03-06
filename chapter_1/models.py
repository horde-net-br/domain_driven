from collections import namedtuple
from dataclasses import dataclass
from datetime import date
from typing import Optional

from exceptions import ProductMismatch, UnavailableQuantity

Product = namedtuple('Product', ['sku'])

@dataclass(frozen=True)
class OrderLine:
    id_: str
    product: Product
    qty: int


class Batch:
    def __init__(self, reference: str, product: Product, starting_quantity: int, eta: Optional[date]):
        self.reference = reference
        self.product = product
        self.starting_quantity = starting_quantity
        self.eta = eta
        self._allocations = set()  # type: Set[OrderLine]

    @property
    def available_qty(self):
        return self.starting_quantity - sum((x.qty for x in self._allocations))

    def allocate(self, line):
        if line.product != self.product:
            raise ProductMismatch()
        if self.available_qty < line.qty:
            raise UnavailableQuantity()
        self._allocations.add(line)

    def deallocate(self, line):
        if line in self._allocations:
            self._allocations.remove(line)

