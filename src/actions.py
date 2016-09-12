# -*- coding: utf-8 -*-

class Action(object):
    def __init__(self, subject):
        self.subject = subject
        self.accomplished = False
        pass

    def do(self):
        pass


class MovementXY(Action):
    def __init__(self, subject):
        super(MovementXY, self).__init__(subject)
        self.target_x = None
        self.target_y = None

        self.path = []

    def initialize_path(self):
        field_map = self.__make_map()
        self.__wave(field_map, self.subject.x, self.subject.y, self.target_x, self.target_y)

        if field_map[self.target_y][self.target_x] == -1:
            self.path = []

        self.path = self.__find_backwards(field_map, self.target_x, self.target_y)

    @staticmethod
    def __wave(field_map, x1, y1, x2, y2):
        current_wave_list = [(x1, y1)]
        field_map[y1][x1] = 0

        while len(current_wave_list) > 0 and field_map[y2][x2] is None:
            next_wave_list = []
            for coordinates in current_wave_list:
                x, y = coordinates
                wave_num = field_map[y][x] + 1

                if (len(field_map)-1 >= y+1) and field_map[y+1][x] is None:
                    field_map[y+1][x] = wave_num
                    next_wave_list.append((x, y+1))

                if (y > 0) and field_map[y-1][x] is None:
                    field_map[y-1][x] = wave_num
                    next_wave_list.append((x, y-1))

                if (len(field_map[y])-1 >= x+1) and field_map[y][x+1] is None:
                    field_map[y][x+1] = wave_num
                    next_wave_list.append((x+1, y))

                if (x > 0) and field_map[y][x-1] is None:
                    field_map[y][x-1] = wave_num
                    next_wave_list.append((x-1, y))

            current_wave_list = next_wave_list[:]

    @staticmethod
    def __find_backwards(field_map, x2, y2):
        num_steps = field_map[y2][x2]

        if num_steps is None or num_steps == -1:
            return None

        path = [(x2, y2)]
        num_steps -= 1

        while num_steps > 0:

            x, y = path[-1]

            if (len(field_map) - 1 >= y + 1) and (field_map[y + 1][x] == num_steps):
                path.append((x, y + 1))
            elif (y > 0) and (field_map[y - 1][x] == num_steps):
                path.append((x, y - 1))
            elif (len(field_map[y]) - 1 >= x + 1) and (field_map[y][x + 1] == num_steps):
                path.append((x + 1, y))
            elif (x > 0) and (field_map[y][x - 1] == num_steps):
                path.append((x - 1, y))

            num_steps -= 1

        path.reverse()

        return path

    def __make_map(self):
        field_map = []

        for input_row in self.subject.board.field:
            row = []
            for cell in input_row:
                if cell[-1].passable:
                    row.append(None)
                else:
                    row.append(-1)
            field_map.append(row)

        return field_map

    def check_path_passable(self):

        for step_coordinates in self.path:
            if not self.subject.board.field[step_coordinates[1]][step_coordinates[0]][-1].passable:
                return False

        return True


    def set_xy(self, x, y):
        self.target_x = x
        self.target_y = y

    def do(self):
        self.check_set_accomplishment()
        if self.accomplished:
            return True

        if not self.path or not self.check_path_passable():
            self.initialize_path()

        if not self.path:
            return self.accomplished

        current_step_x, current_step_y = self.path[0]

        if self.subject.board.field[current_step_y][current_step_x][-1].passable:
            self.subject.board.field[self.subject.y][self.subject.x].pop()
            self.subject.board.insert_object(current_step_x, current_step_y, self.subject, epoch=1)
            self.path.pop(0)

        self.check_set_accomplishment()

        return self.accomplished

    def check_set_accomplishment(self):
        self.accomplished = (self.subject.x == self.target_x and self.subject.y == self.target_y)
