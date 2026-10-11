from math import hypot
from socket import socket, AF_INET, SOCK_STREAM
from pygame import *
from threading import Thread
from random import randint
from menu import ConnectWindow   # беремо наше вікно з файлу menu.py

win = ConnectWindow()   # створюємо лаунчер
win.mainloop()          # ПАУЗА: програма чекає тут, поки вікно не закриють

if win.host is None:    # якщо закрили хрестиком, даних немає
    exit()              # тож просто виходимо, щоб не було помилки

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((win.host, win.port))   # підключаємось за адресою з лаунчера, а не до localhost
my_data = list(map(int, sock.recv(64).decode().strip().split(',')))
my_id = my_data[0]
my_player = my_data[1:]
sock.setblocking(False)

init()
window = display.set_mode((1000, 1000))
clock = time.Clock()
f = font.Font(None, 50)
all_players = []
running = True
lose = False


def receive_data():
    global all_players, running, lose
    while running:
        try:
            data = sock.recv(4096).decode().strip()
            if data == "LOSE":
                lose = True
            elif data:
                parts = data.strip('|').split('|')
                all_players = [list(map(int, p.split(','))) for p in parts if len(p.split(',')) == 4]
        except:
            pass


Thread(target=receive_data, daemon=True).start()


class Eat:
    def __init__(self, x, y, r, c):
        self.x = x
        self.y = y
        self.radius = r
        self.color = c

    def check_collision(self, player_x, player_y, player_r):
        dx = self.x - player_x
        dy = self.y - player_y
        return hypot(dx, dy) <= self.radius + player_r


eats = [Eat(randint(-2000, 2000), randint(-2000, 2000), 10,
            (randint(0, 255), randint(0, 255), randint(0, 255)))
        for _ in range(300)]

# Палітра кольорів. Кожен колір — це (червоний, зелений, синій), числа від 0 до 255
COLORS = [
    (231, 76, 60),    # червоний
    (52, 152, 219),   # синій
    (46, 204, 113),   # зелений
    (241, 196, 15),   # жовтий
    (155, 89, 182),   # фіолетовий
    (230, 126, 34),   # помаранчевий
    (26, 188, 156),   # бірюзовий
    (236, 64, 122),   # рожевий
]


def get_color(player_id):
    # % len(COLORS) — остача від ділення на 8, завжди від 0 до 7
    # тож номер ніколи не вийде за межі списку
    return COLORS[player_id % len(COLORS)]

score = 0                                # лічильник з'їденої їжі, на старті 0
score_font = font.SysFont('Arial', 30)   # шрифт для табло: Arial, розмір 30
                                         # (Arial вміє українські літери)

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    window.fill((255, 255, 255))
    scale = max(0.3, min(50 / my_player[2], 1.5))

    for p in all_players:
        if p[0] == my_id: continue
        sx = int((p[1] - my_player[0]) * scale + 500)
        sy = int((p[2] - my_player[1]) * scale + 500)
        draw.circle(window, get_color(p[0]), (sx, sy), int(p[3] * scale))

    draw.circle(window, get_color(my_id), (500, 500), int(my_player[2] * scale))

    to_remove = []
    for eat in eats:
        if eat.check_collision(my_player[0], my_player[1], my_player[2]):
            to_remove.append(eat)
            my_player[2] += int(eat.radius * 0.2)
            score += 1   # збільшуємо лічильник на 1
        else:
            sx = int((eat.x - my_player[0]) * scale + 500)
            sy = int((eat.y - my_player[1]) * scale + 500)
            draw.circle(window, eat.color, (sx, sy), int(eat.radius * scale))
    for eat in to_remove:
        eats.remove(eat)

    if lose:
        t = f.render('U lose!', 1, (244, 0, 0))
        window.blit(t, (400, 500))

        # render() — "надрукуй текст на картинці"
    # True — згладжування літер, щоб були гладенькі
    # (0, 0, 0) — чорний колір тексту
    score_text = score_font.render(f'Їжа: {score}   Розмір: {my_player[2]}', True, (0, 0, 0))

    # blit() — "приклей картинку на екран" у точку (20, 20): 20 від лівого краю і 20 від верху
    window.blit(score_text, (20, 20))

    display.update()
    clock.tick(60)

    if not lose:
        keys = key.get_pressed()
        if keys[K_w]: my_player[1] -= 15
        if keys[K_s]: my_player[1] += 15
        if keys[K_a]: my_player[0] -= 15
        if keys[K_d]: my_player[0] += 15

        try:
            msg = f"{my_id},{my_player[0]},{my_player[1]},{my_player[2]}"
            sock.send(msg.encode())
        except:
            pass

quit()