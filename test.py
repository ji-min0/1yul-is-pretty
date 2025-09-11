import pygame
from window import Window, Layer, Button, TextLabel, TextOutput, Image, TextInput
import os; import sys;
pygame.init()
try:
    if hasattr(sys, "_MEIPASS"):
        os.chdir(sys._MEIPASS)
except Exception:
    pass
screen_width = 600
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("한율이는 이쁘다")

ui = Window(size=screen.get_size())
base = ui.add_layer("base", z_index=0)
overlays = ui.add_layer("overlays", z_index=10)

btn = Button((257, 735, 100, 60), text="클릭",bg=(0,0,0),font_size=24)
out = TextOutput((55, 470, 500, 230),font_size = 24,text_color=(255,255,255),bg_color=(51,51,204),border_color=(255,255,255),border_radius=25,padding=10)
input = TextInput()
lbl = TextLabel((0, 100, screen_width, 0), text="한율이는 이쁘다",font_size=52,color=(255,255,255),align = "center")
img = Image("assets/bg.jpg",(0,0,screen_height,screen_width))

base.add(img)
base.add(btn)
base.add(lbl)
base.add(out)


btn.on_click = lambda b: out.print("클릭됨")

running = True

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            ui.handle_event(event)
    ui.update(dt)
    ui.draw(screen)
    pygame.display.flip()