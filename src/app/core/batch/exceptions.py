

class BatchException(object):
    class OutOfStock(Exception):
        pass
    class InvalidSku(Exception):
        pass
