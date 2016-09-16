# -*- coding: utf-8 -*-

import pygame
from pygame import *

# <editor-fold desc="Field">
from field import *
# import __field

# </editor-fold>

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 10
PLATFORM_HEIGHT = 10


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Field game")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    # <editor-fold desc="Text stats">
    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont = pygame.font.SysFont("monospace", 15)
    # </editor-fold>

    # <editor-fold desc="Field">
    f = Field(60, 40)

    b = Block()
    g = Creature()
    c = Creature()
    c.name = "John"
    brg = BreedingGround()

    f.insert_object(5, 2, c)
    f.insert_object(30, 20, g)
    f.insert_object(3, 4, b)
    # f.insert_object(10, 15, brg)

    level = f.list_obj_representation()

    # f = __field.load_from_pickle("__field.pickle")

    # </editor-fold>

    timer = pygame.time.Clock()

    while 1:  # Основной цикл программы
        timer.tick(10)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit, "QUIT"

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        # <editor-fold desc="Field">  TODO Нет первого состояния!
        f.integrity_check()
        f.make_time()
        # f.save_pickle("__field.pickle")
        level = f.list_obj_representation()
        # </editor-fold>

        # <editor-fold desc="Text stats">
        # render text
        label = myfont.render("Epoch: {0}".format(f.epoch), 1, (255, 255, 0))
        screen.blit(label, (630, 10))

        stats = f.get_stats()
        for i, element in enumerate(stats):
            label = myfont.render("{0}: {1}".format(element, stats[element]), 1, (255, 255, 0))
            screen.blit(label, (630, 25 + (i*15)))

        # </editor-fold>

        x = y = 0  # координаты

        for row in level:  # вся строка
            for element in row:  # каждый символ
                pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf.fill(Color(element.color))
                screen.blit(pf, (x, y))

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
