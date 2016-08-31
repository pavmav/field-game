import random


class Entity(object):
    def __init__(self):
        self.x = None
        self.y = None
        self.passable = False
        pass

    def __str__(self):
        raise Exception

    def act(self, board):
        pass


class Block(Entity):
    def __init__(self):
        super(Block, self).__init__()
        self.passable = False

    def __str__(self):
        return '#'


class Creature(Entity):
    def __init__(self):
        super(Creature, self).__init__()
        self.passable = False

    def __str__(self):
        return '@'

    def act(self, board):
        return self.wander(board)

    def move(self, x, y, board):
        if board.field[y][x].passable:
            board.insert_object(self.x, self.y, Blank())
            board.insert_object(x, y, self)
            return True
        else:
            return False

    def wander(self, board):
        possible_actions = [self.move_east, self.move_north, self.move_west, self.move_south]
        action = random.choice(possible_actions)
        return action(board)

    def move_north(self, board):
        return self.move(self.x, self.y - 1, board)

    def move_south(self, board):
        return self.move(self.x, self.y + 1, board)

    def move_east(self, board):
        return self.move(self.x + 1, self.y, board)

    def move_west(self, board):
        return self.move(self.x - 1, self.y, board)


class Blank(Entity):
    def __init__(self):
        super(Blank, self).__init__()
        self.passable = True

    def __str__(self):
        return '.'
