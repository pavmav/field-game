# -*- coding: utf-8 -*-

from entities import *


class Field(object):
    def __init__(self, length, height):
        self.length = length
        self.height = height
        self.field = []
        self.epoch = 0

        for y in range(self.height):
            row = []
            self.field.append(row)
            for x in range(self.length):
                if y == 0 or x == 0 or y == (height - 1) or x == (length - 1):
                    init_object = Block()
                else:
                    init_object = Blank()

                init_object.x = x
                init_object.y = y
                init_object.z = 0

                row.append([init_object])

    def print_field(self):
        for y in range(self.height):
            row_str = ''
            for element in self.field[y]:
                row_str += str(element[-1]) + ' '
            print row_str

    def list_str_representation(self):
        representation = []
        for y in range(self.height):
            row_str = ''
            for element in self.field[y]:
                row_str += str(element[-1])
            representation.append(row_str)
        return representation

    def insert_object(self, x, y, entity_object, epoch = 0):
        assert x < self.length
        assert y < self.height

        if self.field[y][x][-1].scenery:
            self.field[y][x].append(entity_object)
        else:
            self.field[y][x][-1] = entity_object

        entity_object.z = self.epoch + epoch  # TODO возможно, надо ставить следующую эпоху

        entity_object.board = self
        entity_object.x = x
        entity_object.y = y

    def make_time(self):
        for y in range(self.height):
            for x in range(self.length):
                for element in self.field[y][x]:
                    if element.z == self.epoch:
                        element.live()

        self.epoch += 1

    def integrity_check(self):
        error_list = []
        # First we check the field structure
        # and make full list of objects
        objects_full_list = []
        if len(self.field) != self.height:
            error_str = "Field height ({0}) is not equal to the number of rows({1})".format(self.height,
                                                                                            len(self.field))
            error_list.append(error_str)
        for y, row in enumerate(self.field):
            if len(row) != self.length:
                error_str = "Field length ({0}) is not equal to the number of cells ({1}) in row {2}".format(
                                                                                        self.height, len(self.field), y)
                error_list.append(error_str)
            for x, cell in enumerate(row):
                if len(cell) == 0:
                    error_str = "Absolute vacuum (empty list) at coordinates x:{0} y:{1}".format(x, y)
                    error_list.append(error_str)
                for element in cell:
                    objects_full_list.append(element)

        # Then we check for object doubles

        for line in error_list:
            print line
        return error_list
