from abc import ABC, abstractmethod
class View(ABC):
    @abstractmethod
    def displayHunger(self, level):
        pass

    @abstractmethod
    def displayMood(self,level):
        pass

    @abstractmethod
    def displayImage(self):
        pass

    @abstractmethod
    def displayEnergy(self,level):
        pass

    @abstractmethod
    def playBtnClicked(self):
        pass

    @abstractmethod
    def restBtnClicked(self):
        pass