# -*- coding: utf-8 -*-

class Need(object):
    def __init__(self, subject, importance=1):
        self.subject = subject
        self._importance = importance

    def set_importance(self, importance):
        self._importance = importance

    @property
    def importance(self):
        return self._importance

    def get_satisfaction(self):
        satisfaction = 1

        # some code here

        return satisfaction * self._importance
