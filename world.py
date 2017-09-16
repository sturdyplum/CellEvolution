from Cell import Cell
from Food import Food
import random
import time

def runWorld(number_of_cells, number_of_food, canvas):
    size_of_world = 900
    cells = [Cell() for i in range(number_of_cells)]  # creates the initial cells
    food = []

    for k in range(number_of_food - len(food)):  # creates the needed amount of food
        food.append(Food())

    j = 0
    while j < 100000000:
        j += 1
        canvas.delete("all")
        while len(food) < number_of_food:
            food.append(Food())

        # Get rid of the cells that are dead
        for cell in cells:
            if not cell.alive:
                cells.remove(cell)

        cells.sort(key=lambda x: x.fitness, reverse=False)

        # If all cells are dead, add three new random cells
        if len(cells) == 0:
            cells.append(Cell())
            cells.append(Cell())
            cells.append(Cell())

        # Repopulate the population by cross breeding cells that are currently alive
        while len(cells) < number_of_cells:
            first = random.randint(int(2 * len(cells) / 3), len(cells) - 1)
            second = random.randint(int(2 * len(cells)/ 3), len(cells)- 1)
            cells.append(cells[first].mix(cells[second]))


        spec = Cell()
        replaced = False
        for z in cells:
            if z.alive:
                if(z.fitness > spec.fitness):
                    spec = z
                    replaced = True

        if j % 1000 == 0:
            print(str(j) + " " + str(spec.fitness))
        if j > 50000:
            for f in food:
                canvas.create_circle(f.x_pos, f.y_pos, 4, fill = "green")

            for c in cells:
                canvas.create_circle(c.x_pos, c.y_pos, 4, fill = "blue")

            if replaced:
                canvas.create_circle(spec.x_pos, spec.y_pos, 4, fill = "red")
            canvas.update()
        for z in cells:
            if z.alive:
                z.single_cycle(food)
