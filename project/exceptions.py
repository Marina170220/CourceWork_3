class ItemNotFound(Exception):
    def __init__(self):
        self.message = "Item not found"
