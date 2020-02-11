class Item:
    def __init__(self,
                 name=None,
                 attributes=None):
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes
        self.name = name
