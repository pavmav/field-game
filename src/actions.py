# -*- coding: utf-8 -*-

class Action(object):
    def __init__(self, subject):
        self.subject = subject
        self.accomplished = False
        self.time_start = subject.board.epoch
        self.time_finish = None

    def do(self):
        pass

    def get_result(self):
        return self.accomplished


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

                if (len(field_map) - 1 >= y + 1) and field_map[y + 1][x] is None:
                    field_map[y + 1][x] = wave_num
                    next_wave_list.append((x, y + 1))

                if (y > 0) and field_map[y - 1][x] is None:
                    field_map[y - 1][x] = wave_num
                    next_wave_list.append((x, y - 1))

                if (len(field_map[y]) - 1 >= x + 1) and field_map[y][x + 1] is None:
                    field_map[y][x + 1] = wave_num
                    next_wave_list.append((x + 1, y))

                if (x > 0) and field_map[y][x - 1] is None:
                    field_map[y][x - 1] = wave_num
                    next_wave_list.append((x - 1, y))

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

        for input_row in self.subject.board.get_field():
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
            if not self.subject.board.cell_passable(step_coordinates[0], step_coordinates[1]):
                return False

        return True

    def set_xy(self, x, y):
        self.target_x = x
        self.target_y = y

    def do(self):
        super(MovementXY, self).do()
        self.check_set_accomplishment()
        if self.accomplished:
            return True

        if not self.path or not self.check_path_passable():
            self.initialize_path()

        if not self.path:
            return self.accomplished

        current_step_x, current_step_y = self.path[0]

        if self.subject.board.cell_passable(current_step_x, current_step_y):
            self.subject.board.remove_object(self.subject, self.subject.x, self.subject.y)
            self.subject.board.insert_object(current_step_x, current_step_y, self.subject, epoch=1)
            self.path.pop(0)

        self.check_set_accomplishment()

        return self.accomplished

    def check_set_accomplishment(self):
        self.accomplished = (self.subject.x == self.target_x and self.subject.y == self.target_y)


class SearchSubstance(Action):
    def __init__(self, subject):
        super(SearchSubstance, self).__init__(subject)

        self.__target_substance_type = None

        self.__substance_x = None
        self.__substance_y = None

    def set_target(self, substance_type):
        self.__target_substance_type = substance_type

    def get_result(self):

        if not self.accomplished:
            self.do()

        if self.__substance_x is None or self.__substance_y is None:
            return self.accomplished

        return self.__substance_x, self.__substance_y

    def search(self):
        continue_search = False
        radius = 1

        while continue_search or radius == 1:
            continue_search = False
            # print radius
            for x in range(self.subject.x - radius, self.subject.x + radius + 1):
                if x == self.subject.x - radius or x == self.subject.x + radius:
                    for y in range(self.subject.y - radius, self.subject.y + radius + 1):
                        if (x >= 0 and x < self.subject.board.length) and (y >= 0 and y < self.subject.board.height):
                            cell = self.subject.board.get_cell(x, y)
                            for element in cell:
                                # print self.__target_substance_type
                                if element.contains(self.__target_substance_type):
                                    self.__substance_x = x
                                    self.__substance_y = y
                                    self.accomplished = True
                                    return
                            continue_search = True
                else:
                    for y in [self.subject.y - radius, self.subject.y + radius]:
                        if (x >= 0 and x < self.subject.board.length) and (y >= 0 and y < self.subject.board.height):
                            cell = self.subject.board.get_cell(x, y)
                            for element in cell:
                                # print self.__target_substance_type
                                if element.contains(self.__target_substance_type):
                                    self.__substance_x = x
                                    self.__substance_y = y
                                    self.accomplished = True
                                    return
                            continue_search = True

                        # print x, y

            radius += 1

    def do(self):
        super(SearchSubstance, self).do()
        self.search()


class ExtractSubstance(Action):
    def __init__(self, subject):
        super(ExtractSubstance, self).__init__(subject)

        self.__substance_x = None
        self.__substance_y = None

        self.__substance_type = None

    def set_objective(self, substance_x, substance_y, substance_type):
        self.__substance_type = substance_type
        self.__substance_x = substance_x
        self.__substance_y = substance_y

    def get_result(self):
        return super(ExtractSubstance, self).get_result()

    def do(self):
        super(ExtractSubstance, self).do()

        cell = self.subject.board.get_cell(self.__substance_x, self.__substance_y)

        for element in cell:
            if element.contains(self.__substance_type):
                self.subject.pocket(element.extract(self.__substance_type))
                self.accomplished = True
                break
