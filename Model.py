from abc import ABC, abstractmethod

class Model(ABC):

    @abstractmethod
    def getHunger(self):
        pass
   
    @abstractmethod
    def getEnergy(self):
        pass
   
    @abstractmethod
    def getMood(self):
        pass
   
    @abstractmethod
    def updateMood(self, energy, hunger):
        pass
   
    @abstractmethod
    def play(self, energy):
        pass
   
    @abstractmethod
    def feed(self,food):
        pass
   
    @abstractmethod
    def rest(self):
        pass
