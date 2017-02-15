class Result():
    def __init__(self, degree, items):
        self.degree = degree
        self.items = items


class Item():
    def __init__(self, name, score, context, current):
        self.name = name
        self.score = score
        self.context = context
        self.current = current
