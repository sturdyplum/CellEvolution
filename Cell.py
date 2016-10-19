from NeuralNetwork import NeuralNetwork


class Cell:

    def __init__(self, parent1, parent2, x_pos=-1, y_pos=-1, start_energy=-1, max_energy=-1, is_child=False, is_shell=True):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.energy = start_energy
        self.max_energy = max_energy
        self.rounds = 0
        if not is_shell:
            if is_child:
                self.net = NeuralNetwork(17, 8, 5, parent1, parent2, is_child)#python doesnt let me make multiple constructers so this is a hacky work around should fix this later
            else:
                self.net = NeuralNetwork(17, 8, 5, 0, 0, is_child)
        self.dead = False

    def eat_food(self, food_energy):
        self.energy = min(self.max_energy, self.energy+food_energy)

    def move(self, world_x, world_y, preds, foods):
        inp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]#generates the input for the neural network
        # index 0 = predator right, 1 = predaor above, 2 = predator left, 3 = predator down (0 if no 1 if yes)
        # index 4 = food right, 5 = food above, 6 = food left, 7 = food down (0 if no 1 if yes)
        # index 8-11 distances from predators right, up, left, down (distance/max distance to normalize)
        # index 11-15 distances from food right, up, left, down (distance/max distance to normalize)
        # index 16 current energy/ max energy

        dist_up = 1000000
        dist_down = 1000000
        dist_left = 1000000
        dist_right = 1000000
        inp[16] = self.energy/200 ##change this along with max en

        for p in preds:#finds predators **make this more efficent later**
            if p.x_pos == self.x_pos:
                if p.x_pos > self.x_pos:
                    dist_right = min(dist_right, abs(p.x_pos-self.x_pos))
                    inp[0] = 1
                else:
                    dist_left = min(dist_left, abs(p.x_pos-self.x_pos))
                    inp[2] = 1
            if p.y_pos == self.y_pos:
                if p.y_pos > self.y_pos:
                    dist_up = min(dist_up, abs(p.y_pos - self.y_pos))
                    inp[1] = 1
                else:
                    dist_down = min(dist_down, abs(p.y_pos - self.y_pos))
                    inp[3] = 1

        for p in foods:#finds food **make this more efficent later**
            if p.x_pos == self.x_pos:
                if p.x_pos > self.x_pos:
                    if inp[0] == 1:
                        continue
                    dist_right = min(dist_right, abs(p.x_pos - self.x_pos))
                    inp[4] = 1
                else:
                    if inp[1] == 1:
                        continue
                    dist_left = min(dist_left, abs(p.x_pos - self.x_pos))
                    inp[5] = 1
            if p.y_pos == self.y_pos:
                if p.y_pos > self.y_pos:
                    if inp[2] == 1:
                        continue
                    dist_up = min(dist_up, abs(p.y_pos - self.y_pos))
                    inp[6] = 1
                else:
                    if inp[3] == 1:
                        continue
                    dist_down = min(dist_down, abs(p.y_pos - self.y_pos))
                    inp[7] = 1

        if dist_up != 1000000:
            if inp[1] == 1:
                inp[9] = dist_up/world_y
            else:
                inp[13] = dist_up/world_y

        if dist_right != 1000000:
            if inp[0] == 1:
                inp[8] = dist_up / world_y
            else:
                inp[12] = dist_up / world_y

        if dist_left != 1000000:
            if inp[2] == 1:
                inp[10] = dist_up / world_y
            else:
                inp[14] = dist_up / world_y

        if dist_down != 1000000:
            if inp[3] == 1:
                inp[11] = dist_up / world_y
            else:
                inp[15] = dist_up / world_y

        moves = self.net.query(inp)

        if max(moves) == moves[0]:
            return 0
        if max(moves) == moves[1]:
            return 1
        if max(moves) == moves[2]:
            return 2
        if max(moves) == moves[3]:
            return 3
        if max(moves) == moves[4]:
            return 4

    def make_move(self, world_x, world_y, preds, foods):#gets the move from the neural network and makes it if valid
        move = self.move(world_x, world_y, preds, foods)#neural network returns 0 = up, 1 = right, 2 = down, 3 = left, 4 = stand still
        if move == 0 and self.y_pos + 1 < world_y:
            self.y_pos += 1
            return
        if move == 1 and self.x_pos + 1 < world_x:
            self.x_pos += 1
            return
        if move == 2 and self.y_pos > 0:
            self.y_pos -= 1
            return
        if move == 3 and self.x_pos > 0:
            self.x_pos -= 1
            return
        if move == 4:
            return
        if self.y_pos + 1 < world_y:
            self.y_pos += 1
            return
        if self.x_pos + 1 < world_x:
            self.x_pos += 1
            return
        if self.y_pos > 0:
            self.y_pos -= 1
            return
        if self.x_pos > 0:
            self.x_pos -= 1
            return

    def make_move_and_eat(self, world_x, preds, foods):
        self.make_move(world_x, world_x, preds, foods)
        for a in foods:#checks to see if standing on food and eats it if so
            if self.y_pos == a.y_pos and self.x_pos == a.x_pos:
                self.eat_food(a.energy)
                foods.remove(a)
                return
        self.rounds += 1
        self.energy -= 1
        if self.energy < 0:
            self.dead = True

