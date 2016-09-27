# -*- coding: utf-8 -*-

import random
import actions
import substances
import math
import states


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
        self._container = []
        self._states_list = []

        # visualization properties
        self.color = "#004400"

    def __str__(self):
        raise Exception

    @classmethod
    def class_name(cls):
        return "Entity"

    def live(self):
        self.get_affected()
        self.z += 1
        self.age += 1

    def get_affected(self):
        for state in self._states_list:
            state.affect()

    def has_state(self, state_type):
        for state in self._states_list:
            if isinstance(state, state_type):
                return True
        return False

    def add_state(self, state):
        self._states_list.append(state)

    def remove_state(self, state):
        self._states_list.remove(state)

    def contains(self, substance_type):
        for element in self._container:
            if type(element) == substance_type:
                return True
        return False

    def extract(self, substance_type):
        substance_index = None
        for i, element in enumerate(self._container):
            if type(element) == substance_type:
                substance_index = i
                break
        if substance_index is None:
            return None
        return self._container.pop(substance_index)

    def pocket(self, substance_object):
        if substance_object is not None:
            self._container.append(substance_object)

    def dissolve(self):
        self.board.remove_object(self)

    def find_nearest_coordinates_by_type(self, type_to_find):

        list_found = self.board.find_all_coordinates_by_type(type_to_find)

        smallest_distance = 9e10
        closest_so_far = None

        for coordinates in list_found:
            distance = math.sqrt((self.x - coordinates[0]) ** 2 + (self.y - coordinates[1]) ** 2)
            if distance <= smallest_distance:
                smallest_distance = distance
                closest_so_far = coordinates

        return closest_so_far

    def find_nearest_entity_by_type(self, type_to_find):
        coordinates = self.find_nearest_coordinates_by_type(type_to_find)

        if coordinates is None:
            return None

        cell = self.board.get_cell(**coordinates)

        for element in cell:
            if isinstance(element, type_to_find):
                return element

        return None


class Blank(Entity):
    def __init__(self):
        super(Blank, self).__init__()
        self.passable = True
        self.color = "#004400"

    def __str__(self):
        return '.'

    @classmethod
    def class_name(cls):
        return "Blank"

    def live(self):
        super(Blank, self).live()

        if random.random() <= 0.0002:
            self._container.append(substances.Substance())

        if len(self._container) > 0:
            self.color = "#224444"
        else:
            self.color = "#004400"


class Block(Entity):
    def __init__(self):
        super(Block, self).__init__()
        self.passable = False
        self.color = "#000000"

    def __str__(self):
        return '#'

    @classmethod
    def class_name(cls):
        return "Block"


class Creature(Entity):
    def __init__(self):
        super(Creature, self).__init__()
        self.passable = False
        self.scenery = False
        self.alive = True
        self.name = ''
        self.sex = random.choice([True, False])
        if self.sex:
            self.color = "#550000"
        else:
            self.color = "#990000"
        self.mortal = True

    def __str__(self):
        return '@'

    @classmethod
    def class_name(cls):
        return "Creature"

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

        if self.need_to_update_plan():
            self.plan()

        if len(self.action_queue) > 0:

            current_action = self.action_queue[0]

            self.perform_action(current_action)

            while len(self.action_queue) > 0 and self.action_queue[0].instant:
                current_action = self.action_queue[0]

                self.perform_action(current_action)

    def need_to_update_plan(self):
        return len(self.action_queue) == 0

    def plan(self):

        if self.sex:

            find_partner = actions.SearchMatingPartner(self)

            search_results = find_partner.do_results()

            if search_results["accomplished"]:
                fellow_creature = search_results["partner"]

                follow = actions.MovementToEntity(self)
                follow.set_objective(**{"target_entity": fellow_creature})

                self.action_queue.append(follow)

                mate = actions.Mate(self)
                mate.set_objective(**{"target_entity": fellow_creature})
                self.action_queue.append(mate)

                return

        find_substance = actions.SearchSubstance(self)
        find_substance.set_objective(**{"target_substance_type": type(substances.Substance())})
        search_results = find_substance.do_results()

        if search_results["accomplished"]:
            x, y = search_results["substance_x"], search_results["substance_y"]
        else:
            x = random.randint(1, self.board.length - 2)
            y = random.randint(1, self.board.height - 2)

        move = actions.MovementXY(self)
        move.set_objective(**{"target_x": x, "target_y": y})

        self.action_queue.append(move)

        if search_results["accomplished"]:
            extract_substance = actions.ExtractSubstanceXY(self)
            extract_substance.set_objective(**{"substance_x": x,
                                               "substance_y": y,
                                               "substance_type": type(substances.Substance())})
            self.action_queue.append(extract_substance)

    def die(self):
        if not self.mortal:
            return
        self.alive = False
        self.time_of_death = self.z

    def perform_action(self, action):
        results = action.do_results()

        if results["done"] or not action.action_possible():
            self.action_log.append(self.action_queue.pop(0))

        return results

    def can_mate(self, with_who):
        if isinstance(with_who, Creature):
            if with_who.sex != self.sex:

                if not self.alive or not with_who.alive:
                    return False

                if self.sex:
                    return not with_who.has_state(states.Pregnant)
                else:
                    return not self.has_state(states.Pregnant)

        return False

    def will_mate(self, with_who):
        if not self.can_mate(with_who):
            return False

        if self.sex:
            return True
        else:
            return random.choice([True, False])


class BreedingGround(Entity):
    def __init__(self):
        super(BreedingGround, self).__init__()
        self.passable = True
        self.color = "#000055"

    def __str__(self):
        return "*"

    def live(self):
        super(BreedingGround, self).live()

        if not self.board.cell_passable(self.x, self.y):
            return

        if random.random() < 0.2:
            new_creature = Creature()
            self.board.insert_object(self.x, self.y, new_creature)

    @classmethod
    def class_name(cls):
        return "Breeding ground"
