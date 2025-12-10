from Model import Model
import json
import os


class PetModel(Model):

    def __init__(self):
        self.hunger = 50
        self.energy = 100
        self.mood ="Neutral"


    def feed(self,food):
        if self.hunger < 100:
            self.hunger = min(100, self.hunger + food)
            return "Yum!"
        else:
            return "I'm full!"


    def play(self, energy):
        if self.energy == 0:
            return "I'm too tired to play!"
        elif self.energy < 50:
            # still allow a small play but with tired message
            self.energy = max(0, self.energy - 10)
            self.hunger = max(0, self.hunger - 10)
            return "I'm tired..."
        else:
            self.energy = max(0, self.energy - energy)
            self.hunger = max(0, self.hunger - 10)
            return "Let's play!"

    def rest(self):
        if self.energy >= 100 :
            return "I'm not tired!"
        else:
            self.energy = min(100, self.energy + 10)
            return "Zzzz..."
    

    def updateMood(self, energy, hunger):
        if self.energy == 50 and self.hunger == 50:
           self.mood = "Neutral"

        elif self.energy < 50 and self.hunger < 50: 
            self.mood = "Sad"
        else:
            self.mood = "Happy"
        

    # Implement abstract getters required by Model ABC
    def getHunger(self):
        return self.hunger

    def getEnergy(self):
        return self.energy

    def getMood(self):
        return self.mood

    # persistence helpers
    def to_dict(self):
        return {
            'hunger': int(self.hunger),
            'energy': int(self.energy),
            'mood': str(self.mood)
        }

    def from_dict(self, data: dict):
        try:
            self.hunger = int(data.get('hunger', self.hunger))
            self.energy = int(data.get('energy', self.energy))
            self.mood = str(data.get('mood', self.mood))
        except Exception:
            # ignore and keep defualts
            pass

    def save_to_file(self, path='save.json'):
        try:
            d = self.to_dict()
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def load_from_file(self, path='save.json'):
        try:
            if not os.path.exists(path):
                return False
            with open(path, 'r', encoding='utf-8') as f:
                d = json.load(f)
            self.from_dict(d)
            return True
        except Exception:
            return False
