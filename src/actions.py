# -*- coding: utf-8 -*-

import random
import entities
import math
import states

class Action(object):
    def __init__(self, subject):
        self.subject = subject
        self.accomplished = False
        self._done = False
        self.instant = False
        # self.time_start = subject.board.epoch
        # self.time_finish = None

    def get_objective(self):
        return {}

    def set_objective(self, control=False, **kwargs):
        valid_objectives = self.get_objective().keys()

        for key in kwargs.keys():
            if not key in valid_objectives:
                if control:
                    raise ValueError("{0} is not a valid objective".format(key))
                else:
                    pass  # maybe need to print
            else:
                setattr(self, "_{0}".format(key), kwargs[key])

    def action_possible(self):
        return True

    def do(self):
        self.check_set_results()
        self._done = True

    def check_set_results(self):
        self.accomplished = True

    @property
    def results(self):
        out = {"done": self._done, "accomplished": self.accomplished}
        return out

    def do_results(self):
        self.do()
        return self.results


class MovementXY(Action):
    def __init__(self, subject):
        super(MovementXY, self).__init__(subject)

        self._target_x = None
        self._target_y = None

        self.path = []

    def get_objective(self):
        out = {"target_x": self._target_x, "target_y": self._target_y}

        return out

    def action_possible(self):

        if self._target_x is None or self._target_y is None:
            return False

        if self.path is None or len(self.path) == 0:
            self.initialize_path()

        if self.path is None or len(self.path) == 0:
            return False

        return True

    def do(self):

        if self.results["done"]:
            return

        if not self.action_possible():
            return

        if not self.path or not self.check_path_passable():
            self.initialize_path()

        if not self.path:
            self.check_set_results()
            self._done = True
            return

        current_step_x, current_step_y = self.path.pop(0)

        if self.subject.board.cell_passable(current_step_x, current_step_y):
            self.subject.board.remove_object(self.subject, self.subject.x, self.subject.y)
            self.subject.board.insert_object(current_step_x, current_step_y, self.subject, epoch=1)

        self.check_set_results()

        self._done = self.results["accomplished"]

    def check_set_results(self):
        self.accomplished = (self.subject.x == self._target_x and self.subject.y == self._target_y)

    def initialize_path(self):
        field_map = self.__make_map()
        self.__wave(field_map, self.subject.x, self.subject.y, self._target_x, self._target_y)

        if field_map[self._target_y][self._target_x] == -1:
            self.path = []

        self.path = self.__find_backwards(field_map, self._target_x, self._target_y)

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

            possible_steps = []

            if (len(field_map) - 1 >= y + 1) and (field_map[y + 1][x] == num_steps):
                possible_steps.append((x, y + 1))
            elif (y > 0) and (field_map[y - 1][x] == num_steps):
                possible_steps.append((x, y - 1))
            elif (len(field_map[y]) - 1 >= x + 1) and (field_map[y][x + 1] == num_steps):
                possible_steps.append((x + 1, y))
            elif (x > 0) and (field_map[y][x - 1] == num_steps):
                possible_steps.append((x - 1, y))

            # for row in field_map:
            #     print row

            path.append(random.choice(possible_steps))

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

        return self.subject.board.cell_passable(self.path[0][0], self.path[0][1])

        for step_coordinates in self.path:
            if not self.subject.board.cell_passable(step_coordinates[0], step_coordinates[1]):
                return False

        return True


class MovementToEntity(MovementXY):
    def __init__(self, subject):
        super(MovementToEntity, self).__init__(subject)

        self._target_entity = None

    def get_objective(self):
        out = {"target_entity": self._target_entity}

        return out

    def action_possible(self):

        if self._target_entity is None:
            return False

        self.set_target_coordinates()

        if self._target_x is None or self._target_y is None:
            return False

        if self.path is None or len(self.path) == 0:
            self.initialize_path()

        if self.path is None or len(self.path) == 0:
            return False

        return True

    def do(self):

        if self.results["done"]:
            return

        if not self.action_possible():
            return

        self.set_target_coordinates()

        self.initialize_path()

        if not self.action_possible():
            return

        super(MovementToEntity, self).do()

        self.check_set_results()

        self._done = self.results["accomplished"]

    def check_set_results(self):
        if self._target_entity.passable:
            self.accomplished = (self.subject.x == self._target_x and self.subject.y == self._target_y)
        else:
            distance = abs(self.subject.x - self._target_entity.x) + abs(self.subject.y - self._target_entity.y)
            self.accomplished = distance < 2

    def set_target_coordinates(self):
        if self._target_entity.passable:
            self._target_x = self._target_entity.x
            self._target_y = self._target_entity.y
        else:
            cells_near = []
            if self.subject.board.cell_passable(self._target_entity.x, self._target_entity.y+1):
                cells_near.append((self._target_entity.x, self._target_entity.y+1))
            if self.subject.board.cell_passable(self._target_entity.x, self._target_entity.y-1):
                cells_near.append((self._target_entity.x, self._target_entity.y-1))
            if self.subject.board.cell_passable(self._target_entity.x+1, self._target_entity.y):
                cells_near.append((self._target_entity.x+1, self._target_entity.y))
            if self.subject.board.cell_passable(self._target_entity.x-1, self._target_entity.y):
                cells_near.append((self._target_entity.x-1, self._target_entity.y))
            if len(cells_near) == 0:
                return

            best_coordinates = random.choice(cells_near)
            smallest_distance = 9e10

            for coordinates in cells_near:
                distance = math.sqrt((self.subject.x - coordinates[0])**2 + (self.subject.y - coordinates[1])**2)

                if distance < smallest_distance:
                    smallest_distance = distance
                    best_coordinates = coordinates

            self._target_x, self._target_y = best_coordinates


