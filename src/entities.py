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

        if (self.time_of_death != None) and self.z - self.time_of_death > 10:
            self.dissolve()
            return

        if not self.alive:
            return

        if random.random() <= 0.005 and self.age > 10:
            self.die()
            return

        self.wander()

    def wander(self):
        move_east = actions.MovementXY(self)
        move_east.set_xy(self.x + 1, self.y)
        move_north = actions.MovementXY(self)
        move_north.set_xy(self.x, self.y - 1)
        move_west = actions.MovementXY(self)
        move_west.set_xy(self.x - 1, self.y)
        move_south = actions.MovementXY(self)
        move_south.set_xy(self.x, self.y + 1)

        possible_actions = [move_east, move_north, move_west, move_south]
        chosen_action = random.choice(possible_actions)
        return chosen_action.do()

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

        if random.random() < 0.1:
            new_creature = Creature()
            self.board.insert_object(self.x, self.y, new_creature)
