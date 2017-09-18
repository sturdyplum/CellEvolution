import tkinter as tk
import world
from Cell import Cell

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):

        self.cellNumbers = tk.Text(self, width=38, height = 1)
        self.cellNumbers.grid()
        self.cellNumbers.insert(1.0, "Enter the number of cells")
        self.cellNumbers.config(state='disabled')

        self.cellNumbersGet = tk.Text(self, width=5, height=1)
        self.cellNumbersGet.grid()

        self.foodNumbers = tk.Text(self, width=37, height=1)
        self.foodNumbers.grid()
        self.foodNumbers.insert(1.0, "Enter the number of food")
        self.foodNumbers.config(state='disabled')

        self.foodNumbersGet = tk.Text(self, width=5, height=1)
        self.foodNumbersGet.grid()
        
        
        self.predNumbers = tk.Text(self, width=37, height=1)
        self.predNumbers.grid()
        self.predNumbers.insert(1.0, "Enter the number of predators")
        self.predNumbers.config(state='disabled')

        self.predNumbersGet = tk.Text(self, width=5, height=1)
        self.predNumbersGet.grid()
        
        self.useMemoryGet = tk.IntVar()
        self.useMemory = tk.Checkbutton(self, text="Use memory", variable=self.useMemoryGet)
        self.useMemory.grid()
        
        self.controlSpeedGet = tk.IntVar()
        self.controlSpeed = tk.Checkbutton(self, text="Cells control speed", variable=self.controlSpeedGet)
        self.controlSpeed.grid()
        

        self.quitButton = tk.Button(self, text='Quit',
                                    command=self.quit)
        self.quitButton.grid()
        self.startButton = tk.Button(self, text='Start',
                                    command=lambda : self.run_world()
                                     )
        self.startButton.grid()
    def run_world(self):
        num_cells = int(self.cellNumbersGet.get("1.0", "end-1c"))
        num_food = int(self.foodNumbersGet.get("1.0", "end-1c"))
        num_pred = int(self.predNumbersGet.get("1.0", "end-1c"))
        Cell.useMemory = self.useMemoryGet.get()
        Cell.controlSpeed = self.controlSpeedGet.get()
        
        self.cellNumbersGet.destroy()
        self.cellNumbers.destroy()
        self.foodNumbersGet.destroy()
        self.foodNumbers.destroy()
        self.useMemory.destroy()
        self.controlSpeed.destroy()
        self.predNumbersGet.destroy()
        self.predNumbers.destroy()
        self.startButton.destroy()
        self.quitButton.destroy()
        speedSlider = tk.Scale(self, from_=-15, to=15, orient=tk.HORIZONTAL, label="Speed") 
        thresholdSlider = tk.Scale(self, from_=0, to=20, orient=tk.HORIZONTAL, resolution=1, label="Threshold") 
        thresholdSlider.grid(row=0, column=0)
        shouldDraw = tk.IntVar()
        drawCheckbox = tk.Checkbutton(self, text="Draw canvas", variable=shouldDraw)
        drawCheckbox.grid(row=0, column=1)
        drawCheckbox.select()
        shouldGradient = tk.IntVar()
        gradientCheckbox = tk.Checkbutton(self, text="Draw gradient", variable=shouldGradient)
        gradientCheckbox.grid(row=0, column=2)
        
        
        
        canvas = tk.Canvas(self, width=900, height=900, borderwidth=2, highlightthickness=0, bg="#dddddd")
        canvas.grid(row=1, column=0, columnspan=2)
        canvas2 = tk.Canvas(self, width=600, height=900, borderwidth=2,  highlightthickness=0, bg="#ffffff")
        canvas2.grid(row=1, column=2, columnspan=1)

        def _create_circle(self, x, y, r, **kwargs):
            return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
        
        tk.Canvas.create_circle = _create_circle
        self.update()
        world.runWorld(number_of_cells=num_cells,number_of_food=num_food,canvas=canvas, speedSlider=speedSlider, thresholdSlider=thresholdSlider, shouldDraw=shouldDraw, number_of_preds=num_pred, shouldGradient=shouldGradient, canvas2=canvas2)



app = Application()
app.master.title('Cell Evolution')
app.mainloop()
