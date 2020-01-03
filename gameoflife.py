#!/usr/bin/python3

from application import Application
import argparse

'''
Obviously main function
'''
def main():

    #Get command line options
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--scaling', dest='scaling', type=int, default=10, help="Set the scaling of the simulation (is multiplied by ration 16:9).")
    parser.add_argument('-c', '--cellsize', dest='cell_size', type=int, default=1, help="Set the size of a cell in pixel.")
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbosity', default=False, help="Enable additional information of simulation such as fps and generation counter.")
    parser.add_argument('-m', '--maxgeneration', dest='max_generation', type=int, default=0, help="Set the generation when to stop the simulation. Set to 0 (default if omitted) to run to infinity and beyond...")
    parser.add_argument('-w', '--wrap', action='store_true', dest='wrap', default=False, help="Wraps the edges of the Canvas area both in X- and Y- direction. Assumes that all cells out of the canvas borders are dead if ommited.")

    args = parser.parse_args()

    #Start simulation
    app = Application(scaling=args.scaling, cell_size=args.cell_size, max_generation=args.max_generation, verbosity=args.verbosity, wrapping=args.wrap)
    app.master.iconbitmap('./images/Glider.ico')
    app.mainloop()

if __name__ == "__main__":
    main()