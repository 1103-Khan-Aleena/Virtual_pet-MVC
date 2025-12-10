from Controller import Controller
class PetController(Controller):

    def __init__ (self, model, view):
        self.model = model
        self.view = view

    def feedBtnClicked(self):
        food_amount = 10
        msg = self.model.feed(food_amount)
        self.model.updateMood(self.model.energy, self.model.hunger)
        if hasattr(self.view, 'updateHungerDisplay'):
            self.view.updateHungerDisplay(self.model.hunger)
        if hasattr(self.view, 'updateMoodDis'):
            self.view.updateMoodDis(self.model.mood)
        if hasattr(self.view, 'updateStatus') and msg is not None:
            self.view.updateStatus(msg)
        # play a temporary feeding animation then revert to the mood/default image
        if hasattr(self.view, 'play_action'):
            try:
                # capture current model state to show immediately after action
                m = self.model.mood
                e = self.model.energy
                h = self.model.hunger
                self.view.play_action('ActionFeed', on_finished=lambda m=m, e=e, h=h: self.view.setImageForState(m, e, h))
            except Exception:
                if hasattr(self.view, 'setImageForState'):
                    self.view.setImageForState(self.model.mood, self.model.energy, self.model.hunger)
        elif hasattr(self.view, 'setImageForState'):
            self.view.setImageForState(self.model.mood, self.model.energy, self.model.hunger)
        #keep the state even after the action
        try:
            self.model.save_to_file()
        except Exception:
            pass

    def playBtnClicked(self):
        energy_amount =  10
        msg = self.model.play(energy_amount)
        self.model.updateMood(self.model.energy, self.model.hunger)
        #implement the view base on the buttoms I have made
        if hasattr(self.view, 'updateEnergyDisplay'):
            self.view.updateEnergyDisplay(self.model.energy)
        if hasattr(self.view, 'updateMoodDis'):
            self.view.updateMoodDis(self.model.mood)
        if hasattr(self.view, 'updateHungerDisplay'):
            self.view.updateHungerDisplay(self.model.hunger)
        if hasattr(self.view, 'updateStatus') and msg is not None:
            self.view.updateStatus(msg)
        if hasattr(self.view, 'play_action'):
            try:
                m = self.model.mood
                e = self.model.energy
                h = self.model.hunger
                self.view.play_action('ActionPlay', on_finished=lambda m=m, e=e, h=h: self.view.setImageForState(m, e, h))
            except Exception:
                if hasattr(self.view, 'setImageForState'):
                    self.view.setImageForState(self.model.mood, self.model.energy, self.model.hunger)
        elif hasattr(self.view, 'setImageForState'):
            self.view.setImageForState(self.model.mood, self.model.energy, self.model.hunger)
        # persist state after action
        try:
            self.model.save_to_file()
        except Exception:
            pass


    def restBtnClicked(self):
        # call rest on the model (no arg)
        msg = self.model.rest()
        self.model.updateMood(self.model.energy, self.model.hunger)
        if hasattr(self.view, 'updateEnergyDisplay'):
            self.view.updateEnergyDisplay(self.model.energy)
        if hasattr(self.view, 'updateMoodDis'):
            self.view.updateMoodDis(self.model.mood)
        if hasattr(self.view, 'updateStatus') and msg is not None:
            self.view.updateStatus(msg)
        if hasattr(self.view, 'play_action'):
            try:
                m = self.model.mood
                e = self.model.energy
                h = self.model.hunger
                self.view.play_action('ActionRest', on_finished=lambda m=m, e=e, h=h: self.view.setImageForState(m, e, h))
            except Exception:
                if hasattr(self.view, 'setImageForState'):
                    self.view.setImageForState(self.model.mood, self.model.energy, self.model.hunger)
        elif hasattr(self.view, 'setImageForState'):
            self.view.setImageForState(self.model.mood, self.model.energy, self.model.hunger)
        # persist state after action
        try:
            self.model.save_to_file()
        except Exception:
            pass
        
    def updateView(self):
        # Refresh view from model state
        if hasattr(self.view, 'updateHungerDisplay'):
            self.view.updateHungerDisplay(self.model.hunger)
        if hasattr(self.view, 'updateEnergyDisplay'):
            self.view.updateEnergyDisplay(self.model.energy)
        if hasattr(self.view, 'updateMoodDis'):
            self.view.updateMoodDis(self.model.mood)
        if hasattr(self.view, 'setImageForState'):
            self.view.setImageForState(self.model.mood, self.model.energy, self.model.hunger)

    def save_and_quit(self):
        # persist state and close the UI if available
        try:
            self.model.save_to_file()
        except Exception:
            pass
        try:
            if hasattr(self.view, 'root'):
                self.view.root.destroy()
        except Exception:
            pass
        