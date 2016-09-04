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
        pass

    def __str__(self):
        raise Exception

    def live(self):
        self.z += 1
        self.age += 1
        pass


class Block(Entity):
    def __init__(self):
        super(Block, self).__init__()
        self.passable = False

    def __str__(self):
        return '#'


class Creature(Entity):
    def __init__(self):
        super(Creature, self).__init__()
        self.passable = False
        self.scenery = False
        self.alive = True

    def __str__(self):
        return '@'

    def live(self):
        if not self.alive:  # TODO возможны ли зомби? и надо ли вообще что-либо возвращать?
            return False

        if self.age <= 25:
            action_result = self.wander()
            self.z += 1
            self.age += 1
            return action_result
        else:
            self.die()

    def move(self, x, y):
        if self.board.field[y][x][-1].passable:
            self.board.field[self.y][self.x].pop()
            self.board.insert_object(x, y, self)
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


class Blank(Entity):
    def __init__(self):
        super(Blank, self).__init__()
        self.passable = True

    def __str__(self):
        return '.'
