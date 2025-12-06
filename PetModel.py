class PetModel(Model):

    def __init__(self):
        self.hunger = 50
        self.energy = 100
        self.mood ="Neutral"


    def feed(self,food):
        if self.hunger < 50:
            print("Yum!")
            self.hunger = self.hunger+10
        else:
            print("Im full!")


    def play(self, energy):
        if self.energy < 50:
            print("Im tired....")
        else:
            print("Let's play!")
            self.energy = self.energy - 10


    def rest(self,energy):
        if self.energy >= 50 :
            print("Im not tired!")
        else:
            print("Zzzz...")
            self.energy = self.energy + 10
    

    def updateMood(self, energy, hunger):
        if self.energy == 5 and self.hunger == 5:
           self.mood = "Neutral"

        elif self.energy < 5 and self.hunger < 5: 
            self.mood = "Sad"
        else:
            self.mood = "Happy"
        