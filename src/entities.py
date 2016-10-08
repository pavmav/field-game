# -*- coding: utf-8 -*-

import random
import actions
import substances
import math
import states
import brain
from sklearn.externals import joblib
import numpy as np
import pandas


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

    def count_substance_of_type(self, type_of_substance):
        num = 0
        for element in self._container:
            if isinstance(element, type_of_substance):
                num += 1

        return num


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

        if random.random() <= 0.0004:
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
        self.private_learning_memory = brain.LearningMemory(self)
        self.public_memory = None

        self.decision_model = joblib.load("mating_model/dt_model")

        # TODO
        self.children = 0

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

            self.perform_action_save_memory(current_action)

            while len(self.action_queue) > 0 and self.action_queue[0].instant:
                current_action = self.action_queue[0]

                self.perform_action_save_memory(current_action)

        # if self.age % 40 == 0:
        self.update_decision_model()

    def set_sex(self, sex):
        self.sex = sex
        if self.sex:
            self.color = "#550000"
        else:
            self.color = "#990000"

    def need_to_update_plan(self):
        return len(self.action_queue) == 0

    def plan(self):

        if self.sex:

            find_partner = actions.SearchMatingPartner(self)

            search_results = find_partner.do_results()

            if search_results["accomplished"]:

                features = [float(self.age),
                            float(self.has_state(states.NotTheRightMood)),
                            float(actions.SearchMatingPartner(self).do_results()["partner"].count_substance_of_type(
                                    substances.Substance)),
                            float(self.count_substance_of_type(substances.Substance))]

                features = np.asarray(features)

                features = features.reshape(1, -1)

                if self.decision_model.predict(features):
                    go_mating = actions.GoMating(self)
                    self.queue_action(go_mating)
                    return
                else:
                    harvest_substance = actions.HarvestSubstance(self)
                    harvest_substance.set_objective(**{"target_substance_type": type(substances.Substance())})
                    self.queue_action(harvest_substance)
                    return


                # return TODO Clever planning

        harvest_substance = actions.HarvestSubstance(self)
        harvest_substance.set_objective(**{"target_substance_type": type(substances.Substance())})
        self.queue_action(harvest_substance)

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

    def perform_action_save_memory(self, action):
        if isinstance(action, actions.GoMating):
            results = self.perform_action(action)
            if results["done"]:
                self.private_learning_memory.save_results(results, action)
                self.public_memory.save_results(results, action)
            return results
        else:
            return self.perform_action(action)

    def queue_action(self, action):
        if isinstance(action, actions.GoMating):
            features = {"age": float(self.age),
                        "self_num_substance": float(self.count_substance_of_type(substances.Substance)),
                        "partner_num_substance": float(
                            actions.SearchMatingPartner(self).do_results()["partner"].count_substance_of_type(
                                substances.Substance)),
                        "not_in_mood": float(self.has_state(states.NotTheRightMood))}

            self.private_learning_memory.save_state(features, action)
            self.public_memory.save_state(features, action)

        self.action_queue.append(action)

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
            if self.has_state(states.NotTheRightMood):
                return False
            return True
        else:
            self_has_substance = self.count_substance_of_type(substances.Substance)
            partner_has_substance = with_who.count_substance_of_type(substances.Substance)
            if self_has_substance + partner_has_substance == 0:
                return False
            if self_has_substance <= partner_has_substance:
                return True
            else:
                return random.random() < 1. * partner_has_substance / (self_has_substance*3 + partner_has_substance)

    def update_decision_model(self):
        table_list_of_dicts = self.private_learning_memory.make_table(actions.GoMating)
        df_train = pandas.DataFrame.from_dict(*[table_list_of_dicts])
        if len(df_train) > 5:
            # df_train.drop(df_train.columns[0], axis=1, inplace=True)
            y_train = df_train.pop('target')
            X_train = df_train
            # print X_train
            self.decision_model.fit(X_train, y_train)
            self.private_learning_memory = brain.LearningMemory(self)

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
