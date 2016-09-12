# -*- coding: utf-8 -*-

import random
import actions


class Entity(object):
    def __init__(self):
        # home universe
        self.board = None

        # time-space coordinates
        self.x = None
        self.y = None
        self.z = None

        # lifecycle properties
        self.age = 0
        self.alive = False
        self.time_of_death = None

        # action queues
        self.action_queue = []
        self.action_log = []

        # common properties
        self.passable = False
        self.scenery = True

        # visualization properties
        self.color = "#004400"

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

        if (self.time_of_death is not None) and self.z - self.time_of_death > 10:
            self.dissolve()
            return

        if not self.alive:
            return

        if random.random() <= 0.005 and self.age > 10:
            self.die()
            return

        if len(self.action_queue) == 0:
            x = random.randint(1, self.board.length-2)
            y = random.randint(1, self.board.height-2)

            if not self.board.field[y][x][-1].passable:
                return

            move_random = actions.MovementXY(self)
            move_random.set_xy(x, y)

            self.action_queue.append(move_random)

        self.action_queue[0].do()

        if self.action_queue[0].accomplished:
            self.action_log.append(self.action_queue.pop(0))

    def die(self):
        self.alive = False
        self.time_of_death = self.z


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

        if random.random() < 0.5:
            new_creature = Creature()
            self.board.insert_object(self.x, self.y, new_creature)
