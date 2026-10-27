class vec2:
    def __init__(self, *args):
        if len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        else:
            self.x = args[0][0]
            self.y = args[0][1]

    # def __init__(self, pos: tuple[int, int]):
    #     self.x = pos[0]
    #     self.y = pos[1]

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"
