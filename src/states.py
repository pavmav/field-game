# -*- coding: utf-8 -*-

import actions

class State(object):
    def __init__(self, subject):

        self.subject = subject
        self.duration = 0

    def affect(self):
        self.duration += 1

class Pregnant(State):
    def __init__(self, subject):
        super(Pregnant, self).__init__(subject)

        self.timing = 15

    def affect(self):
        super(Pregnant, self).affect()

        if self.duration == self.timing:
            self.subject.action_queue.insert(0, actions.GiveBirth(self.subject, self))

