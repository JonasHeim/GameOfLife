#!/usr/bin/python3

import tkinter as tk
import time

scaling = 20

window_height = 9 * scaling
window_width = 16 * scaling


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.draw_layer = tk.Canvas(master, width=window_width, height=window_height)
        self.draw_layer.pack()
        
        self.current_matrix = [[0 for x in range(window_height)] for y in range(window_width)] 
        self.next_matrix = [[0 for x in range(window_height)] for y in range(window_width)] 

        time_begin = time.time()

        for i in range(window_width):
            for j in range(window_height):
                self.current_matrix[i][j] = self.draw_layer.create_rectangle(i, j, i+1, j+1, outline='')
                self.next_matrix[i][j] = self.current_matrix[i][j]

        time_end = time.time()

        # Create initial glider pattern
        self.draw_layer.itemconfig(self.current_matrix[6][5], outline='black')
        self.draw_layer.itemconfig(self.current_matrix[7][6], outline='black')
        self.draw_layer.itemconfig(self.current_matrix[5][7], outline='black')
        self.draw_layer.itemconfig(self.current_matrix[6][7], outline='black')
        self.draw_layer.itemconfig(self.current_matrix[7][7], outline='black')
        

        print("Initialization of "+str(window_width)+"x"+str(window_height)+" took "+str(time_end-time_begin)+" ms")

        self.after(20, self.update)

    def update(self):
        for i in range(window_width):
            for j in range(window_height):
                '''
                    1. Rule
                        A dead cell is reborn, if it has exact three alive neighours
                    2. Rule
                        A living cell with less than two living neighbours will die
                    3. Rule
                        A living cell with exact two or three living neighbours will stay alive
                    4. Rule
                        A living cell with more than threee living neighbours will die
                '''
                if self.current_matrix                

        self.after(20, self.update)

    def get_neighbours(self):
        

app = Application()
app.master.title('Game of Life Simulation '+str(window_width)+'x'+str(window_height))
app.mainloop()
