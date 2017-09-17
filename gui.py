import tkinter as tk
import world

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
        use_memory = self.useMemoryGet.get()
        self.cellNumbersGet.destroy()
        self.cellNumbers.destroy()
        self.foodNumbersGet.destroy()
        self.foodNumbers.destroy()
        self.useMemory.destroy()
        self.predNumbersGet.destroy()
        self.predNumbers.destroy()
        self.startButton.destroy()
        self.quitButton.destroy()
        speedSlider = tk.Scale(self, from_=-15, to=15, orient=tk.HORIZONTAL, label="Speed") 
        thresholdSlider = tk.Scale(self, from_=0, to=20, orient=tk.HORIZONTAL, resolution=1, label="Threshold") 
        thresholdSlider.grid()
        shouldDraw = tk.IntVar()
        drawCheckbox = tk.Checkbutton(self, text="Draw canvas", variable=shouldDraw)
        drawCheckbox.grid()
        
        
        
        canvas = tk.Canvas(self, width=900, height=900, borderwidth=2, highlightthickness=0, bg="white")
        canvas.grid()

        def _create_circle(self, x, y, r, **kwargs):
            return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
        
        tk.Canvas.create_circle = _create_circle
        self.update()
        world.runWorld(number_of_cells=num_cells,number_of_food=num_food,canvas=canvas, speedSlider=speedSlider, thresholdSlider=thresholdSlider, shouldDraw=shouldDraw, number_of_preds=num_pred, use_memory=use_memory)



app = Application()
app.master.title('Cell Evolution')
app.mainloop()
