import tkinter as tk

class Dino:
    def __init__(self, canvas, x, y, scale=1.0):
        self.canvas = canvas
        self.scale = scale
        self.tag = "dino"
        s = scale
        # Body
        self.body = canvas.create_oval(x, y, x+140*s, y+60*s, fill="#6bbf59", outline="", tags=self.tag)
        # Head
        self.head = canvas.create_oval(x+110*s, y-30*s, x+170*s, y+20*s, fill="#6bbf59", outline="", tags=self.tag)
        # Eye
        self.eye = canvas.create_oval(x+140*s, y-10*s, x+148*s, y-2*s, fill="white", outline="", tags=self.tag)
        self.pupil = canvas.create_oval(x+144*s, y-7*s, x+147*s, y-4*s, fill="black", tags=self.tag)
        self.eye2 = canvas.create_oval(x+155*s, y-10*s, x+163*s, y-2*s, fill="white", outline="", tags=self.tag)
        self.pupil2 = canvas.create_oval(x+159*s, y-7*s, x+162*s, y-4*s, fill="black", tags=self.tag)
        # Tail (a polygon)
        self.tail = canvas.create_polygon(
            x+10*s, y+30*s,
            x-30*s, y+10*s,
            x+10*s, y+50*s,
            fill="#5ea84b", outline="", tags=self.tag
        )
        # Legs
        self.leg1 = canvas.create_rectangle(x+30*s, y+60*s, x+50*s, y+90*s, fill="#4f8f3a", outline="", tags=self.tag)
        self.leg2 = canvas.create_rectangle(x+80*s, y+60*s, x+100*s, y+90*s, fill="#4f8f3a", outline="", tags=self.tag)
        # Smile
        self.smile = canvas.create_arc(x+125*s, y-10*s, x+155*s, y+10*s, start=200, extent=140, style="arc", width=2, tags=self.tag)
        # Animation state
        self.leg_dir = 1
        self.tail_dir = 1
        self.leg_offset = 0
        self.tail_offset = 0

    def step(self):
        # Move whole dino to the right slowly
        dx = 2
        self.canvas.move(self.tag, dx, 0)

        # Animate legs: small up/down motion
        max_leg = 6
        step_leg = 1 * self.leg_dir
        self.canvas.move(self.leg1, 0, step_leg)
        self.canvas.move(self.leg2, 0, -step_leg)
        self.leg_offset += step_leg
        if abs(self.leg_offset) >= max_leg:
            self.leg_dir *= -1

        # Animate tail: wiggle by small rotation-ish movement
        tail_dx = 1 * self.tail_dir
        self.canvas.move(self.tail, tail_dx, 0)
        self.tail_offset += tail_dx
        if abs(self.tail_offset) >= 8:
            self.tail_dir *= -1

def main():
    root = tk.Tk()
    root.title("Friendly Dinosaur Animation")
    WIDTH, HEIGHT = 800, 240
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#eaf7ff")
    canvas.pack()

    # Ground
    canvas.create_rectangle(0, HEIGHT-40, WIDTH, HEIGHT, fill="#cfe7b4", outline="")

    dino = Dino(canvas, x= -160, y=HEIGHT-120, scale=1.0)

    def animate():
        dino.step()
        # If dino moved off right edge, teleport back to left
        bbox = canvas.bbox(dino.tag)
        if bbox and bbox[0] > WIDTH + 40:
            # move to left off-screen
            canvas.move(dino.tag, - (bbox[0] + 200), 0)
        root.after(50, animate)

    animate()
    root.mainloop()

if __name__ == "__main__":
    main()