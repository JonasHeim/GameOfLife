#!/usr/bin/python3

import tkinter as tk
import time
import math
import random

scaling = 50
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
        self.draw_layer = tk.Canvas(master, width=window_width, height=window_height, borderwidth=0, highlightthickness=0)
        self.draw_layer.pack(expand=tk.TRUE, fill=tk.BOTH)
        
        self.current_matrix = [[0 for y in range(num_cell_y)] for x in range(num_cell_x)] 
        self.next_matrix = [[0 for y in range(num_cell_y)] for x in range(num_cell_x)] 

        time_begin = time.time()

        for pos_x in range(num_cell_x):
            for pos_y in range(num_cell_y):
                self.current_matrix[pos_x][pos_y] = self.draw_layer.create_rectangle(pos_x*cell_size, pos_y*cell_size, pos_x*cell_size+cell_size+1, pos_y*cell_size+cell_size+1, width=0, fill='')
                self.next_matrix[pos_x][pos_y] = self.current_matrix[pos_x][pos_y]

        time_end = time.time()
        
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

        #Color table
        color_table = ['red', 'black', 'green', 'blue']

        for i in range(10):
            rand_pos_x = random.randint(0, num_cell_x-1)
            rand_pos_y = random.randint(0, num_cell_y-1)
            rand_color = random.randint(0, len(color_table)-1)

            self.draw_layer.itemconfig(self.current_matrix[rand_pos_x][rand_pos_y], fill=color_table[rand_color])
        
        self.after(1, self.update)

    def get_neighbours(self, pos_x, pos_y):
        # Check the four corners at first
        if(0 == pos_x) and (0 == pos_y):
            #Top left corner
            print("Top left corner")
        elif (num_cell_x == pos_x) and (0 == pos_y):
            #Top right corner
            print("Top right corner")
        elif(0 == pos_x) and (num_cell_y == pos_y):
            #Bottom left corner
            print("Bottom left corner")
        elif(num_cel_x == pos_x) and (num_cell_y == pos_y):
            #Bottom right corner
            print("Bottom right corner")
        else:
            print("No corner")

app = Application()
app.master.title('Game of Life Simulation '+str(window_width)+'x'+str(window_height))
app.mainloop()
