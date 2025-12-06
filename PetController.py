class PetController(Controller):

    def __init__ (self, model, view):
        self.model = model
        self.view = view

    def feedBtnClicked(self):
        food_amount = 10
        self.model.feed(food_amount)
        self.model.updateMood()
        #self.view.updateHungerDisplay(self.model.hunger)
        #self.view.updateMoodDis(self.model.mood)

    def playBtnClicked(self):
        energy_amount =  10
        self.model.play(energy_amount)
        self.model.updateMood()
        #implement the view base on the buttoms we make

    def restBtnClicked(self):
        energy_amount = 10
        self.model.play(energy_amount)
        self.model.updateMood()
        