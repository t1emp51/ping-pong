from pygame import *
import socket
import json
from threading import Thread
from launcher_menu import run_menu

run_menu()

# ---ПУГАМЕ НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Пінг-Понг")
# ---СЕРВЕР ---
def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('localhost', 8080)) # ---- Підключення до сервера
            buffer = ""
            game_state = {}
            my_id = int(client.recv(24).decode())
            return my_id, game_state, buffer, client
        except:
            pass


def receive():
    global buffer, game_state, game_over
    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data
            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
        except:
            game_state["winner"] = -1
            break

# --- ШРИФТИ ---
font_win = font.Font(None, 72)
font_main = font.Font(None, 36)
# --- ЗОБРАЖЕННЯ ----
ball_image = image.load("images/ball1.png")
ball_image = transform.scale(ball_image, (30, 30))
background_image = image.load("images/background2.png")

paddle_left_img =  image.load("images/platform_left_png")
paddle_left_img =  transform.scale (paddle_left_img,(20,100))

paddle_right_img =  image.load("images/platform_right_png")
paddle_right_img =  transform.scale(paddle_right_img,(20,100))
# --- ЗВУКИ ---
mixer.init()
sound_wall_hit = mixer.Sound("sound/wall_hit.mp3")
sound_platform_hit = mixer.Sound("sound/platform_hit.mp3")
# ---Настраиваем громкость (от 0.0 до 1.0)---
sound_wall_hit.set_volume(0.1)
sound_platform_hit.set_volume(0.1)
# --- НАЛАШТУВАННЯ ---
sound_on = True
try:
    with open('settings.json', 'r') as f:
        data = json.load(f)
        sound_on = data.get("sound", True)
except:
    pass

# --- ГРА ---
game_over = False
winner = None
you_winner = None
my_id, game_state, buffer, client = connect_to_server()
Thread(target=receive, daemon=True).start()
while True:
    for e in event.get():
        if e.type == QUIT:
            exit()

    if "countdown" in game_state and game_state["countdown"] > 0:
        screen.fill((0, 0, 0))
        countdown_text = font.Font(None, 72).render(str(game_state["countdown"]), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 30))
        display.update()
        continue  # Не малюємо гру до завершення відліку

    if "winner" in game_state and game_state["winner"] is not None:
        screen.fill((20, 20, 20))

        if you_winner is None:  # Встановлюємо тільки один раз
            if game_state["winner"] == my_id:
                you_winner = True
            else:
                you_winner = False

        if you_winner:
            text = "Ти переміг!"
        else:
            text = "Пощастить наступним разом!"

        win_text = font_win.render(text, True, (255, 215, 0))
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)

        text = font_win.render('К - рестарт', True, (255, 215, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(text, text_rect)

        display.update()
        continue  # Блокує гру після перемоги

    if game_state:
        screen.blit(background_image, (0, 0)) # !!!!!!!!!!!!!!!!

        screen.blit(paddle_left_img, (20,game_state['paddles']['0']))
        screen.blit(paddle_right_img, (WIDTH - 40, game_state['paddles']['1']))


        screen.blit(ball_image, (game_state['ball']['x'] - 10, game_state['ball']['y'] - 10)) # !!!!!!!!
        score_text = font_main.render(f"{game_state['scores'][0]} : {game_state['scores'][1]}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 -25, 20))

        if sound_on and game_state['sound_event']:
            if game_state['sound_event'] == 'wall_hit':
                sound_wall_hit.play()
            if game_state['sound_event'] == 'platform_hit':
                sound_platform_hit.play()

    else:
        wating_text = font_main.render(f"Очікування гравців...", True, (255, 255, 255))
        screen.blit(wating_text, (WIDTH // 2 - 25, 20))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_w]:
        client.send(b"UP")
    elif keys[K_s]:
        client.send(b"DOWN")
