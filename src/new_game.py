
# -*- coding: utf-8 -*-

import pygame
from pygame import *

# <editor-fold desc="Field">
from field import *
# </editor-fold>

#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#000000"
CREATURE_COLOR = "#550000"

def main():
    pygame.init() # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Field game") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

    # <editor-fold desc="Field">
    f = Field(20, 15)

    b = Block()
    g = Creature()
    c = Creature()

    f.insert_object(5, 2, c)
    f.insert_object(4, 2, g)
    f.insert_object(3, 4, b)

    level = f.list_str_representation()
    # </editor-fold>

    timer = pygame.time.Clock()

    while 1: # Основной цикл программы
        timer.tick(5)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit, "QUIT"

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        # <editor-fold desc="Field">

        f.make_time()
        level = f.list_str_representation()
        # </editor-fold>

        x = y = 0  # координаты

        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "#":
                    pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf.fill(Color(PLATFORM_COLOR))
                    screen.blit(pf, (x, y))
                elif col == "@":
                    pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf.fill(Color(CREATURE_COLOR))
                    screen.blit(pf, (x, y))

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        pygame.display.update()  # обновление и вывод всех изменений на экран

if __name__ == "__main__":
    main()