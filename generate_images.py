"""Generate realistic food images for the menu using Pillow."""
from PIL import Image, ImageDraw, ImageFilter
import random
import math
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)
W, H = 600, 400


def rand_offset(base, variance):
    return base + random.randint(-variance, variance)


def draw_ellipse_aa(draw, bbox, fill):
    """Draw an anti-aliased ellipse by drawing on a larger canvas and downscaling."""
    draw.ellipse(bbox, fill=fill)


# ── Burger ──
def generate_burger():
    img = Image.new("RGB", (W, H), (35, 30, 28))
    draw = ImageDraw.Draw(img)

    cx, cy = W // 2, H // 2 + 10

    # Plate / surface glow
    for r in range(180, 0, -2):
        alpha = int(25 * (r / 180))
        c = (55 + alpha, 45 + alpha, 38 + alpha)
        draw.ellipse([cx - r, cy + 40 - r // 3, cx + r, cy + 40 + r // 3], fill=c)

    # Shadow under burger
    draw.ellipse([cx - 120, cy + 50, cx + 120, cy + 80], fill=(25, 20, 18))

    # Bottom bun
    draw.ellipse([cx - 110, cy + 10, cx + 110, cy + 60], fill=(195, 130, 50))
    draw.rectangle([cx - 110, cy + 20, cx + 110, cy + 45], fill=(195, 130, 50))
    # Bun texture
    for i in range(20):
        x = random.randint(cx - 100, cx + 100)
        y = random.randint(cy + 15, cy + 40)
        draw.ellipse([x - 2, y - 1, x + 2, y + 1], fill=(180, 120, 45))

    # Lettuce layer
    for i in range(30):
        x = cx - 105 + i * 7
        y_base = cy + 10
        for j in range(3):
            ox = random.randint(-5, 5)
            oy = random.randint(-4, 4)
            draw.ellipse([x + ox - 12, y_base + oy - 5, x + ox + 12, y_base + oy + 5],
                         fill=(random.randint(60, 100), random.randint(160, 200), random.randint(40, 70)))

    # Tomato slices
    for i in range(4):
        tx = cx - 70 + i * 45
        draw.ellipse([tx - 20, cy - 5, tx + 20, cy + 10], fill=(200, 45, 35))
        draw.ellipse([tx - 14, cy - 1, tx + 14, cy + 6], fill=(220, 60, 45))

    # Cheese (melting over sides)
    cheese_points = []
    for i in range(25):
        x = cx - 115 + i * 9.5
        y = cy - 15 + math.sin(i * 0.8) * 5
        cheese_points.append((x, y))
    for i in range(24, -1, -1):
        x = cx - 115 + i * 9.5
        drip = 15 + (8 if i % 4 == 0 else 0)
        cheese_points.append((x, cy - 15 + drip))
    draw.polygon(cheese_points, fill=(255, 200, 50))
    # Cheese highlight
    for i in range(12):
        x = cx - 100 + i * 18
        draw.ellipse([x - 4, cy - 14, x + 4, cy - 8], fill=(255, 220, 90))

    # Patty
    draw.ellipse([cx - 105, cy - 30, cx + 105, cy - 5], fill=(90, 50, 30))
    draw.ellipse([cx - 100, cy - 28, cx + 100, cy - 10], fill=(110, 65, 35))
    # Grill marks
    for i in range(5):
        x = cx - 70 + i * 35
        draw.line([x, cy - 26, x + 25, cy - 12], fill=(70, 38, 20), width=3)

    # Top bun
    draw.ellipse([cx - 110, cy - 80, cx + 110, cy - 15], fill=(210, 145, 55))
    # Bun highlight (glossy)
    draw.ellipse([cx - 70, cy - 75, cx + 30, cy - 45], fill=(230, 170, 75))
    draw.ellipse([cx - 40, cy - 70, cx + 10, cy - 52], fill=(240, 185, 90))
    # Sesame seeds
    for _ in range(18):
        sx = random.randint(cx - 80, cx + 80)
        sy = random.randint(cy - 72, cy - 35)
        angle = random.randint(0, 180)
        draw.ellipse([sx - 4, sy - 2, sx + 4, sy + 2], fill=(245, 235, 200))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    img.save(os.path.join(OUTPUT_DIR, "burger.jpg"), quality=92)


# ── Pizza ──
def generate_pizza():
    img = Image.new("RGB", (W, H), (40, 28, 22))
    draw = ImageDraw.Draw(img)

    cx, cy = W // 2, H // 2 + 15

    # Wooden surface texture
    for y in range(H):
        r = 55 + int(10 * math.sin(y * 0.05))
        g = 38 + int(8 * math.sin(y * 0.05))
        b = 25 + int(5 * math.sin(y * 0.05))
        draw.line([0, y, W, y], fill=(r, g, b))

    # Shadow
    draw.ellipse([cx - 165, cy - 105, cx + 165, cy + 135], fill=(30, 18, 12))

    # Pizza base - full circle
    draw.ellipse([cx - 155, cy - 110, cx + 155, cy + 120], fill=(210, 170, 90))
    # Crust ring
    draw.ellipse([cx - 145, cy - 100, cx + 145, cy + 110], fill=(200, 140, 55))
    # Crust highlights
    for i in range(40):
        angle = i * 9 * math.pi / 180
        r_crust = 148
        bx = cx + int(r_crust * math.cos(angle))
        by = cy + 5 + int((r_crust - 5) * math.sin(angle))
        draw.ellipse([bx - 6, by - 6, bx + 6, by + 6],
                     fill=(random.randint(190, 220), random.randint(140, 170), random.randint(60, 90)))

    # Sauce
    draw.ellipse([cx - 130, cy - 85, cx + 130, cy + 95], fill=(180, 50, 30))
    # Sauce variation
    for _ in range(60):
        sx = random.randint(cx - 120, cx + 120)
        sy = random.randint(cy - 75, cy + 85)
        dist = math.sqrt((sx - cx) ** 2 + ((sy - cy - 5) * 1.1) ** 2)
        if dist < 120:
            draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5],
                         fill=(random.randint(160, 195), random.randint(40, 65), random.randint(20, 40)))

    # Cheese base
    for _ in range(200):
        sx = random.randint(cx - 125, cx + 125)
        sy = random.randint(cy - 80, cy + 90)
        dist = math.sqrt((sx - cx) ** 2 + ((sy - cy - 5) * 1.1) ** 2)
        if dist < 118:
            sz = random.randint(4, 12)
            draw.ellipse([sx - sz, sy - sz // 2, sx + sz, sy + sz // 2],
                         fill=(random.randint(240, 255), random.randint(200, 230), random.randint(80, 130)))

    # Pepperoni
    pepperoni_positions = []
    for _ in range(14):
        for attempt in range(20):
            px = random.randint(cx - 110, cx + 110)
            py = random.randint(cy - 70, cy + 80)
            dist = math.sqrt((px - cx) ** 2 + ((py - cy - 5) * 1.1) ** 2)
            too_close = any(math.sqrt((px - ex) ** 2 + (py - ey) ** 2) < 40 for ex, ey in pepperoni_positions)
            if dist < 110 and not too_close:
                pepperoni_positions.append((px, py))
                break

    for px, py in pepperoni_positions:
        r = random.randint(15, 19)
        draw.ellipse([px - r, py - r, px + r, py + r], fill=(160, 30, 20))
        draw.ellipse([px - r + 2, py - r + 2, px + r - 2, py + r - 2], fill=(175, 40, 28))
        # Pepperoni oil spots
        for _ in range(3):
            ox = px + random.randint(-6, 6)
            oy = py + random.randint(-6, 6)
            draw.ellipse([ox - 2, oy - 2, ox + 2, oy + 2], fill=(190, 55, 35))

    # Basil leaves
    for _ in range(5):
        bx = random.randint(cx - 90, cx + 90)
        by = random.randint(cy - 60, cy + 70)
        dist = math.sqrt((bx - cx) ** 2 + ((by - cy) * 1.1) ** 2)
        if dist < 105:
            # Simple leaf shape
            leaf_color = (random.randint(40, 70), random.randint(130, 170), random.randint(30, 55))
            draw.ellipse([bx - 8, by - 4, bx + 8, by + 4], fill=leaf_color)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    img.save(os.path.join(OUTPUT_DIR, "pizza.jpg"), quality=92)


# ── Tacos ──
def generate_tacos():
    img = Image.new("RGB", (W, H), (45, 40, 35))
    draw = ImageDraw.Draw(img)

    # Dark slate/wood surface
    for y in range(H):
        v = 42 + int(5 * math.sin(y * 0.03))
        draw.line([0, y, W, y], fill=(v, v - 5, v - 8))

    # Draw 3 tacos
    taco_positions = [(W // 2 - 150, H // 2 + 5), (W // 2, H // 2 - 10), (W // 2 + 150, H // 2 + 5)]

    for idx, (tx, ty) in enumerate(taco_positions):
        # Shadow
        draw.ellipse([tx - 75, ty + 25, tx + 75, ty + 55], fill=(30, 25, 20))

        # Tortilla (taco shell shape - U shape)
        # Left side
        for i in range(50):
            angle = math.pi * 0.15 + (math.pi * 0.7) * i / 50
            r = 65
            x1 = tx + int(r * math.cos(angle))
            y1 = ty + int(r * 0.7 * math.sin(angle))
            x2 = tx + int((r - 12) * math.cos(angle))
            y2 = ty + int((r - 12) * 0.7 * math.sin(angle))
            color = (random.randint(210, 230), random.randint(180, 200), random.randint(110, 140))
            draw.line([x1, y1, x2, y2], fill=color, width=4)

        # Fill interior
        draw.ellipse([tx - 50, ty - 20, tx + 50, ty + 40], fill=(220, 190, 120))

        # Meat filling
        for _ in range(25):
            mx = tx + random.randint(-40, 40)
            my = ty + random.randint(-15, 20)
            dist = math.sqrt((mx - tx) ** 2 + ((my - ty - 5) * 1.5) ** 2)
            if dist < 42:
                sz = random.randint(3, 8)
                draw.ellipse([mx - sz, my - sz, mx + sz, my + sz],
                             fill=(random.randint(140, 180), random.randint(80, 110), random.randint(50, 70)))

        # Lettuce
        for _ in range(12):
            lx = tx + random.randint(-35, 35)
            ly = ty + random.randint(-20, 0)
            draw.ellipse([lx - 6, ly - 3, lx + 6, ly + 3],
                         fill=(random.randint(80, 120), random.randint(180, 220), random.randint(50, 80)))

        # Tomato bits
        for _ in range(6):
            rx = tx + random.randint(-30, 30)
            ry = ty + random.randint(-18, 5)
            draw.ellipse([rx - 4, ry - 4, rx + 4, ry + 4],
                         fill=(random.randint(200, 230), random.randint(50, 70), random.randint(30, 50)))

        # Cheese shreds
        for _ in range(8):
            sx = tx + random.randint(-30, 30)
            sy = ty + random.randint(-15, 15)
            draw.line([sx, sy, sx + random.randint(-10, 10), sy + random.randint(5, 15)],
                      fill=(255, random.randint(210, 240), random.randint(80, 120)), width=2)

        # Lime-colored garnish on top
        for _ in range(4):
            gx = tx + random.randint(-20, 20)
            gy = ty + random.randint(-25, -10)
            draw.ellipse([gx - 3, gy - 3, gx + 3, gy + 3],
                         fill=(random.randint(100, 150), random.randint(200, 240), random.randint(60, 100)))

    # Lime wedge on the side
    lx, ly = W // 2 + 220, H // 2 + 50
    draw.pieslice([lx - 25, ly - 25, lx + 25, ly + 25], 200, 340, fill=(140, 200, 60))
    draw.pieslice([lx - 20, ly - 20, lx + 20, ly + 20], 205, 335, fill=(170, 220, 80))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    img.save(os.path.join(OUTPUT_DIR, "tacos.jpg"), quality=92)


# ── Chicken Wings ──
def generate_wings():
    img = Image.new("RGB", (W, H), (35, 30, 28))
    draw = ImageDraw.Draw(img)

    cx, cy = W // 2, H // 2 + 10

    # Dark surface
    for y in range(H):
        v = 32 + int(4 * math.sin(y * 0.04))
        draw.line([0, y, W, y], fill=(v + 5, v, v - 3))

    # Plate
    draw.ellipse([cx - 170, cy - 90, cx + 170, cy + 110], fill=(50, 48, 45))
    draw.ellipse([cx - 165, cy - 87, cx + 165, cy + 107], fill=(65, 62, 58))
    draw.ellipse([cx - 150, cy - 78, cx + 150, cy + 95], fill=(55, 52, 48))

    # Generate wing positions
    wing_positions = []
    for _ in range(9):
        for attempt in range(30):
            wx = cx + random.randint(-110, 110)
            wy = cy + random.randint(-50, 60)
            dist = math.sqrt(((wx - cx) / 140) ** 2 + ((wy - cy - 5) / 80) ** 2)
            too_close = any(math.sqrt((wx - ex) ** 2 + (wy - ey) ** 2) < 45 for ex, ey in wing_positions)
            if dist < 0.85 and not too_close:
                wing_positions.append((wx, wy))
                break

    for wx, wy in wing_positions:
        angle = random.randint(0, 360)
        # Wing shape (elongated ellipse rotated)
        wing_w = random.randint(28, 38)
        wing_h = random.randint(16, 22)

        # Base color (golden/orange glazed)
        base_r = random.randint(180, 210)
        base_g = random.randint(90, 120)
        base_b = random.randint(30, 50)

        # Draw wing body
        draw.ellipse([wx - wing_w, wy - wing_h, wx + wing_w, wy + wing_h],
                     fill=(base_r, base_g, base_b))
        # Glaze highlights
        draw.ellipse([wx - wing_w + 5, wy - wing_h + 3, wx + wing_w - 8, wy + wing_h - 5],
                     fill=(base_r + 20, base_g + 15, base_b + 5))
        # Crispy texture spots
        for _ in range(6):
            sx = wx + random.randint(-wing_w + 5, wing_w - 5)
            sy = wy + random.randint(-wing_h + 3, wing_h - 3)
            draw.ellipse([sx - 3, sy - 2, sx + 3, sy + 2],
                         fill=(base_r - 30, base_g - 20, base_b - 10))
        # Sauce glaze
        for _ in range(4):
            sx = wx + random.randint(-wing_w + 8, wing_w - 8)
            sy = wy + random.randint(-wing_h + 4, wing_h - 4)
            draw.ellipse([sx - 4, sy - 3, sx + 4, sy + 3],
                         fill=(random.randint(160, 190), random.randint(40, 60), random.randint(20, 35)))

    # Dipping sauce bowl
    sx, sy = cx + 120, cy + 55
    draw.ellipse([sx - 30, sy - 18, sx + 30, sy + 18], fill=(60, 58, 55))
    draw.ellipse([sx - 25, sy - 14, sx + 25, sy + 14], fill=(220, 210, 190))
    draw.ellipse([sx - 22, sy - 11, sx + 22, sy + 11], fill=(200, 195, 180))

    # Celery sticks
    for i in range(3):
        cx_s = cx - 130 + i * 15
        draw.line([cx_s, cy - 60, cx_s + 25, cy + 40], fill=(120, 180, 70), width=6)
        draw.line([cx_s + 1, cy - 58, cx_s + 26, cy + 38], fill=(140, 200, 85), width=3)

    # Scatter some sesame/seasoning
    for _ in range(30):
        sx = cx + random.randint(-130, 130)
        sy = cy + random.randint(-70, 80)
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(240, 230, 200))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    img.save(os.path.join(OUTPUT_DIR, "wings.jpg"), quality=92)


if __name__ == "__main__":
    random.seed(42)
    generate_burger()
    print("Generated burger.jpg")
    random.seed(77)
    generate_pizza()
    print("Generated pizza.jpg")
    random.seed(13)
    generate_tacos()
    print("Generated tacos.jpg")
    random.seed(99)
    generate_wings()
    print("Generated wings.jpg")
    print("All images generated in", OUTPUT_DIR)
