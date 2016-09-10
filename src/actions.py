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

        self.x_increment = None
        self.y_increment = None
        self.straight = None

        # y = a + bx
        self.a = None
        self.b = None

    def set_xy(self, x, y):
        self.target_x = x
        self.target_y = y

    def initialize_equation(self):
        self.x_increment = 0
        self.y_increment = 0

        y_direction = self.target_y - self.subject.y
        x_direction = self.target_x - self.subject.x

        if y_direction > 0:
            self.y_increment = 1
        elif y_direction < 0:
            self.y_increment = -1

        if x_direction > 0:
            self.x_increment = 1
        elif x_direction < 0:
            self.x_increment = -1

        if self.x_increment == 0 or self.y_increment == 0:
            self.straight = True
        else:
            self.straight = False

            x1, y1 = float(self.subject.x), float(self.subject.y)
            x2, y2 = float(self.target_x), float(self.target_y)

            self.b = (y2 - y1) / (x2 - x1)
            self.a = y1 - (self.b * x1)

    def do(self):
        self.check_set_accomplishment()
        if self.accomplished:
            return True

        if self.straight is None \
                or (self.subject.x == self.target_x or self.subject.y == self.target_y):
            self.initialize_equation()

        if self.straight:
            current_step_x = self.subject.x + self.x_increment
            current_step_y = self.subject.y + self.y_increment
        else:
            y = self.a + (self.b * (self.subject.x + self.x_increment))

            if abs(self.subject.y) <= y <= (abs(self.subject.y) + 1):
                current_step_x = self.subject.x + self.x_increment
                current_step_y = self.subject.y
            else:
                current_step_x = self.subject.x
                current_step_y = self.subject.y + self.y_increment

        if self.subject.board.field[current_step_y][current_step_x][-1].passable:
            self.subject.board.field[self.subject.y][self.subject.x].pop()
            self.subject.board.insert_object(current_step_x, current_step_y, self.subject, epoch=1)

        self.check_set_accomplishment()

        return self.accomplished

    def check_set_accomplishment(self):
        self.accomplished = (self.subject.x == self.target_x and self.subject.y == self.target_y)
