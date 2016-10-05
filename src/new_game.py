# -*- coding: utf-8 -*-

import pygame
from pygame import *

import tkinter as tk
import tkFileDialog

# <editor-fold desc="Field">
from field import *
import field
import entities
import pandas

# </editor-fold>

import cProfile

def profile(func):
    """Decorator for run function profile"""
    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result
    return wrapper

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

    # b = Block()
    # c = Creature()
    # c.name = "John"
    # g = Creature()
    #
    # c.set_sex(True)
    # c.add_state(states.NotTheRightMood(c))
    # g.set_sex(False)
    #
    # c.mortal = False
    # g.mortal = False

    # brg = BreedingGround()
    #
    # f.insert_object(5, 2, c)
    # f.insert_object(30, 20, g)
    # f.insert_object(3, 4, b)
    # f.insert_object(10, 15, brg)

    f.populate(entities.Creature, 20)

    for y in range(10, 30):
        f.insert_object(20, y, Block())

    for x in range(21, 40):
        f.insert_object(x, 10, Block())

    for y in range(10, 30):
        f.insert_object(40, y, Block())

    level = f.list_obj_representation()

    # f = __field.load_from_pickle("__field.pickle")

    tick = 10

    # </editor-fold>

    timer = pygame.time.Clock()
    go_on = True

    while go_on:  # Основной цикл программы
        timer.tick(tick)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit, "QUIT"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    f.pause = not f.pause
                elif e.key == pygame.K_s:
                    root = tk.Tk()
                    root.withdraw()
                    file_path = tkFileDialog.asksaveasfilename()
                    f.save_pickle(file_path)
                elif e.key == pygame.K_l:
                    root = tk.Tk()
                    root.withdraw()
                    file_path = tkFileDialog.askopenfilename()
                    f = field.load_from_pickle(file_path)
                    f.pause = True
                elif e.key == pygame.K_UP:
                    tick += 10
                elif e.key == pygame.K_DOWN and tick >= 11:
                    tick -= 10
                elif e.key == pygame.K_ESCAPE:
                    go_on = False
                # elif e.key == pygame.K_c:
                #     print c.count_substance_of_type(substances.Substance)
                # elif e.key == pygame.K_m:
                #     l = c.learning_memory.make_table(actions.GoMating)
                #     print "/n"
                #     for line in l:
                #         print line
                elif e.key == pygame.K_g:
                    table_list_of_dicts = f.public_memory.make_table(actions.GoMating)
                    df = pandas.DataFrame.from_dict(*[table_list_of_dicts])
                    print df

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        # <editor-fold desc="Field">  TODO Нет первого состояния!
        # if f.epoch == 1000:
        #     f.pause = True
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
