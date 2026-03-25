import pygame
import random
import math

pygame.init()

# Window setup
WIDTH, HEIGHT = 1024, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Bit GeoGuessr")

# Load map
map_img = pygame.image.load("assets/map.png")
map_img = pygame.transform.scale(map_img, (WIDTH, HEIGHT))

# Font
font = pygame.font.SysFont(None, 28)

# City data (scaled for 1536x1024 → 1024x512)
locations = [
    {"city": "Paris", "hint": "Eiffel Tower", "pos": (439, 172)},
    {"city": "New York", "hint": "Statue of Liberty", "pos": (252, 183)},
    {"city": "Tokyo", "hint": "Shibuya Crossing", "pos": (807, 192)},
    {"city": "Cairo", "hint": "Pyramids", "pos": (520, 228)},
    {"city": "Sydney", "hint": "Opera House", "pos": (745, 312)},
    {"city": "Rio de Janeiro", "hint": "Christ the Redeemer", "pos": (330, 309)},
    {"city": "London", "hint": "Big Ben", "pos": (428, 159)},
    {"city": "Moscow", "hint": "Red Square", "pos": (556, 146)},
    {"city": "Beijing", "hint": "Forbidden City", "pos": (714, 201)},
    {"city": "Toronto", "hint": "CN Tower", "pos": (223, 177)},
]

# Pin drawing
def draw_pin(screen, pos, color):
    x, y = pos
    pygame.draw.circle(screen, (0, 0, 0), (x, y), 10)
    pygame.draw.circle(screen, color, (x, y), 7)
    pygame.draw.line(screen, (0, 0, 0), (x, y + 7), (x, y + 20), 3)

# Debug text
def draw_debug_text(screen, click_pos, correct_pos):
    cx, cy = click_pos
    tx, ty = correct_pos

    text1 = font.render(f"Clicked: ({cx}, {cy})", True, (255, 255, 255))
    text2 = font.render(f"Correct: ({tx}, {ty})", True, (0, 255, 0))

    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))

# Distance function
def pixel_distance(a, b):
    return int(math.dist(a, b))

# Game state
score = 0
streak = 0
guess_pos = None
correct_city = random.choice(locations)
correct_pos = correct_city["pos"]
last_correct_pos = None        # ⭐ ADDED
message = ""

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle click
        if event.type == pygame.MOUSEBUTTONDOWN:
            guess_pos = pygame.mouse.get_pos()

            last_correct_pos = correct_pos   # ⭐ ADDED — save old city BEFORE switching

            # Calculate distance using the OLD correct city
            dist = pixel_distance(guess_pos, last_correct_pos)   # ⭐ CHANGED

            # Scoring logic
            gained = max(0, 200 - dist)
            score += gained

            if dist < 50:
                streak += 1
            else:
                streak = 0

            message = f"Nice! {correct_city['city']} (+{gained})"

            # Pick next city
            correct_city = random.choice(locations)
            correct_pos = correct_city["pos"]

    # Draw map
    screen.blit(map_img, (0, 0))

    # Draw pins + debug
    if guess_pos is not None:
        draw_pin(screen, guess_pos, (255, 0, 0))      # Red = guess

        if last_correct_pos is not None:              # ⭐ CHANGED
            draw_pin(screen, last_correct_pos, (0, 255, 0))  # Green = previous correct city
            draw_debug_text(screen, guess_pos, last_correct_pos)

    # UI text
    hint_text = font.render(f"Hint: {correct_city['hint']}", True, (0, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    streak_text = font.render(f"Streak: {streak}", True, (0, 0, 0))
    msg_text = font.render(message, True, (0, 0, 0))

    screen.blit(hint_text, (10, HEIGHT - 100))
    screen.blit(score_text, (10, HEIGHT - 70))
    screen.blit(streak_text, (10, HEIGHT - 40))
    screen.blit(msg_text, (10, HEIGHT - 130))

    pygame.display.update()

pygame.quit()
