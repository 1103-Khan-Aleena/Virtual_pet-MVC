import tkinter as tk
import math
import os

class PetCanvas:
    def __init__(self, canvas, image_path="assets/egg.png", x=150, y=150, size=160):
        """
        canvas: tkinter.Canvas
        image_path: path to egg.png
        x, y: center coordinates
        size: target 'radius-ish' size used for scaling the image (bigger -> larger image)
        """
        self.canvas = canvas

        # base position (used so wiggle doesn't drift)
        self.base_x = x
        self.base_y = y

        # current center position (may be animated)
        self.x = x
        self.y = y
        self.size = size  # controls image scaling

        # state
        self.mood = "Neutral"  # Happy, Sad, Neutral, SuperTired
        self.energy = 100
        self.hunger = 50

        # animation state
        self.blink_state = False
        self.bounce_offset = 0

        # load image (keep reference to prevent GC)
        self.photo = self._load_image(image_path, self.size)
        self.image_id = None  # will hold canvas image id

    def _load_image(self, path, target_size):
        """Load image and return a PhotoImage (or ImageTk.PhotoImage)."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

        # Try to use Pillow for nicer resizing if available
        try:
            from PIL import Image, ImageTk
            img = Image.open(path).convert("RGBA")
            w, h = img.size
            # scale so the largest dimension matches (target_size*2)
            scale = (target_size * 2) / max(w, h)
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            img = img.resize((new_w, new_h), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            # fallback to tkinter PhotoImage (no resizing)
            try:
                return tk.PhotoImage(file=path)
            except Exception as e:
                raise RuntimeError("Failed to load image. Install Pillow for resizing support.") from e

    def draw(self):
        # clear previous pet group
        self.canvas.delete("pet")

        # compute current displayed center using bounce offset
        display_x = self.x
        display_y = self.y + self.bounce_offset

        # draw body image
        if self.photo:
            self.image_id = self.canvas.create_image(
                display_x, display_y, image=self.photo, tags="pet", anchor="center"
            )
            # get displayed image w/h for feature placement
            try:
                img_w = self.photo.width()
                img_h = self.photo.height()
            except Exception:
                img_w = self.size * 2
                img_h = self.size * 2
        else:
            # fallback: draw an oval if image missing
            radius = self.size
            self.canvas.create_oval(
                display_x - radius, display_y - radius,
                display_x + radius, display_y + radius,
                fill="#E9B6E4", outline="#060400", width=3, tags="pet"
            )
            img_w = self.size * 2
            img_h = self.size * 2

        # draw eyes and mouth on top of image (positions scale with img size)
        self._draw_eyes(display_x, display_y, img_w, img_h)
        self._draw_mouth(display_x, display_y, img_w, img_h)

        # mood indicators
        self._draw_mood_indicator(display_x, display_y, img_w, img_h)

    def _draw_eyes(self, cx, cy, img_w, img_h):
        # positions scale with image dimensions so facial features line up
        # these multipliers can be adjusted if your egg art is different
        eye_x_offset = int(img_w * 0.18)
        eye_y_offset = int(img_h * 0.22)
        eye_size = max(4, int(min(img_w, img_h) * 0.06))

        left_eye_x = cx - eye_x_offset
        right_eye_x = cx + eye_x_offset
        eye_y = cy - eye_y_offset

        if self.blink_state:
            # closed eyes (lines)
            self.canvas.create_line(
                left_eye_x - eye_size, eye_y,
                left_eye_x + eye_size, eye_y,
                width=2, fill="black", tags="pet"
            )
            self.canvas.create_line(
                right_eye_x - eye_size, eye_y,
                right_eye_x + eye_size, eye_y,
                width=2, fill="black", tags="pet"
            )
        else:
            pupil_offset_y = 0
            pupil_offset_x = 0
            if self.mood == "Happy":
                pupil_offset_y = -int(eye_size * 0.25)
            elif self.mood == "Sad":
                pupil_offset_y = int(eye_size * 0.25)

            # left eye
            self.canvas.create_oval(
                left_eye_x - eye_size, eye_y - eye_size,
                left_eye_x + eye_size, eye_y + eye_size,
                fill="white", outline="black", width=1, tags="pet"
            )
            self.canvas.create_oval(
                left_eye_x - max(2,int(eye_size*0.4)) + pupil_offset_x, eye_y + pupil_offset_y - max(2,int(eye_size*0.4)),
                left_eye_x + max(2,int(eye_size*0.4)) + pupil_offset_x, eye_y + pupil_offset_y + max(2,int(eye_size*0.4)),
                fill="black", tags="pet"
            )

            # right eye
            self.canvas.create_oval(
                right_eye_x - eye_size, eye_y - eye_size,
                right_eye_x + eye_size, eye_y + eye_size,
                fill="white", outline="black", width=1, tags="pet"
            )
            self.canvas.create_oval(
                right_eye_x - max(2,int(eye_size*0.4)) + pupil_offset_x, eye_y + pupil_offset_y - max(2,int(eye_size*0.4)),
                right_eye_x + max(2,int(eye_size*0.4)) + pupil_offset_x, eye_y + pupil_offset_y + max(2,int(eye_size*0.4)),
                fill="black", tags="pet"
            )

    def _draw_mouth(self, cx, cy, img_w, img_h):
        mouth_y = cy - 20
        mouth_width = int(img_w * 0.18)

        if self.mood == "Happy":
            self.canvas.create_arc(
                cx - mouth_width, mouth_y - int(mouth_width * 0.5),
                cx + mouth_width, mouth_y + int(mouth_width * 0.5),
                start=180, extent=180,
                fill="black", outline="black", width=2, tags="pet"
            )
        elif self.mood == "Sad":
            self.canvas.create_arc(
                cx - mouth_width, mouth_y - int(mouth_width * 0.5),
                cx + mouth_width, mouth_y + int(mouth_width * 0.5),
                start=0, extent=180,
                fill="black", outline="black", width=2, tags="pet"
            )
        else:
            self.canvas.create_line(
                cx - mouth_width, mouth_y,
                cx + mouth_width, mouth_y,
                width=2, fill="black", tags="pet"
            )

    def _draw_mood_indicator(self, cx, cy, img_w, img_h):
        # sleeping Z
        if self.energy <= 0:
            self._draw_z_indicator(cx, cy, img_w, img_h)
        elif self.hunger >= 100:
            self._draw_heart_indicator(cx, cy, img_w, img_h)
        elif self.hunger >= 80:
            self._draw_hungry_indicator(cx, cy, img_w, img_h)

    def _draw_z_indicator(self, cx, cy, img_w, img_h):
        z_x = cx + img_w * 0.6
        z_y = cy - img_h * 0.4
        self.canvas.create_line(z_x, z_y, z_x + 12, z_y, width=2, fill="gray", tags="pet")
        self.canvas.create_line(z_x + 12, z_y, z_x, z_y + 12, width=2, fill="gray", tags="pet")
        self.canvas.create_line(z_x, z_y + 12, z_x + 12, z_y + 12, width=2, fill="gray", tags="pet")

    def _draw_heart_indicator(self, cx, cy, img_w, img_h):
        hx = cx - img_w * 0.6
        hy = cy - img_h * 0.6
        hx = int(hx); hy = int(hy)
        self.canvas.create_oval(hx - 8, hy - 8, hx + 0, hy, fill="red", outline="red", tags="pet")
        self.canvas.create_oval(hx + 0, hy - 8, hx + 8, hy, fill="red", outline="red", tags="pet")
        self.canvas.create_polygon(hx - 4, hy, hx + 4, hy, hx, hy + 8, fill="red", outline="red", tags="pet")

    def _draw_hungry_indicator(self, cx, cy, img_w, img_h):
        bx = cx
        by = cy + int(img_h * 0.12)
        self.canvas.create_oval(bx - 15, by - 10, bx + 15, by + 10, outline="#FF6B6B", width=2, tags="pet")
        self.canvas.create_line(bx - 8, by - 5, bx + 8, by + 5, width=1, fill="#FF6B6B", tags="pet")

    # external API
    def set_state(self, mood=None, energy=None, hunger=None):
        if mood is not None:
            self.mood = mood
        if energy is not None:
            self.energy = energy
        if hunger is not None:
            self.hunger = hunger
        self.draw()

    def blink(self):
        self.blink_state = True
        self.draw()
        self.canvas.after(120, self._blink_off)

    def _blink_off(self):
        self.blink_state = False
        self.draw()

    def bounce(self, duration_ms=400):
        # reset offsets, animate bounce relative to base_y
        self.bounce_offset = 0
        self._animate_bounce(0, duration_ms)

    def _animate_bounce(self, elapsed, total_duration):
        if elapsed >= total_duration:
            self.bounce_offset = 0
            # restore base position
            self.x = self.base_x
            self.y = self.base_y
            self.draw()
            return

        progress = elapsed / total_duration
        # sine wave bounce (vertical)
        self.bounce_offset = int(math.sin(progress * math.pi) * (self.size * 0.2))  # scale bounce with size
        self.draw()
        self.canvas.after(16, lambda: self._animate_bounce(elapsed + 16, total_duration))

    def wiggle(self, duration_ms=500):
        # wiggle without permanently changing base position
        self._animate_wiggle(0, duration_ms)

    def _animate_wiggle(self, elapsed, total_duration):
        if elapsed >= total_duration:
            # restore original position at end
            self.x = self.base_x
            self.y = self.base_y
            self.draw()
            return

        progress = elapsed / total_duration
        # horizontal oscillation around base_x, scaled with size
        offset = int(math.sin(progress * math.pi * 4) * max(6, int(self.size * 0.05)))
        self.x = self.base_x + offset
        self.draw()
        self.canvas.after(16, lambda: self._animate_wiggle(elapsed + 16, total_duration))


# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Egg Pet")
    c = tk.Canvas(root, width=420, height=420, bg="white")
    c.pack()

    # Change size here to make the egg bigger/smaller:
    pet = PetCanvas(c, image_path="assets/egg.png", x=210, y=210, size=180)
    pet.draw()

    # Bind keys to test animations
    root.bind("<space>", lambda e: pet.blink())
    root.bind("b", lambda e: pet.bounce())
    root.bind("w", lambda e: pet.wiggle())
    root.bind("h", lambda e: pet.set_state(mood="Happy"))
    root.bind("s", lambda e: pet.set_state(mood="Sad"))
    root.bind("n", lambda e: pet.set_state(mood="Neutral"))

    tk.Label(root, text="space=blink, b=bounce, w=wiggle, h=happy, s=sad, n=neutral").pack(pady=6)
    root.mainloop()
