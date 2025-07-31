from pygame import *
import json
import os
import sys


def run_menu():
    window_size = 600, 400
    window = display.set_mode(window_size)
    display.set_caption("Меню зі складністю")
    font.init()
    main_font = font.Font(None, 36)

    # --- JSON збереження ---
    filename = "settings.json"
    sound_on = True

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            sound_on = data.get("sound", True)
    else:
        with open(filename, 'w') as f:
            json.dump({'sound': True}, f)

    class Button:
        def __init__(self, x, y, width, height, color, text, text_color=(0, 0, 0)):
            self.rect = Rect(x, y, width, height)
            self.color = color
            self.text = text
            self.text_color = text_color
            self.font = font.Font(None, 28)

        def draw(self):
            draw.rect(window, self.color, self.rect)
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            window.blit(text_surf, text_rect)

        def is_clicked(self, event):
            return event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

    # --- Кнопки ---
    play_button = Button(200, 80, 200, 50, (200, 200, 200), "Грати")
    sound_button = Button(200, 160, 200, 50, (200, 200, 200), "Sound: On")
    exit_button = Button(200, 240, 200, 50, (200, 200, 200), "Вийти")

    def update_sound_button():
        text = f"Sound: {'On' if sound_on else 'Off'}"
        sound_button.text = text

    running = True
    while running:
        window.fill((255, 255, 255))

        play_button.draw()
        sound_button.draw()
        exit_button.draw()

        display.update()

        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            if play_button.is_clicked(e):
                with open(filename, 'w') as f:
                    json.dump({'sound': sound_on}, f)
                running = False
            if sound_button.is_clicked(e):
                sound_on = not sound_on
                update_sound_button()
            if exit_button.is_clicked(e):
                sys.exit()
run_menu()