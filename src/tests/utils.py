from uuid import uuid4


def random_suffix():
    return uuid4().hex[:6]


def random_sku(name: str = ""):
    return f"sku-{name}-{random_suffix()}"


def random_batch(name: int):
    return f"batch-{name}-{random_suffix()}"


def random_order(name: int):
    return f"order-{name}-{random_suffix()}"
