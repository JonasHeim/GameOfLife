import tkinter as tk
from tkinter import font
import time
import math
import random

class Application(tk.Frame):
    def __init__(self, scaling, cell_size, max_generation, verbosity, wrapping, master=None):

        self.scaling = scaling
        self.cell_size = cell_size
        self.max_generation = max_generation
        self.is_verbose = verbosity
        self.wrap = wrapping

        #Used for pausing/unpausing the simulation
        self.is_paused = False

        if self.scaling < 10:
            raise ValueError("Scaling must be greater or equal 10!")

        if self.cell_size < 1:
            raise ValueError("Cell size must be greater or equal 1!")

        '''
        Set the window size
        Always make sure, the window size is an integer multiple of the cell size,
        while trying to stay to 16x9 format
        '''
        self.window_width = 16 * self.scaling
        self.window_height = 9 * self.scaling

        #Do some rounding down if necessary, because we only want to have integer values
        if 0 != (self.window_height % self.cell_size):
            self.window_height = math.floor(self.window_height/self.cell_size)*self.cell_size

        if 0 != (self.window_width % self.cell_size):
            self.window_width = math.floor(self.window_width/self.cell_size)*self.cell_size

        self.num_cell_x = int(self.window_width/self.cell_size)
        self.num_cell_y = int(self.window_height/self.cell_size)

        #Print out dimenstions
        print(str(self.num_cell_x)+"x"+str(self.num_cell_y)+" cells with size "+str(self.cell_size))

        self.default_title = 'Game of Life Simulation ('+str(self.get_window_dimension()[0])+'x'+str(self.get_window_dimension()[1])+')'

        self.generation = 0
        tk.Frame.__init__(self, master)
        self.draw_layer = tk.Canvas(master, width=self.window_width, height=self.window_height, borderwidth=0, highlightthickness=0)

        '''
        Add keyboard bindings
        '''
        #Need to use bind_all for spacebar and return, to create a binding for the whole application
        self.draw_layer.bind_all('<space>', self.pause_simulation)
        self.draw_layer.bind_all('<Return>', self.step_simulation)

        self.draw_layer.bind('<Button-1>', self.mouse_clicked)


        self.draw_layer.pack(expand=tk.TRUE, fill=tk.BOTH)
        
        self.current_matrix = [[0 for y in range(self.num_cell_y)] for x in range(self.num_cell_x)] 
        self.next_matrix = [[0 for y in range(self.num_cell_y)] for x in range(self.num_cell_x)] 

        time_begin = time.time()

        #Create handles for cells
        for pos_x in range(self.num_cell_x):
            for pos_y in range(self.num_cell_y):
                self.next_matrix[pos_x][pos_y] = self.draw_layer.create_rectangle(pos_x*cell_size, pos_y*cell_size, pos_x*cell_size+cell_size+1, pos_y*cell_size+cell_size+1, width=0, activefill='red', fill='')
        
        if self.is_verbose:
            #Create label for FPS
            self.font_fps = font.Font(family='Times', size=10, weight='bold')
            self.label_fps = self.draw_layer.create_text(10, 10, text='FPS:\t', font=self.font_fps, fill='red', anchor=tk.NW)

        if self.is_verbose:
            #Create label for generation
            self.font_generation = font.Font(family='Times', size=10, weight='bold')
            self.label_generation = self.draw_layer.create_text(10, 20, text='Gen.:\t0', font=self.font_generation, fill='red', anchor=tk.NW)

        #Create initial glider pattern #1
        self.current_matrix[6][5] = 1
        self.current_matrix[7][6] = 1
        self.current_matrix[5][7] = 1
        self.current_matrix[6][7] = 1
        self.current_matrix[7][7] = 1

        #Create initial glider pattern #2
        self.current_matrix[11][5] = 1
        self.current_matrix[12][6] = 1
        self.current_matrix[10][7] = 1
        self.current_matrix[11][7] = 1
        self.current_matrix[12][7] = 1

        #Create initial glider pattern #3
        self.current_matrix[16][5] = 1
        self.current_matrix[17][6] = 1
        self.current_matrix[15][7] = 1
        self.current_matrix[16][7] = 1
        self.current_matrix[17][7] = 1

        #Create initial glider pattern #4
        self.current_matrix[21][5] = 1
        self.current_matrix[22][6] = 1
        self.current_matrix[20][7] = 1
        self.current_matrix[21][7] = 1
        self.current_matrix[22][7] = 1

        #Create initial glider pattern #5
        self.current_matrix[26][5] = 1
        self.current_matrix[27][6] = 1
        self.current_matrix[25][7] = 1
        self.current_matrix[26][7] = 1
        self.current_matrix[27][7] = 1

        #Bring in some randomization
        for i in range(500):
            self.current_matrix[random.randint(0, self.num_cell_x-1)][random.randint(0, self.num_cell_y-1)] = 1

        #Draw initial pattern
        for pos_x in range(self.num_cell_x):
            for pos_y in range(self.num_cell_y):
                if 1 == self.current_matrix[pos_x][pos_y]:
                    self.draw_layer.itemconfig(self.next_matrix[pos_x][pos_y], fill='black')

        time_end = time.time()

        print("Initialization of "+str(self.num_cell_x*self.num_cell_y)+" cells withing "+str(self.window_width)+"x"+str(self.window_height)+" pixels took "+str(time_end-time_begin)+" s")

        #Schedule periodic update
        self.after(1, self.update)

    def update(self, force = False):

        if self.is_paused and not force:
            return

        #Check if generation is limited
        if self.max_generation != 0:
            #Check if maximum is reached
            if self.generation == self.max_generation:
                #Maximum is reached; set window title and stop simulation
                self.set_title('TERMINATED')
                return

        #Check every cell
        time_begin = time.time()
        for pos_x in range(self.num_cell_x):
            for pos_y in range(self.num_cell_y):
                #Get living neighbours of current cell
                if self.wrap:
                    current_neighbours = self.get_living_neighbours_wrap_edges(pos_x, pos_y)
                else:
                    current_neighbours = self.get_living_neighbours_dead_edges(pos_x, pos_y)
                
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
                if 0 != self.current_matrix[pos_x][pos_y]:
                    #Cell lives
                    if (2 > current_neighbours) or (3 < current_neighbours):
                        #Cell dies
                        #Rule 2 and 4
                        self.draw_layer.itemconfig(self.next_matrix[pos_x][pos_y], fill='')
                        #print(str(pos_x)+":"+str(pos_y)+" dies - "+str(current_neighbours)+" cells alive")
                    #else:
                        #Cell stays alive, nothing to do
                        #Rule 3
                        #print(str(pos_x)+":"+str(pos_y)+" stays alive - "+str(current_neighbours)+" cells alive")
                        #self.draw_layer.itemconfig(self.current_matrix[pos_x][pos_y], fill='black') 
                else:
                    #Cell is dead
                    #Rule 1
                    if 3 == current_neighbours:
                        #Cell gets reborn
                        #print(str(pos_x)+":"+str(pos_y)+" becomes alive - "+str(current_neighbours)+" cells alive")
                        self.draw_layer.itemconfig(self.next_matrix[pos_x][pos_y], fill='black')
                    #else:
                    #     #Cell stays dead, nothing to do
                    #    print(str(pos_x)+":"+str(pos_y)+" stays dead - "+str(current_neighbours)+" cells alive")

        #Update current_matrix
        for pos_x in range(self.num_cell_x):
            for pos_y in range(self.num_cell_y):
                if '' != self.draw_layer.itemcget(self.next_matrix[pos_x][pos_y], "fill"):
                    self.current_matrix[pos_x][pos_y] = 1
                else:
                    self.current_matrix[pos_x][pos_y] = 0

        time_end = time.time()

        #print("Tick calculation took "+str(time_end-time_begin)+"s")

        if 0 != (time_end-time_begin):
            self.draw_layer.itemconfig(self.label_fps, text="FPS:\t"+str(round(1/(time_end-time_begin), 2)))
        
        #Refresh generation counter
        self.draw_layer.itemconfig(self.label_generation, text="Gen.:\t"+str(self.generation))

        self.generation += 1

        self.after(1, self.update)

    def get_living_neighbours_dead_edges(self, pos_x, pos_y):
        #Check all surrounding cells
        #We assumne that every cell behind an edge is dead
        #TL TM TR
        #LM    RM
        #BL BM BR

        retval = 0

        #TL
        #Don't check if on left edge or on top edge
        if(0 != pos_y) and (0 != pos_x):
            if 0 != self.current_matrix[pos_x-1][pos_y-1]:
                retval += 1

        #TM
        #Don't check if on top edge
        if(0 != pos_y):
            if 0 != self.current_matrix[pos_x][pos_y-1]:
                retval += 1
            
        #TR
        #Don't check if on top edge or on right edge
        if(0 != pos_y) and ((self.num_cell_x-1) != pos_x):
            if 0 != self.current_matrix[pos_x+1][pos_y-1]:
                retval += 1
            
        #LM
        #Don't check if on left edge
        if(0 != pos_x):
            if 0 != self.current_matrix[pos_x-1][pos_y]:
                retval += 1
            

        #RM
        #Don't check if on right edge
        if((self.num_cell_x-1) != pos_x):
            if 0 != self.current_matrix[pos_x+1][pos_y]:
                retval += 1

        #BL
        #Don't check if on left edge or bottom edge
        if(0 != pos_x) and ((self.num_cell_y-1) != pos_y):
            if 0 != self.current_matrix[pos_x-1][pos_y+1]:
                retval += 1

        #BM
        #Don't check if on bottom edge
        if((self.num_cell_y-1) != pos_y):
            if 0 != self.current_matrix[pos_x][pos_y+1]:
                retval += 1

        #BR
        #Don't check if on bottom edge or right edge
        if((self.num_cell_y-1) != pos_y) and ((self.num_cell_x-1) != pos_x):
            if 0 != self.current_matrix[pos_x+1][pos_y+1]:
                retval += 1

        return retval

    def get_living_neighbours_wrap_edges(self, pos_x, pos_y):
        #Check all surrounding cells
        #TL TM TR
        #LM    RM
        #BL BM BR

        retval = 0

        #TL
        if 0 == pos_x:
            #We are on left edge
            if 0 == pos_y:
                #We are on top left corner, so wrap around x and y
                if 0 != self.current_matrix[self.num_cell_x-1][self.num_cell_y-1]:
                    retval += 1
            else:
                #Simple left edge, so wrap around x
                if 0 != self.current_matrix[self.num_cell_x-1][pos_y-1]:
                    retval += 1
        elif 0 == pos_y:
            #We are on top edge, so wrap around y
            if 0 != self.current_matrix[pos_x-1][self.num_cell_y-1]:
                retval += 1
        else:
            #No edge cell
            if 0 != self.current_matrix[pos_x-1][pos_y-1]:
                retval += 1

        #TM
        #Are we on top edge
        if 0 == pos_y:
            #We are on top edge, so wrap around y
            if 0 != self.current_matrix[pos_x][self.num_cell_y-1]:
                retval += 1
        else:
            #No edge cell
            if 0 != self.current_matrix[pos_x][pos_y-1]:
                retval += 1

        #TR
        if self.num_cell_x-1 == pos_x:
            #We are on right edge
            if 0 == pos_y:
                #We are on top right corner, so wrap around x and y
                if 0 != self.current_matrix[0][self.num_cell_y-1]:
                    retval += 1
            else:
                #Simple right edge, so wrap around x
                if 0 != self.current_matrix[0][pos_y-1]:
                    retval += 1
        elif 0 == pos_y:
            #We are on top edge, so wrap around y
            if 0 != self.current_matrix[pos_x+1][self.num_cell_y-1]:
                retval += 1
        else:
            #No edge cell
            if 0 != self.current_matrix[pos_x+1][pos_y-1]:
                retval += 1

        #LM
        if 0 == pos_x:
            #We are on left edge, so wrap around x
            if 0 != self.current_matrix[self.num_cell_x-1][pos_y]:
                retval += 1
        else:
            #No edge cell
            if 0 != self.current_matrix[pos_x-1][pos_y]:
                retval += 1

        #RM
        if (self.num_cell_x-1) == pos_x:
            #We are on right edge, so wrap around x
            if 0 != self.current_matrix[0][pos_y]:
                retval += 1
        else:
            #No edge cell
            if 0 != self.current_matrix[pos_x+1][pos_y]:
                retval += 1

        #BL
        if 0 == pos_x:
            #We are on left edge
            if (self.num_cell_y-1) == pos_y:
                #We are on bottom left corner, so wrap around x and y
                if 0 != self.current_matrix[self.num_cell_x-1][0]:
                    retval += 1
            else:
                #Simple left edge, so wrap around x
                if 0 != self.current_matrix[self.num_cell_x-1][pos_y+1]:
                    retval += 1
        elif (self.num_cell_y-1) == pos_y:
            #we are on bottom edge, so wrap around y
            if 0 != self.current_matrix[pos_x-1][0]:
                retval += 1
        else:
            #No edge cell
            if 0 != self.current_matrix[pos_x-1][pos_y+1]:
                retval += 1
        
        #BM
        if (self.num_cell_y-1) == pos_y:
            #we are on bottom edge, so wrap around y
            if 0 != self.current_matrix[pos_x][0]:
                retval += 1
        else:
            #No edge cell
            if 0 != self.current_matrix[pos_x][pos_y+1]:
                retval += 1

        #BR
        if (self.num_cell_x-1) == pos_x:
            #We are on right edge
            if (self.num_cell_y-1) == pos_y:
                #we are on bottom right corner, so wrap around x and y
                if 0 != self.current_matrix[0][0]:
                    retval += 1
            else:
                #Simple right edge, so wrap around x
                if 0 != self.current_matrix[0][pos_y+1]:
                    retval += 1
        elif (self.num_cell_y-1) == pos_y:
            #We are on bottom edge, so wrap around y
            if 0 != self.current_matrix[pos_x+1][0]:
                retval += 1
        else:
            #No edge cell
            if 0 != self.current_matrix[pos_x+1][pos_y+1]:
                retval += 1

        return retval

    def get_window_dimension(self):
        return self.window_width, self.window_height

    def set_title(self, title):
        if title == "":
            self.master.title(self.default_title)
        else:
            self.master.title(title + ' - ' + self.default_title)

    def pause_simulation(self, event):
        if self.is_paused:
            self.is_paused = False
            self.set_title("")
            self.after(1, self.update)
        else:
            self.is_paused = True
            self.set_title("PAUSED")

    def step_simulation(self, event):
        #Only step if simulation is paused
        if self.is_paused:
            self.after(1, self.update, True)

    def mouse_clicked(self, event):
        #Only enable manipulation if simulation is paused
        if self.is_paused:
            self.toggle_cell(int(event.x/self.cell_size), int(event.y/self.cell_size))

    def toggle_cell(self, pos_x, pos_y):
        #Get current state of cell
        if '' != self.draw_layer.itemcget(self.next_matrix[pos_x][pos_y], "fill"):
            self.draw_layer.itemconfig(self.next_matrix[pos_x][pos_y], fill='')
        else:
            self.draw_layer.itemconfig(self.next_matrix[pos_x][pos_y], fill='black')
