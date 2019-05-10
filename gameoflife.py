#!/usr/bin/python3

import tkinter as tk
from tkinter import font
import time
import math
import random

scaling = 75
cell_size = 20

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
        self.label_fps = self.draw_layer.create_text(20, 10, text='0', font=self.font_fps, fill='red')

        #Create initial glider pattern #1
        self.draw_layer.itemconfig(self.current_matrix[6][5], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[7][6], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[5][7], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[6][7], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[7][7], fill='black')

        #Create initial glider pattern #2
        self.draw_layer.itemconfig(self.current_matrix[11][5], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[12][6], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[10][7], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[11][7], fill='black')
        self.draw_layer.itemconfig(self.current_matrix[12][7], fill='black')


        print("Initialization of "+str(num_cell_x*num_cell_y)+" cells withing "+str(window_width)+"x"+str(window_height)+" pixels took "+str(time_end-time_begin)+" s")

        self.after(200, self.update)

    def update(self):
        #Check every cell
        time_begin = time.time()
        for pos_x in range(num_cell_x):
            for pos_y in range(num_cell_y):
                #Get living neighbours of current cell
                current_neighbours = self.get_living_neighbours(pos_x, pos_y)
                
                ''' Game rules
                
                    1. Rule
                        A dead cell is reborn, if it has exact three alive neighours
                    2. Rule
                        A living cell with less than two living neighbours will die
                    3. Rule
                        A living cell with exact two or three living neighbours will stay alive
                    4. Rule
                        A living cell with more than three living neighbours will die
                '''
                if '' != self.draw_layer.itemcget(self.current_matrix[pos_x][pos_y], "fill"):
                    #Cell lives
                    if (2 > current_neighbours) or (3 < current_neighbours):
                        #Cell dies
                        #Rule 2 and 4
                        self.next_matrix[pos_x][pos_y] = 0
                        #print(str(pos_x)+":"+str(pos_y)+" dies - "+str(current_neighbours)+" cells alive")
                    else:
                        #Cell stays alive
                        #Rule 3
                        self.next_matrix[pos_x][pos_y] = 1
                        #print(str(pos_x)+":"+str(pos_y)+" stays alive - "+str(current_neighbours)+" cells alive")
                else:
                    #Cell is dead
                    #Rule 1
                    if 3 == current_neighbours:
                        #Cell gets reborn
                        self.next_matrix[pos_x][pos_y] = 1
                        #print(str(pos_x)+":"+str(pos_y)+" becomes alive - "+str(current_neighbours)+" cells alive")
                    # else:
                    #     #Cell stays dead
                    #     print(str(pos_x)+":"+str(pos_y)+" stays dead - "+str(current_neighbours)+" cells alive")

        #Set pixel according to rules
        for pos_x in range(num_cell_x):
            for pos_y in range(num_cell_y):
                if 1 == self.next_matrix[pos_x][pos_y]:
                    self.draw_layer.itemconfig(self.current_matrix[pos_x][pos_y], fill='black')

                    #Reset next matrix
                    self.next_matrix[pos_x][pos_y] = 0
                else:
                    self.draw_layer.itemconfig(self.current_matrix[pos_x][pos_y], fill='')
                

        time_end = time.time()

        self.draw_layer.itemconfig(self.label_fps, text=str(math.floor(1/(time_end-time_begin)))+"fps")
        
        self.after(1, self.update)

    def get_living_neighbours(self, pos_x, pos_y):
        #Check all surrounding cells
        #We assumne that every cell behind an edge is dead
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
