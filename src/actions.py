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
        self.check_set_accomplishment()
        if self.accomplished:
            return True

        # TODO rethink movement
        y_direction = self.target_y - self.subject.y
        x_direction = self.target_x - self.subject.x

        if abs(x_direction) > abs(y_direction):
            current_step_x = self.subject.x + (x_direction / abs(x_direction))
            current_step_y = self.subject.y
        else:
            current_step_x = self.subject.x
            current_step_y = self.subject.y + (y_direction / abs(y_direction))

        if self.subject.board.field[current_step_y][current_step_x][-1].passable:
            self.subject.board.field[self.subject.y][self.subject.x].pop()
            self.subject.board.insert_object(current_step_x, current_step_y, self.subject, epoch=1)

        self.check_set_accomplishment()

        return self.accomplished

    def check_set_accomplishment(self):
        self.accomplished = (self.subject.x == self.target_x and self.subject.y == self.target_y)