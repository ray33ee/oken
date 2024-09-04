
import overrides

inverse_list = []

class Remove:
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f"Remove({repr(self.path)})"


class Move:
    pass

class RestoreFile:
    def __init__(self, path):
        with overrides._open(path, "rb") as bfh:
            self.data = bfh.read()

        self.path = path

    def __repr__(self):
        return f"RestoreFile({repr(self.path)})"

class Rmdir:
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f"Rmdir({repr(self.path)})"

class Mkdir:
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f"Mkdir({repr(self.path)})"

class Move:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __repr__(self):
        return f"Move({repr(self.src)}, {repr(self.dst)})"
