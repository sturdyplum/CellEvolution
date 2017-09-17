from Cell import Cell
from Food import Food
import random
import time

def randomCell(cells):
    totalFitness = 0
    for cell in cells:
        totalFitness += cell.fitness
    if random.randint(1,100) <= 3 or (totalFitness < 3 and random.randint(1,100) <= 10):
        return Cell()
    if totalFitness < len(cells)/5:
        return cells[random.randint(int(2 * len(cells) / 3), len(cells) - 1)]
    countDone = 0
    ran = random.randint(1, totalFitness)
    for cell in cells:
        countDone += cell.fitness
        if ran <= countDone:
            return cell
    return
    
def runWorld(number_of_cells, number_of_food, canvas, speedSlider, thresholdSlider):
    size_of_world = 900
    cells = [Cell() for i in range(number_of_cells)]  # creates the initial cells
    food = []

    for k in range(number_of_food - len(food)):  # creates the needed amount of food
        food.append(Food())

    j = 0
    while j < 100000000:
        j += 1
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
            first = randomCell(cells)
            second = randomCell(cells)
            while first == second:
                second = randomCell(cells)
            cells.append(first.mix(second))

        totalFitness = 0
        for cell in cells:
            totalFitness += cell.fitness

        spec = Cell()
        replaced = False
        for z in cells:
            if z.alive:
                if(z.fitness > spec.fitness):
                    spec = z
                    replaced = True

        if j % 1000 == 0:
            print(str(j) + " " + str(spec.fitness) + " " + str(totalFitness))
        if j > 40000 or j % 1000 == 0:
            canvas.delete("all")
            for f in food:
                canvas.create_rectangle(f.x_pos-3, f.y_pos-3, f.x_pos+3, f.y_pos+3, fill = "black")

            for c in cells:
                if c.fitness >= thresholdSlider.get():
                    canvas.create_circle(c.x_pos, c.y_pos, 6, fill = '#%02x%02x%02x' % (c.color[0], c.color[1], c.color[2]))
                    canvas.create_text(c.x_pos-4,c.y_pos-13, text='%d / %d' % (c.energy, c.fitness))

            if replaced:
                canvas.create_circle(spec.x_pos, spec.y_pos, 2, fill = "red")
            canvas.update()
        for z in cells:
            if z.alive:
                z.single_cycle(food, pow(1.05,speedSlider.get()))
