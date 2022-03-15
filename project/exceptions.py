class ItemNotFound(Exception):
    def __init__(self):
        self.message = "Item not found"


class ItemAlreadyExists(Exception):
    def __init__(self):
        self.message = "Item already exist"

