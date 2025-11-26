import tkinter as tk
from tkinter import font
import random

def main():
    root = tk.Tk()
    root.title("Happy Birthday Mom! 🎉")
    WIDTH, HEIGHT = 800, 600
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#ffe6f0")
    canvas.pack()
    
    # Title
    title_font = font.Font(family="Arial", size=40, weight="bold")
    canvas.create_text(WIDTH/2, 50, text="Happy Birthday Mom!", font=title_font, fill="#ff1493")
    
    # Cake
    cake_x, cake_y = WIDTH/2, HEIGHT/2 + 80
    # Cake layers
    canvas.create_rectangle(cake_x-80, cake_y, cake_x+80, cake_y+40, fill="#d4691c", outline="")
    canvas.create_rectangle(cake_x-70, cake_y-40, cake_x+70, cake_y, fill="#e8a76f", outline="")
    canvas.create_rectangle(cake_x-60, cake_y-80, cake_x+60, cake_y-40, fill="#d4691c", outline="")
    
    # Candles
    candle_positions = [cake_x-40, cake_x-20, cake_x, cake_x+20, cake_x+40]
    candles = []
    for cx in candle_positions:
        candles.append(canvas.create_rectangle(cx-2, cake_y-100, cx+2, cake_y-70, fill="#fff8dc"))
    
    # Flames (animated)
    flames = []
    flame_colors = ["#ff6347", "#ffa500", "#ffff00"]
    
    def animate_flames():
        for i, cx in enumerate(candle_positions):
            if i < len(flames):
                canvas.delete(flames[i])
            color = random.choice(flame_colors)
            offset = random.randint(-3, 3)
            flame = canvas.create_polygon(
                cx + offset, cake_y - 105,
                cx - 5 + offset, cake_y - 90,
                cx + 5 + offset, cake_y - 90,
                fill=color
            )
            flames.append(flame)
        root.after(200, animate_flames)
    
    animate_flames()
    
    # Balloons
    balloon_data = []
    colors = ["#ff1493", "#00bfff", "#ffff00", "#00ff00", "#ff69b4"]
    for i in range(5):
        x = random.randint(50, WIDTH-50)
        y = HEIGHT + 50
        color = colors[i % len(colors)]
        balloon_data.append({"x": x, "y": y, "color": color, "id": None})
    
    def draw_balloons():
        for b in balloon_data:
            if b["id"]:
                canvas.delete(b["id"])
            b["id"] = canvas.create_oval(
                b["x"]-15, b["y"]-20, b["x"]+15, b["y"]+20,
                fill=b["color"], outline=""
            )
            # String
            canvas.create_line(b["x"], b["y"]+20, b["x"], b["y"]+50, fill="gray")
    
    def animate_balloons():
        for b in balloon_data:
            b["y"] -= 2
            if b["y"] < -50:
                b["y"] = HEIGHT + 50
        draw_balloons()
        root.after(50, animate_balloons)
    
    draw_balloons()
    animate_balloons()
    
    # Confetti
    confetti_pieces = []
    for _ in range(30):
        confetti_pieces.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(-50, HEIGHT),
            "dx": random.uniform(-2, 2),
            "dy": random.uniform(1, 3),
            "id": None
        })
    
    def animate_confetti():
        for c in confetti_pieces:
            if c["id"]:
                canvas.delete(c["id"])
            c["x"] += c["dx"]
            c["y"] += c["dy"]
            if c["y"] > HEIGHT:
                c["y"] = -10
                c["x"] = random.randint(0, WIDTH)
            color = random.choice(["#ff1493", "#00bfff", "#ffff00", "#00ff00", "#ff69b4"])
            c["id"] = canvas.create_rectangle(c["x"], c["y"], c["x"]+5, c["y"]+5, fill=color, outline="")
        root.after(50, animate_confetti)
    
    animate_confetti()
    
    # Message at bottom
    msg_font = font.Font(family="Arial", size=16, slant="italic")
    canvas.create_text(WIDTH/2, HEIGHT-30, text="Wishing you a wonderful day! 💝", font=msg_font, fill="#ff1493")
    
    root.mainloop()

if __name__ == "__main__":
    main()