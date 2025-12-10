from View import View
import tkinter as tk
from PetCanvas import PetCanvas


class PetView(View):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.root = tk.Tk()
        self.root.title("Virtual Pet")

        self.label = tk.Label(self.root, text="Welcome to Virtual Pet")
        self.label.pack()

        self.displayHunger = tk.Label(self.root, text="Hunger Level: --")
        self.displayHunger.pack()
        self.displayMood = tk.Label(self.root, text="Mood: --")
        self.displayMood.pack()
        self.displayEnergy = tk.Label(self.root, text="Energy Level: --")
        self.displayEnergy.pack()

        #canvas where the programmatic pet will be drawn
        self.canvas_width = 400
        self.canvas_height = 300
        self.pet_canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="#BFEFFF")
        self.pet_canvas.pack(pady=8)

        #instantiate the canvas-based pet
        self.pet = PetCanvas(self.pet_canvas, x=self.canvas_width // 2, y=self.canvas_height // 2, size=80)
        self.pet.draw()

        #status/message label
        self.statusLabel = tk.Label(self.root, text="Status: --", fg="blue")
        self.statusLabel.pack(pady=(6, 0))

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=8)

        self.playBtn = tk.Button(btn_frame, text="Play", command=self._on_play)
        self.playBtn.grid(row=0, column=0, padx=4)
        self.restBtn = tk.Button(btn_frame, text="Rest", command=self._on_rest)
        self.restBtn.grid(row=0, column=1, padx=4)
        self.feedBtn = tk.Button(btn_frame, text="Feed", command=self._on_feed)
        self.feedBtn.grid(row=0, column=2, padx=4)

    #controller hookup
    def setController(self, controller):
        self.controller = controller
        #register window close to persist state via controller
        try:
            self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        except Exception:
            pass

    def _on_close(self):
        try:
            if self.controller and hasattr(self.controller, 'save_and_quit'):
                self.controller.save_and_quit()
                return
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def start(self):
        self.root.mainloop()

    #button handlers
    def _on_play(self):
        if self.controller:
            self.controller.playBtnClicked()

    def _on_rest(self):
        if self.controller:
            self.controller.restBtnClicked()

    def _on_feed(self):
        if self.controller:
            self.controller.feedBtnClicked()

    #update UI (used by controller)
    def updateHungerDisplay(self, level):
        self.displayHunger.config(text=f"Hunger Level: {level}")

    def updateEnergyDisplay(self, level):
        self.displayEnergy.config(text=f"Energy Level: {level}")

    def updateMoodDis(self, mood):
        self.displayMood.config(text=f"Mood: {mood}")

    def updateStatus(self, message):
        #show short status messages in the GUI
        self.statusLabel.config(text=f"Status: {message}")
    #Pet/canvas integration
    def setImageForState(self, mood, energy, hunger):
        #Update the canvas pet to reflect the given state immediately
        try:
            self.pet.set_state(mood, energy, hunger)
        except Exception:
            pass

    def play_action(self, action_key, on_finished=None, frame_delay=None):
        #Map action keys to pet animations. Calls on_finished after the animation duration
        #choose animation and duration
        duration = 300
        try:
            if action_key == 'ActionPlay':
                self.pet.bounce(duration_ms=400)
                duration = 400
            elif action_key == 'ActionFeed':
                # wiggle + blink for feeding
                self.pet.wiggle(duration_ms=500)
                self.pet.blink()
                duration = 500
            elif action_key == 'ActionRest':
                #show blink and a small sleep
                self.pet.blink()
                duration = 300
            else:
                #unknown action: small blink
                self.pet.blink()
                duration = 200
        except Exception:
            duration = 200

        #schedule callback after duration
        if on_finished:
            try:
                self.root.after(duration, on_finished)
            except Exception:
                try:
                    on_finished()
                except Exception:
                    pass
    def setGifSize(self, width, height):
        #Compatibility: resize canvas and pet size.
        try:
            w = int(width)
            h = int(height)
            self.canvas_width = w
            self.canvas_height = h
            try:
                self.pet_canvas.config(width=w, height=h)
            except Exception:
                pass
            #reposition and resize pet to fit
            try:
                self.pet.x = w // 2
                self.pet.y = h // 2
                # scale pet size to smaller of dims
                self.pet.size = int(min(w, h) * 0.2)
                self.pet.draw()
            except Exception:
                pass
        except Exception:
            pass

    #implement abstract View methods
    def displayHunger(self, level):
        self.updateHungerDisplay(level)

    def displayMood(self, level):
        self.updateMoodDis(level)

    def displayImage(self):
        #return the canvas widget used for drawing
        return self.pet_canvas

    def displayEnergy(self, level):
        self.updateEnergyDisplay(level)

    def playBtnClicked(self):
        self._on_play()

    def restBtnClicked(self):
        self._on_rest()
