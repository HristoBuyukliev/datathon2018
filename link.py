class Link:

    def __init__(self, source, target, strength):
        self.source = source
        self.target = target
        self.strength = strength

    def __hash__(self):
        return (self.source + self.target).__hash__()

    def __eq__(self, other):
        return self.source == other.source and self.target == other.target
