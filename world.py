from Cell import Cell
from Food import Food
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
import matplotlib.pyplot as plt
import random
import time
import copy

multi = False

class Runner(object):
    def __init__(self, food,preds, j):
        self.food=food
        self.preds=preds
        self.j=j

    def __call__(self, z):
        if(z.alive):
             z.single_cycle(self.food, self.preds, self.j)

def randomCell(cells, isPred):
    totalFitness = 0
    for cell in cells:
        totalFitness += cell.fitness
    if random.randint(1,100) <= 3 or (totalFitness < 3 and random.randint(1,100) <= 10):
        return Cell(isPred)
    if totalFitness < len(cells)/5:
        return cells[random.randint(int(2 * len(cells) / 3), len(cells) - 1)]
    countDone = 0
    ran = random.randint(1, totalFitness)
    for cell in cells:
        countDone += cell.fitness
        if ran <= countDone:
            return cell
    return

def repopulate(cells, number_of_cells, isPred):
    # Get rid of the cells that are dead
    for cell in cells:
        if not cell.alive:
            cells.remove(cell)
    cells.sort(key=lambda x: x.fitness, reverse=False)

    # If all cells are dead, add three new random cells
    if len(cells) == 0:
        while len(cells) < 3 and len(cells) < number_of_cells:
            cells.append(Cell(isPred))
    # Repopulate the population by cross breeding cells that are currently alive
    while len(cells) < number_of_cells:
        first = randomCell(cells, isPred)
        second = randomCell(cells, isPred)
        while first == second:
            second = randomCell(cells, isPred)
        cells.append(first.mix(second))

def runWorld(number_of_cells, number_of_food, number_of_preds, canvas, speedSlider, thresholdSlider, shouldDraw, shouldGradient):
    Cell.useSecondary = number_of_preds > 0
        
    size_of_world = 900
    cells = [Cell(0) for i in range(number_of_cells)]  # creates the initial cells
    preds = [Cell(1) for i in range(number_of_preds)]
    food = []
    best = []
    avg = []

    for k in range(number_of_food - len(food)):  # creates the needed amount of food
        food.append(Food())

    j = 0
    while j < 100000000:
        j += 1
        while len(food) < number_of_food:
            food.append(Food())

        repopulate(cells, number_of_cells, 0)
        repopulate(preds, number_of_preds, 1)
        
        totalFitness = 0
        for cell in cells:
            totalFitness += cell.fitness

        spec = Cell(0)
        replaced = False
        for z in cells:
            if z.alive:
                if(z.fitness > spec.fitness):
                    spec = z
                    replaced = True

        if j % 1000 == 0:
            print(str(j) + " " + str(spec.fitness) + " " + str(totalFitness))
            best.append(spec.fitness)
            avg.append(totalFitness/number_of_cells)
            plt.plot(best,'g')
            plt.plot(avg,'r')
            plt.savefig('stats.svg')
            canvas.update()
        if shouldDraw.get() == 1:
            canvas.delete("all")
            if shouldGradient.get():
                bestCopy = Cell(0)
                bestCopy.nn = copy.deepcopy(spec.nn)
                for x in range(0, 900, 50):
                    for y in range(0, 900, 50):
                        bestCopy.direction = 0
                        bestCopy.x_pos = x
                        bestCopy.y_pos = y
                        for i in range(1,10):
                            tmpX = bestCopy.x_pos
                            tmpY = bestCopy.y_pos
                            bestCopy.make_move(food, preds)
                            canvas.create_line(tmpX,tmpY,bestCopy.x_pos,bestCopy.y_pos)
            for f in food:
                canvas.create_rectangle(f.x_pos-3, f.y_pos-3, f.x_pos+3, f.y_pos+3, fill = "black")

            for c in cells:
                if c.fitness >= thresholdSlider.get():
                    canvas.create_circle(c.x_pos, c.y_pos, 6, fill = '#%02x%02x%02x' % (c.color[0], c.color[1], c.color[2]))
                    canvas.create_text(c.x_pos-7,c.y_pos-13, text='%de / %df / %.1fs' % (c.energy, c.fitness, c.speed))
            for c in preds:
                canvas.create_circle(c.x_pos, c.y_pos, 6, fill = 'black')

            if replaced:
                canvas.create_circle(spec.x_pos, spec.y_pos, 2, fill = "red")
            canvas.update()
        if multi:
            pool = ThreadPool()
            pool.map(Runner(food,preds,j),cells)
            pool.close()
            pool.join()
        if not multi:    
            for z in cells:
               if z.alive:
                  z.single_cycle(food, preds, j)
        for z in preds:
            if z.alive:
                z.single_cycle(cells, food, j)
