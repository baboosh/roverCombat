class PlayerData:

    def __init__(self):
        self.selected_rover = None
        self.rovers = []

    def getRovers(self):
        return self.rovers

    def getRover(self):
        return self.selected_rover