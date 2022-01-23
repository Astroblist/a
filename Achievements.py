class Achievement:
    def __init__(self, name, description, status):
        self.name = name
        self.description = description
        self.status = status


cartographer = Achievement("Cartographer!", "Find and use the map for the first time!", "Uncompleted")
sailor = Achievement("Sailor!", "Set to the seas with your repaired ship!", "Uncompleted")
king = Achievement("King Slayer!", "Slay the unruly leader of the land", "Uncompleted")
no_sword = Achievement("Who needs a sword anyway?", "Beat the game without a sword", "Uncompleted")
no_shield = Achievement("Who needs a shield anyway?", "Beat the game without a shield", "Uncompleted")
fists = Achievement("Bear fists!", "Beat the game with your bare hands", "Uncompleted")

Achievement = [cartographer, sailor, king, no_shield, no_sword, fists]
