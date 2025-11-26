import tkinter as tk
import math
import random

def main():
    root = tk.Tk()
    root.title("Milky Way Galaxy Animation")
    WIDTH, HEIGHT = 1000, 700
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#000814")
    canvas.pack()
    
    # Title
    canvas.create_text(WIDTH/2, 30, text="The Milky Way Galaxy", font=("Arial", 28, "bold"), fill="#00d9ff")
    
    # Create stars in galaxy
    stars = []
    galaxy_center_x, galaxy_center_y = WIDTH/2, HEIGHT/2
    
    # Inner bright stars (disk)
    for _ in range(400):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(20, 200)
        x = galaxy_center_x + distance * math.cos(angle)
        y = galaxy_center_y + distance * math.sin(angle)
        brightness = random.randint(100, 255)
        size = random.randint(1, 3)
        color = f"#{brightness:02x}{brightness:02x}ff"
        stars.append({"x": x, "y": y, "angle": angle, "distance": distance, "size": size, "color": color, "id": None})
    
    # Outer halo stars (fewer, dimmer)
    for _ in range(150):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(200, 300)
        x = galaxy_center_x + distance * math.cos(angle)
        y = galaxy_center_y + distance * math.sin(angle)
        brightness = random.randint(40, 120)
        size = 1
        color = f"#{brightness:02x}{brightness//2:02x}{brightness:02x}"
        stars.append({"x": x, "y": y, "angle": angle, "distance": distance, "size": size, "color": color, "id": None})
    
    # Background distant stars
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        brightness = random.randint(30, 80)
        color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
        canvas.create_oval(x, y, x+1, y+1, fill=color, outline="")
    
    rotation_angle = 0

    # Sun (center) setup: multiple concentric ovals to simulate glow + pulsing
    sun_layers = []
    # base radii from outer glow to core
    sun_base_radii = [90, 60, 40, 26]  
    sun_colors = ["#2b1300", "#ff9f1c", "#ff7a00", "#fff1a6"]  # outer darker -> inner bright
    for r, c in zip(sun_base_radii, sun_colors):
        oid = canvas.create_oval(
            galaxy_center_x - r, galaxy_center_y - r,
            galaxy_center_x + r, galaxy_center_y + r,
            fill=c, outline=""
        )
        sun_layers.append(oid)
    pulse_phase = 0.0

    def draw_stars():
        for star in stars:
            if star["id"]:
                canvas.delete(star["id"])
            star["id"] = canvas.create_oval(
                star["x"] - star["size"], star["y"] - star["size"],
                star["x"] + star["size"], star["y"] + star["size"],
                fill=star["color"], outline=""
            )
    
    def update_sun():
        nonlocal pulse_phase
        # pulse between ~0.92 and ~1.08
        pulse = 1.0 + 0.06 * math.sin(pulse_phase)
        pulse_phase += 0.12
        for oid, base_r in zip(sun_layers, sun_base_radii):
            r = base_r * pulse
            canvas.coords(oid,
                galaxy_center_x - r, galaxy_center_y - r,
                galaxy_center_x + r, galaxy_center_y + r
            )
    
    def animate():
        nonlocal rotation_angle
        rotation_angle += 0.003
        
        # Rotate stars around galaxy center
        for star in stars:
            new_angle = star["angle"] + rotation_angle
            star["x"] = galaxy_center_x + star["distance"] * math.cos(new_angle)
            star["y"] = galaxy_center_y + star["distance"] * math.sin(new_angle)
        
        draw_stars()
        update_sun()  # keep sun drawn on top of stars
        root.after(50, animate)
    
    draw_stars()
    update_sun()
    animate()
    
    # Add some info text
    canvas.create_text(WIDTH/2, HEIGHT-20, text="A spiral galaxy with ~200-400 billion stars", 
                       font=("Arial", 10), fill="#888888")
    
    root.mainloop()

if __name__ == "__main__":
    main()