from Cell import Cell
from Predator import Predator
from Food import Food
from random import randint
import matplotlib.pyplot as plt

num_cells = 100 #int(input("How many cells do we start with?\n")) (not all values for this work at the moment so be carefull
x_world = 100#int(input("How long is the world\n")) size of world
num_predator = 8 #int(input("How many predators do we have?\n"))
num_food = 300#int(input("How much food per tick?\n"))
food_energy = 100 #int(input("How much energy per food?\n"))
max_energy = 200# int(input("Max Energy?\n"))
cycles = 1000#int(input("How many cycles per generation?\n"))
generations = 1000#int(input("How many generations?\n"))

cells = []
preds = []
averages = []

for a in range(0, num_cells): #create initial cells
    x = randint(0, x_world)
    y = randint(0, x_world)
    cell = Cell(0, 0, x, y, max_energy, max_energy, False, False)
    cells.append(cell)


for a in range(0, generations):
    foods = []
    for b in range(0, num_predator):#create predators for this generation
        x = randint(0, x_world)
        y = randint(0, x_world)
        pred = Predator(x, y)
        preds.append(pred)
    for b in range(0, cycles):
        for f in range(len(foods), num_food):#resupply food
            x = randint(0, x_world)
            y = randint(0, x_world)
            food = Food(x, y, food_energy)
            foods.append(food)
        for c in cells:
            if not c.dead:
                c.make_move_and_eat(x_world, preds, foods)#make cells move
        for p in preds:
            p.move(cells)#make predators move
    cells.sort(key=lambda z: z.rounds, reverse=False)#sort cells by how long they lived
    preds = []
    newCells = []
    ans = 0
    for z in cells:
        ans += z.rounds
    print(str(a) + "  " +str(ans/len(cells)) + "   " + str(cells[len(cells)-1].rounds))
    averages.append(ans/len(cells))
    for i in range(int(num_cells/2), num_cells, 2): #mate the top 50% with each other and discard bottom 50%
        cells[i].energy = max_energy
        cells[i+1].energy = max_energy
        cells[i].rounds = 0
        cells[i+1].rounds = 0
        cells[i].dead = False
        cells[i+1].dead = False
        newCells.append(cells[i])
        newCells.append(cells[i+1])
        x = randint(0, x_world)
        y = randint(0, x_world)
        child1 = Cell(cells[i], cells[i+1], x, y, max_energy, max_energy, True, False)#make first child
        x = randint(0, x_world)
        y = randint(0, x_world)
        child2 = Cell(cells[i], cells[i+1], x, y, max_energy, max_energy, True, False)#make second child
        newCells.append(child1)
        newCells.append(child2)
    cells = newCells



plt.plot(averages) #plot progress
plt.ylabel('Round Average')
plt.xlabel('Generation')
plt.show()




