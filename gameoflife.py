#!/usr/bin/python3

import tkinter as tk
import time
import math

scaling = 5
cell_size = 5 

'''
Set the window size
Always make sure, the window size is an integer multiple of the cell size,
while trying to stay to 16x9 format
'''
window_width = 16 * scaling
window_height = 9 * scaling

if 0 != (window_height % cell_size):
    window_height = math.floor(window_height/cell_size)*cell_size

if 0 != (window_width % cell_size):
    window_width = math.floor(window_width/cell_size)*cell_size

num_cell_x = int(window_width/cell_size)
num_cell_y = int(window_height/cell_size)

print(str(num_cell_x)+"x"+str(num_cell_y)+" cells with size "+str(cell_size))

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.draw_layer = tk.Canvas(master, width=window_width, height=window_height)
        self.draw_layer.pack()
        
        self.current_matrix = [[0 for y in range(num_cell_y+1)] for x in range(num_cell_x+1)] 
        self.next_matrix = [[0 for y in range(num_cell_y+1)] for x in range(num_cell_x+1)] 

        time_begin = time.time()

        for pos_x in range(num_cell_x+1):
            for pos_y in range(num_cell_y+1):
                print(str(pos_x)+"-"+str(pos_y)+" "+str(pos_x*cell_size)+"-"+str(pos_y*cell_size))
                self.current_matrix[pos_x][pos_y] = self.draw_layer.create_rectangle(pos_x*cell_size, pos_y*cell_size, cell_size+1, cell_size+1, width=0, fill='')
                self.next_matrix[pos_x][pos_y] = self.current_matrix[pos_x][pos_y]

        time_end = time.time()

        # Create initial glider pattern
        self.draw_layer.itemconfig(self.current_matrix[0][5], fill='green')
        
        print("Initialization of "+str(num_cell_x*num_cell_y)+" cells withing "+str(window_width)+"x"+str(window_height)+" pixels took "+str(time_end-time_begin)+" ms")

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
        self.draw_layer.move(self.current_matrix[0][5], 1, 1)

        self.after(200, self.update)

app = Application()
app.master.title('Game of Life Simulation '+str(window_width)+'x'+str(window_height))
app.mainloop()
