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
                    row.append(Block())
                else:
                    row.append(Blank())

    def print_field(self):
        for y in range(self.height):
            row_str = ''
            for element in self.field[y]:
                row_str += str(element) + ' '
            print row_str

    def insert_object(self, x, y, entity_object):
        assert x < self.length
        assert y < self.height

        self.field[y][x] = entity_object
        entity_object.x = x
        entity_object.y = y


f = Field(20, 6)

b = Block()
c = Creature()

f.insert_object(5, 2, c)
f.insert_object(3, 4, b)

for i in range(20):
    print c.act(f)
    f.print_field()
