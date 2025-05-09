import pygame
import requests
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FBI Wanted Search")
clock = pygame.time.Clock()

# Font and colors
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
TEXT_COLOR = pygame.Color('white')
BG_COLOR = pygame.Color('black')

# Input box
input_box = pygame.Rect(50, 50, 500, 32)
active = False
user_text = ''
last_search = ''
copied_message = ''
copied_timer = 0

# Button
button_box = pygame.Rect(570, 50, 100, 32)
button_label = font.render("Search", True, TEXT_COLOR)

# Example warning messages
def examples():
    return [
        "SHOULD BE CONSIDERED ARMED AND DANGEROUS",
        "WANTED FOR MURDER",
        "FUGITIVE FROM JUSTICE"
    ]

# Results storage
results = []  # list of (title_surface, url_surface, y_position, url_rect)
scroll_y = 0

# Simple search: only warning_message
def do_search(text):
    try:
        r = requests.get('https://api.fbi.gov/wanted/v1/list', params={'warning_message': text})
        data = r.json()
        items = data.get('items', [])[:5]  # Only display the first 5 results
        surfaces = []
        y = 300  # Moved down to avoid overlap with examples
        for item in items:
            url = item.get('url', '')
            title = item.get('title', 'No Title')
            title_surf = font.render(f"{title}", True, TEXT_COLOR)
            url_surf = small_font.render(f"{url}", True, TEXT_COLOR)
            url_rect = url_surf.get_rect(topleft=(50, y + title_surf.get_height()))
            surfaces.append((title_surf, url_surf, y, url, url_rect))
            y += title_surf.get_height() + url_surf.get_height() + 20
        return surfaces
    except:
        err = font.render("Error fetching data", True, TEXT_COLOR)
        return [(err, None, 300, '', None)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
            if button_box.collidepoint(event.pos) and user_text != last_search:
                results = do_search(user_text)
                last_search = user_text
                scroll_y = 0
            for _, _, y_pos, url, url_rect in results:
                if url_rect and url_rect.collidepoint(event.pos[0], event.pos[1] - scroll_y):
                    copied_message = f"Copied to clipboard (not really): {url}"
                    copied_timer = pygame.time.get_ticks()
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN and user_text != last_search:
                    results = do_search(user_text)
                    last_search = user_text
                    scroll_y = 0
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
            # Scrolling
            if event.key == pygame.K_DOWN:
                scroll_y -= 20
            elif event.key == pygame.K_UP:
                scroll_y += 20

    # Draw
    screen.fill(BG_COLOR)
    # input box
    color = COLOR_ACTIVE if active else COLOR_INACTIVE
    pygame.draw.rect(screen, color, input_box, 2)
    txt = user_text or 'Type warning_message...'
    screen.blit(font.render(txt, True, TEXT_COLOR), (input_box.x+5, input_box.y+5))
    # examples
    y0 = input_box.y + 50
    screen.blit(font.render('Examples:', True, TEXT_COLOR), (input_box.x, y0))
    y = y0 + 30
    for ex in examples():
        screen.blit(font.render(ex, True, TEXT_COLOR), (input_box.x+10, y))
        y += 30
    # button
    pygame.draw.rect(screen, COLOR_INACTIVE, button_box)
    screen.blit(button_label, (button_box.x+10, button_box.y+5))
    # results with scrolling (drawn lower to avoid overlap)
    for title_surf, url_surf, y_pos, _, url_rect in results:
        screen.blit(title_surf, (50, y_pos + scroll_y))
        screen.blit(url_surf, (50, y_pos + scroll_y + title_surf.get_height()))

    # show fake copied message
    if copied_message and pygame.time.get_ticks() - copied_timer < 3000:
        msg = small_font.render(copied_message, True, TEXT_COLOR)
        screen.blit(msg, (50, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(30)