class SearchSubstance(Action):
    def __init__(self, subject):
        super(SearchSubstance, self).__init__(subject)

        self.instant = True

        self._target_substance_type = None

        self._substance_x = None
        self._substance_y = None

    def get_objective(self):
        out = {"target_substance_type": self._target_substance_type}

        return out

    def action_possible(self):
        if self._target_substance_type is None:
            return False

        return True

    def do(self):
        if self.results["done"]:
            return

        if not self.action_possible():
            return

        self.search()

        self.check_set_results()
        self._done = True

    def check_set_results(self):
        self.accomplished = (self._substance_x is not None and self._substance_y is not None)

    @property
    def results(self):
        out = super(SearchSubstance, self).results

        out["substance_x"] = self._substance_x
        out["substance_y"] = self._substance_y

        return out

    def search(self):
        continue_search = False
        radius = 1

        while continue_search or radius == 1:
            continue_search = False
            for x in range(self.subject.x - radius, self.subject.x + radius + 1):
                if x == self.subject.x - radius or x == self.subject.x + radius:
                    for y in range(self.subject.y - radius, self.subject.y + radius + 1):
                        if (0 <= x < self.subject.board.length) and (0 <= y < self.subject.board.height):
                            cell = self.subject.board.get_cell(x, y)
                            for element in cell:
                                if element.contains(self._target_substance_type) and not element.alive:
                                    self._substance_x = x
                                    self._substance_y = y
                                    return
                            continue_search = True
                else:
                    for y in [self.subject.y - radius, self.subject.y + radius]:
                        if (0 <= x < self.subject.board.length) and (0 <= y < self.subject.board.height):
                            cell = self.subject.board.get_cell(x, y)
                            for element in cell:
                                # print self._target_substance_type
                                if element.contains(self._target_substance_type) and not element.alive:
                                    self._substance_x = x
                                    self._substance_y = y
                                    return
                            continue_search = True
            radius += 1


class ExtractSubstanceXY(Action):
    def __init__(self, subject):
        super(ExtractSubstanceXY, self).__init__(subject)

        self.instant = True

        self._substance_x = None
        self._substance_y = None

        self._substance_type = None

    def get_objective(self):
        out = {"substance_type": self._substance_type, "substance_x": self._substance_x,
               "substance_y": self._substance_y}

        return out

    def action_possible(self):
        if self._substance_x is None or self._substance_y is None or self._substance_type is None:
            return False

        cell_contains_substance = False
        cell = self.subject.board.get_cell(self._substance_x, self._substance_y)
        for element in cell:
            if element.contains(self._substance_type):
                cell_contains_substance = True
                break

        if not cell_contains_substance:
            return False

        x_distance = abs(self._substance_x - self.subject.x)
        y_distance = abs(self._substance_y - self.subject.y)

        if x_distance + y_distance > 1:
            return False

        return True

    def do(self):
        if self.results["done"]:
            return

        if not self.action_possible():
            return

        cell = self.subject.board.get_cell(self._substance_x, self._substance_y)

        extracted = False

        for element in cell:
            if element.contains(self._substance_type):
                self.subject.pocket(element.extract(self._substance_type))
                extracted = True
                break

        if extracted:
            self.check_set_results()

        self._done = True

    def check_set_results(self):
        self.accomplished = True


class Mate(Action):
    def __init__(self, subject):
        super(Mate, self).__init__(subject)

        self.instant = True

        self._target_entity = None

    def get_objective(self):
        out = {"target_entity": self._target_entity}

        return out

    def action_possible(self):
        if self._target_entity is None:
            return False

        if not self.subject.will_mate(self._target_entity) or not self._target_entity.will_mate(self.subject):
            return False

        distance = abs(self.subject.x - self._target_entity.x) + abs(self.subject.y - self._target_entity.y)
        if distance > 1:
            return False

        return True

    def do(self):
        if self.results["done"]:
            return

        if not self.action_possible():
            return

        self._target_entity._states_list.append(states.Pregnant(self._target_entity))

        self._done = True

        self.check_set_results()

        self._done = self.results["accomplished"]

    def check_set_results(self):
        self.accomplished = self._done


class GiveBirth(Action):
    def __init__(self, subject, pregnant_state):
        super(GiveBirth, self).__init__(subject)

        self.pregnant_state = pregnant_state

    def action_possible(self):
        cells_around = self.get_empty_cells_around()

        if not cells_around:
            return False

        return True

    def do(self):
        if self.results["done"]:
            return

        if not self.action_possible():
            return

        cells_around = self.get_empty_cells_around()

        place = random.choice(cells_around)

        offspring = entities.Creature()

        self.subject.board.insert_object(place[0], place[1], offspring, epoch=1)

        self.subject._states_list.remove(self.pregnant_state)

        self._done = True

        self.check_set_results()

    def get_empty_cells_around(self):
        cells_near = []

        if self.subject.board.cell_passable(self.subject.x, self.subject.y + 1):
            cells_near.append((self.subject.x, self.subject.y + 1))
        if self.subject.board.cell_passable(self.subject.x, self.subject.y - 1):
            cells_near.append((self.subject.x, self.subject.y - 1))
        if self.subject.board.cell_passable(self.subject.x + 1, self.subject.y):
            cells_near.append((self.subject.x + 1, self.subject.y))
        if self.subject.board.cell_passable(self.subject.x - 1, self.subject.y):
            cells_near.append((self.subject.x - 1, self.subject.y))

        return cells_near
