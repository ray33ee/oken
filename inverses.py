
inverse_list = []

class Delete:
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f"Delete({repr(self.path)})"


class Move:
    pass

class RestoreFile:
    def __init__(self, path, data):
        self.data = data
        self.path = path

    def __repr__(self):
        return f"RestoreFile({repr(self.path)})"
