from abc import ABC, abstractmethod

class Controller(ABC):
    @abstractmethod
    def feedBtnClicked(self):
        pass

    @abstractmethod
    def playBtnClicked(self):
        pass

    @abstractmethod
    def restBtnClicked(self):
        pass

    @abstractmethod
    def updateView(self):
        pass