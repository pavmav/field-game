def wave(field, x1, y1, x2, y2):
    current_wave_list = [(x1, y1)]
    field[y1][x1] = 0

    while len(current_wave_list) > 0 and field[y2][x2] is None:
        next_wave_list = []
        for coordinates in current_wave_list:
            x, y = coordinates
            wave_num = field[y][x] + 1

            if (len(field) - 1 >= y + 1) and field[y + 1][x] is None:
                field[y + 1][x] = wave_num
                next_wave_list.append((x, y + 1))

            if (y > 0) and field[y - 1][x] is None:
                field[y - 1][x] = wave_num
                next_wave_list.append((x, y - 1))

            if (len(field[y]) - 1 >= x + 1) and field[y][x + 1] is None:
                field[y][x + 1] = wave_num
                next_wave_list.append((x + 1, y))

            if (x > 0) and field[y][x - 1] is None:
                field[y][x - 1] = wave_num
                next_wave_list.append((x - 1, y))

        current_wave_list = next_wave_list[:]


def find_backwards(field, x2, y2):
    num_steps = field[y2][x2]

    if num_steps is None or num_steps == -1:
        return None

    path = [(x2, y2)]
    num_steps -= 1

    while num_steps > 0:

        x, y = path[-1]

        if (len(field) - 1 >= y + 1) and (field[y + 1][x] == num_steps):
            path.append((x, y + 1))
        elif (y > 0) and (field[y - 1][x] == num_steps):
            path.append((x, y - 1))
        elif (len(field[y]) - 1 >= x + 1) and (field[y][x + 1] == num_steps):
            path.append((x + 1, y))
        elif (x > 0) and (field[y][x - 1] == num_steps):
            path.append((x - 1, y))

        num_steps -= 1

    path.reverse()

    return path


def find_way(field, x1, y1, x2, y2):
    if field[y2][x2] == -1:
        return None

    wave(field, x1, y1, x2, y2)
    return find_backwards(field, x2, y2)


# field = [[None, None, None, None, None],
#          [-1, -1, -1, -1, None],
#          [None, None, None, None, None],
#          [None, -1, -1, -1, -1],
#          [None, None, 0, None, None],
#          [None, None, None, None, None]]
#
# print find_way(field, 2, 4, 3, 0)

# for i in range(2,5):
#     print i

class Foo(object):

    def __init__(self):
        self.__bar = 7
    pass

    def spam(self):
        # setattr(a, "__bar", 3)
        self.__setattr__("__bar", 3)

    def eggs(self):
        print self.__bar

a = Foo()

a.spam()

a.eggs()