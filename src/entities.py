# -*- coding: utf-8 -*-

import random


class Entity(object):
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.passable = False
        self.scenery = True
        self.board = None
        self.age = 0
        self.alive = False
        self.color = "#004400"
        pass

    def __str__(self):
        raise Exception

    def live(self):
        self.z += 1
        self.age += 1


    def dissolve(self):
        cell = self.board.field[self.y][self.x]
        cell.remove(self)


class Blank(Entity):
    def __init__(self):
        super(Blank, self).__init__()
        self.passable = True
        self.color = "#004400"

    def __str__(self):
        return '.'


class Block(Entity):
    def __init__(self):
        super(Block, self).__init__()
        self.passable = False
        self.color = "#000000"

    def __str__(self):
        return '#'


class Creature(Entity):
    def __init__(self):
        super(Creature, self).__init__()
        self.passable = False
        self.scenery = False
        self.alive = True
        self.name = ''
        self.color = "#550000"

    def __str__(self):
        return '@'

    def live(self):
        super(Creature, self).live()

        if self.age > 50:
            self.dissolve()
            return

        if not self.alive:
            return

        if random.random() <= 0.005:
            self.die()
            return

        self.wander()

    def move(self, x, y):
        if self.board.field[y][x][-1].passable:
            self.board.field[self.y][self.x].pop()
            self.board.insert_object(x, y, self, epoch = 1)
            return True
        else:
            return False

    def wander(self):
        possible_actions = [self.move_east, self.move_north, self.move_west, self.move_south]
        action = random.choice(possible_actions)
        return action()

    def move_north(self):
        return self.move(self.x, self.y - 1)

    def move_south(self):
        return self.move(self.x, self.y + 1)

    def move_east(self):
        return self.move(self.x + 1, self.y)

    def move_west(self):
        return self.move(self.x - 1, self.y)

    def die(self):
        self.alive = False


class BreedingGround(Entity):
    def __init__(self):
        super(BreedingGround, self).__init__()
        self.passable = True
        self.color = "#000055"

    def __str__(self):
        return "*"

    def live(self):
        super(BreedingGround, self).live()

        if not self.board.field[self.y][self.x][-1].passable:
            return

        if random.random() < 0.05:
            new_creature = Creature()
            self.board.insert_object(self.x, self.y, new_creature)
