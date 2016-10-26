from Cell import Cell
from Food import Food
from Predator import Predator
import matplotlib.pyplot as plt
import random
import copy

plt.ion()
plt.axis([0, 100, 0, 100])

if __name__ == '__main__':
    number_of_cells = 52
    number_of_food = 60
    number_of_predators = 10
    size_of_world = 100
    numbers_of_cycles = 10000
    max_energy = 200
    numbers_of_generations = 10000

    cells = [Cell() for i in range(number_of_cells)]  # creates the initial cells
    food = []
    predators = []
    for i in range(numbers_of_generations):

        predators = [Predator() for z in range(number_of_predators)]  # creates the initial predators

        for j in range(numbers_of_cycles):

            dead = 0

            for z in cells:
                if not z.alive:
                    dead += 1

            if dead == number_of_cells:
                break

            for k in range(number_of_food - len(food)):  # creates the needed amount of food
                food.append(Food())

            food_x = [food[z].x_pos for z in range(len(food))]
            food_y = [food[z].y_pos for z in range(len(food))]
            cell_x = []
            cell_y = []
            pred_x = [predators[z].x_pos for z in range(number_of_predators)]
            pred_y = [predators[z].y_pos for z in range(number_of_predators)]

            for z in cells:
                if z.alive:
                    cell_x.append(z.x_pos)
                    cell_y.append(z.y_pos)

            plt.clf()
            plt.scatter(food_x, food_y, color='green')
            plt.scatter(cell_x, cell_y, color='blue')
            plt.scatter(pred_x, pred_y, color='red')
            plt.draw()
            plt.pause(.0005)

            for z in predators:
                z.move(cells)

            for z in cells:
                if z.alive:
                    z.move(food, predators)

        new_cells = []

        ave_fitness = 0

        for a in cells:
            ave_fitness += a.fitness

        ave_fitness /= number_of_cells

        print("Gen: " + str(i) + " Avg: " + str(ave_fitness) )

        for a in range(13):
            first = random.randint(0, number_of_cells - 1)
            second = random.randint(0, number_of_cells - 1)
            third = random.randint(0, number_of_cells - 1)

            while second == first:
                second = random.randint(0, number_of_cells - 1)

            while third == second or third == first:
                third = random.randint(0, number_of_cells - 1)

            cell1 = cells[first]
            cell2 = cells[second]
            cell3 = cells[third]

            if cell3.fitness > cell1.fitness:
                cellT = cell3
                cell3 = cell1
                cell1 = cellT

            if cell3.fitness > cell2.fitness:
                cellT = cell3
                cell3 = cell1
                cell1 = cellT

            cell1.fitness = 0
            cell2.fitness = 0
            cell1.alive = True
            cell2.alive = True
            cell1.energy = max_energy
            cell2.energy = max_energy
            cell1.x_pos = random.uniform(0, 100)
            cell1.y_pos = random.uniform(0, 100)
            cell2.x_pos = random.uniform(0, 100)
            cell2.y_pos = random.uniform(0, 100)

            new_cells.append(cell1)
            new_cells.append(cell2)

            child1 = copy.deepcopy(cell1)
            child2 = copy.deepcopy(cell2)

            child1.mix(cell2)
            child2.mix(cell1)

            child1.x_pos = random.uniform(0, 100)
            child1.y_pos = random.uniform(0, 100)
            child2.x_pos = random.uniform(0, 100)
            child2.y_pos = random.uniform(0, 100)

            new_cells.append(child1)
            new_cells.append(child2)

        cells = new_cells








