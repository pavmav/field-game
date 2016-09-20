# -*- coding: utf-8 -*-

import random
import actions
import substances


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

        # visualization properties
        self.color = "#004400"

    def __str__(self):
        raise Exception

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
        if substance_index == None:
            return None
        return self._container.pop(substance_index)

    def pocket(self, substance_object):
        if substance_object is not None:
            self._container.append(substance_object)

    def live(self):
        self.z += 1
        self.age += 1

    def dissolve(self):
        self.board.remove_object(self)

    @classmethod
    def class_name(cls):
        return "Entity"


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

        if random.random() <= 0.0005:
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
        self.color = "#550000"

    def __str__(self):
        return '@'

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

            current_results = current_action.do_results()

            if current_results["done"] or not current_action.action_possible():
                self.action_log.append(self.action_queue.pop(0))
            #
            # else:
            #
            #     self.action_log.append(self.action_queue.pop(0))

    def plan(self):
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
        self.alive = False
        self.time_of_death = self.z

    def need_to_update_plan(self):
        return len(self.action_queue) == 0

    def queue_action(self, action, objectives={}, index=None):
        if index is None:
            self.action_queue.append({"action": action, "objectives": objectives})
        else:
            self.action_queue.insert(index, {"action": action, "objectives": objectives})

    def perform_current_action(self):
        if len(self.action_queue) == 0:
            return

        current_queue_action = self.action_queue.pop(0)

        action_to_do = current_queue_action["action"]
        objectives = current_queue_action["objectives"]

        if objectives is None:
            if action_to_do.get_objective() is None:
                pass  # no objectives to set - move to log   TODO get_objective must return None if no valid objectives
            else:
                pass  # objectives are set, OK to perform
        elif isinstance(objectives, dict):
            # set objectives from queue
            action_to_do.set_objective(**objectives)
        elif isinstance(objectives, actions.Action):
            # set objectives of objective action's result
            action_to_do.set_objective(**objectives.results)
        else:
            raise ValueError()  # objectives should be None, dict or Action

        # TODO perform action, move to log

        current_queue_action.do()

        if current_queue_action.results["done"]:
            self.action_log.append(current_queue_action)

    @classmethod
    def class_name(cls):
        return "Creature"


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

        if random.random() < 0.05:
            new_creature = Creature()
            self.board.insert_object(self.x, self.y, new_creature)

    @classmethod
    def class_name(cls):
        return "Breeding ground"
