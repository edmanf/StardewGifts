class GiftReaction:
    def __init__(self, villager, item, reaction):
        self.villager = villager
        self.item = item
        self.reaction = reaction
        
    def __str__(self):  
        if self.reaction == "Neutral":
            return f'{self.villager} is Neutral to {self.item}'
        else:
            return f'{self.villager} {self.reaction}s {self.item}'