from entities import *


class Field(object):
    def __init__(self, length, height):
        self.length = length
        self.height = height
        self.field = []

        for y in range(self.height):
            row = []
            self.field.append(row)
            for x in range(self.length):
                if y == 0 or x == 0 or y == (height - 1) or x == (length - 1):
                    row.append([Block()])
                else:
                    row.append([Blank()])

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

    def insert_object(self, x, y, entity_object):
        assert x < self.length
        assert y < self.height

        if self.field[y][x][-1].scenery:
            self.field[y][x].append(entity_object)
        else:
            self.field[y][x][-1] = entity_object

        entity_object.board = self
        entity_object.x = x
        entity_object.y = y

    def make_time(self):
        for y in range(self.height):
            for x in range(self.length):
                for element in self.field[y][x]:
                    element.act()

# f = Field(20, 6)
#
# b = Block()
# g = Creature()
# c = Creature()
#
# f.insert_object(5, 2, c)
# f.insert_object(4, 2, g)
# f.insert_object(3, 4, b)
#
# print c.move_west(f)
#
# for i in range(20):
#     print c.act(f)
#     f.print_field()
