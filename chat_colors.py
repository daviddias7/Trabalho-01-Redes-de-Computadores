class Colors:
    def __init__(self):
        self.index = 0

        self.colors = ["31", "32", "33", "34", "35", "36", "37", "90", "91", "92", "93", "94", "96", "97"]

    def get_color(self):
        cor = self.colors[self.index]
        self.index+=1
        if self.index == len(self.colors):
            self.index = 0
        return cor
