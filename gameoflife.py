#!/usr/bin/python3

import tkinter as tk
from tkinter import font
import time
import math
import random

scaling = 50
cell_size = 10

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

        #Create handles for cells
        for pos_x in range(num_cell_x):
            for pos_y in range(num_cell_y):
                self.current_matrix[pos_x][pos_y] = self.draw_layer.create_rectangle(pos_x*cell_size, pos_y*cell_size, pos_x*cell_size+cell_size+1, pos_y*cell_size+cell_size+1, width=0, fill='')

        time_end = time.time()
        
        #Create label for FPS
        self.font_fps = font.Font(family='Times', size=10, weight='bold')
        self.label_fps = self.draw_layer.create_text(10, 10, text='0', font=self.font_fps, fill='blue')

        #Create initial glider pattern
        self.draw_layer.itemconfig(self.current_matrix[6][5], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[7][6], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[5][7], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[6][7], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[7][7], fill='black')


        print("Initialization of "+str(num_cell_x*num_cell_y)+" cells withing "+str(window_width)+"x"+str(window_height)+" pixels took "+str(time_end-time_begin)+" s")

        self.after(2000, self.update)

    def update(self):
        #Check every cell
        #TODO
        time_begin = time.time()
        for pos_x in range(num_cell_x):
            for pos_y in range(num_cell_y):
                '''
                    1. Rule
                        A dead cell is reborn, if it has exact three alive neighours
                    2. Rule
                        A living cell with less than two living neighbours will die
                    3. Rule
                        A living cell with exact two or three living neighbours will stay alive
                    4. Rule
                        A living cell with more than three living neighbours will die
                '''

                current_neighbours = self.get_living_neighbours(pos_x, pos_y)
                if 0 != current_neighbours:
                    print("X: "+str(pos_x)+" Y: "+str(pos_y)+" - "+str(current_neighbours)+" living cells")

                if (3 == current_neighbours) or (2 == current_neighbours):
                    #Cell is reborn/stays alive
                    self.next_matrix[pos_x][pos_y] = 1
                elif (2 > current_neighbours) or (3 < current_neighbours):
                    #Cell will die
                    self.next_matrix[pos_x][pos_y] = 0

        #Set pixel according to rules
        for pos_x in range(num_cell_x):
            for pos_y in range(num_cell_y):
                if 1 == self.next_matrix[pos_x][pos_y]:
                    self.draw_layer.itemconfig(self.current_matrix[pos_x][pos_y], fill='black')
                else:
                    self.draw_layer.itemconfig(self.current_matrix[pos_x][pos_y], fill='')
                #Reset next matrix
                self.next_matrix[pos_x][pos_y] = 0

        time_end = time.time()

        self.draw_layer.itemconfig(self.label_fps, text=str(math.floor(1/(time_end-time_begin))))
        
        self.after(1, self.update)

    def get_living_neighbours(self, pos_x, pos_y):
        #Check all surrounding cells
        #TL TM TR
        #LM    RM
        #BL BM BR

        retval = 0

        #TL
        #Don't check if on left edge or on top edge
        if(0 != pos_y) and (0 != pos_x):
            if "" != self.draw_layer.itemcget(self.current_matrix[pos_x-1][pos_y-1], "fill"):
                retval += 1

        #TM
        #Don't check if on top edge
        if(0 != pos_y):
            if "" != self.draw_layer.itemcget(self.current_matrix[pos_x][pos_y-1], "fill"):
                retval += 1
            
        #TR
        #Don't check if on top edge or on right edge
        if(0 != pos_y) and ((num_cell_x-1) != pos_x):
            if "" != self.draw_layer.itemcget(self.current_matrix[pos_x+1][pos_y-1], "fill"):
                retval += 1
            
        #LM
        #Don't check if on left edge
        if(0 != pos_x):
            if "" != self.draw_layer.itemcget(self.current_matrix[pos_x-1][pos_y], "fill"):
                retval += 1
            

        #RM
        #Don't check if on right edge
        if((num_cell_x-1) != pos_x):
            if "" != self.draw_layer.itemcget(self.current_matrix[pos_x+1][pos_y], "fill"):
                retval += 1

        #BL
        #Don't check if on left edge or bottom edge
        if(0 != pos_x) and ((num_cell_y-1) != pos_y):
            if "" != self.draw_layer.itemcget(self.current_matrix[pos_x-1][pos_y+1], "fill"):
                retval += 1

        #BM
        #Don't check if on bottom edge
        if((num_cell_y-1) != pos_y):
            if "" != self.draw_layer.itemcget(self.current_matrix[pos_x][pos_y+1], "fill"):
                retval += 1

        #BR
        #Don't check if on bottom edge or right edge
        if((num_cell_y-1) != pos_y) and ((num_cell_x-1) != pos_x):
            if "" != self.draw_layer.itemcget(self.current_matrix[pos_x+1][pos_y+1], "fill"):
                retval += 1

        return retval
try:    
    app = Application()
    app.master.title('Game of Life Simulation '+str(window_width)+'x'+str(window_height))
    app.mainloop()
except KeyboardInterrupt:
    print("Exiting...")
    app.destroy()
