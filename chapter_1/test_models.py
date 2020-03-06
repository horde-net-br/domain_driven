import pytest
from datetime import date

from models import Batch, OrderLine, Product
from exceptions import ProductMismatch, UnavailableQuantity

@pytest.fixture
def product():
    return Product(sku='12345JK')


@pytest.fixture
def other_product():
    return Product(sku='12346OP')


@pytest.fixture
def order_line(product):
    return OrderLine('1', product, 10) 


@pytest.fixture
def batch(product):
    return Batch('ref-0001', product, 20, eta=date.today())


def test_allocate_line_to_batch(batch, order_line):
    batch.allocate(order_line)
    assert batch.available_qty == 10
    assert order_line in batch._allocations


def test_allocate_line_with_other_product_raises_product_mismatch(batch, other_product):
    order_line = OrderLine('1', other_product, 10) 
    with pytest.raises(ProductMismatch):
        batch.allocate(order_line)


def test_allocate_line_greater_than_available_qty_raises_unavailable_quantity(batch, product):
    order_line = OrderLine('1', product, 22) 
    with pytest.raises(UnavailableQuantity):
        batch.allocate(order_line)


def test_deallocate_allocated_line(batch, order_line):
    batch._allocations.add(order_line)
    batch.deallocate(order_line)
    assert batch._allocations == set()
