# -*- coding: utf-8 -*-

from entities import *
import pickle


class Field(object):
    def __init__(self, length, height):
        self.length = length
        self.height = height
        self.__field = []
        self.epoch = 0
        self.population = 0

        for y in range(self.height):
            row = []
            self.__field.append(row)
            for x in range(self.length):
                if y == 0 or x == 0 or y == (height - 1) or x == (length - 1):
                    init_object = Block()
                else:
                    init_object = Blank()

                init_object.x = x
                init_object.y = y
                init_object.z = 0

                row.append([init_object])

    def get_field(self):
        return self.__field

    def get_cell(self, x, y):
        return self.__field[y][x]

    def cell_passable(self, x, y):
        return self.__field[y][x][-1].passable

    def print_field(self):
        for y in range(self.height):
            row_str = ''
            for element in self.__field[y]:
                row_str += str(element[-1]) + ' '
            print row_str

    def list_str_representation(self):
        representation = []
        for y in range(self.height):
            row_str = ''
            for element in self.__field[y]:
                row_str += str(element[-1])
            representation.append(row_str)
        return representation

    def list_obj_representation(self):
        representation = []
        for y in range(self.height):
            row_list = []
            for cell in self.__field[y]:
                row_list.append(cell[-1])
            representation.append(row_list)
        return representation

    def insert_object(self, x, y, entity_object, epoch=0):
        assert x < self.length
        assert y < self.height

        if self.__field[y][x][-1].scenery:
            self.__field[y][x].append(entity_object)
        else:
            self.__field[y][x][-1] = entity_object

        entity_object.z = self.epoch + epoch  # TODO возможно, надо ставить следующую эпоху

        entity_object.board = self
        entity_object.x = x
        entity_object.y = y

    def remove_object(self, entity_object, x=None, y=None):
        if x is not None and y is not None:
            cell = self.get_cell(x, y)
            cell.remove(entity_object)
        else:
            for row in self.__field:
                for cell in row:
                    if entity_object in cell:
                        cell.remove(entity_object)

    def make_time(self):
        for y in range(self.height):
            for x in range(self.length):
                for element in self.__field[y][x]:
                    if element.z == self.epoch:
                        element.live()

        self.epoch += 1

    def integrity_check(self):
        error_list = []
        # First we check the __field structure
        # and make full list of objects
        objects_full_list = []
        if len(self.__field) != self.height:
            error_str = "Field height ({0}) is not equal to the number of rows({1})".format(self.height,
                                                                                            len(self.__field))
            error_list.append(error_str)
        for y, row in enumerate(self.__field):
            if len(row) != self.length:
                error_str = "Field length ({0}) is not equal to the number of cells ({1}) in row {2}".format(
                    self.height, len(self.__field), y)
                error_list.append(error_str)
            for x, cell in enumerate(row):
                if len(cell) == 0:
                    error_str = "Absolute vacuum (empty list) at coordinates x:{0} y:{1}".format(x, y)
                    error_list.append(error_str)
                for element in cell:
                    objects_full_list.append(element)
                    if element.x != x or element.y != y:
                        error_str = "Object at coordinates x:{0} y:{1} thinks it's at x:{2} y:{3}".format(x, y,
                                                                                                          element.x,
                                                                                                          element.y)
                        error_list.append(error_str)
                    if element.z != self.epoch:
                        error_str = "Object {0} at spacial coordinates x:{1} y:{2} travels in time. Global " \
                                    "epoch: {3}, its local time: {4}".format(str(element), x, y, self.epoch, element.z)
                        error_list.append(error_str)

        # Then we check for object doubles

        for line in error_list:
            print line
        return error_list

    def save_pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)


def load_from_pickle(filename):
    with open(filename, 'rb') as f:
        field = pickle.load(f)
    return field
