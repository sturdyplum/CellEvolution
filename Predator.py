from Cell import Cell


class Predator:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def closest(self, cells):
        closest = 1000000
        closest_cell = Cell(0, 0, 0, 0, 0, 0, True, True)
        for a in cells:
            if a.dead:
                continue
            if abs(a.x_pos-self.x_pos)+abs(a.y_pos-self.y_pos) < closest:
                closest = abs(a.x_pos-self.x_pos)+abs(a.y_pos-self.y_pos)
                closest_cell = a
        return closest_cell

    def move(self, cells):#finds closest cell to it moves towards it I could make this like a billion time more efficent but I dont feel like it and since there tends to be a low amount of predators it wont help too much
        closest_cell = self.closest(cells)
        if closest_cell.x_pos == -1:
            return
        if self.x_pos != closest_cell.x_pos:
            if closest_cell.x_pos > self.x_pos:
                self.x_pos += 1
            else:
                self.x_pos -= 1
        else:
            if closest_cell.y_pos > self.y_pos:
                self.y_pos += 1
            else:
                self.y_pos -= 1
        if self.x_pos == closest_cell.x_pos and self.y_pos == closest_cell.y_pos:
            closest_cell.dead = True
