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

    def set_xy(self, x, y):
        self.target_x = x
        self.target_y = y

    def do(self):
        # super(MovementXY, self).do()
        if self.subject.board.field[self.target_y][self.target_x][-1].passable:
            self.subject.board.field[self.subject.y][self.subject.x].pop()
            self.subject.board.insert_object(self.target_x, self.target_y, self.subject, epoch=1)

        self.check_set_accomplishment()

        return self.accomplished

    def check_set_accomplishment(self):
        self.accomplished = (self.subject.x == self.target_x and self.subject.y == self.target_y)