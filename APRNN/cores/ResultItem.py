class Result():
    def __init__(self, label, score, items):
        self.label = label
        self.score = score
        self.items = items


class Item():
    def __init__(self, name, score, context, current):
        self.name = name
        self.score = score
        self.context = context
        self.current = current
