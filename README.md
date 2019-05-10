# Conways Game of Life

Python reference implementation for [Conways Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
Drawing is done using a simple Canvas widget of the TKinter module.

The drawing area can be scaled (16x9) as well as the size of the single cells (squared cells).

It supports both interpreting the outer area (not within the Canvas) as constant dead cells or wrapping around edges by selecting which function for neighbour determination is used within the Canvas' update tick.

* ``get_living_neighbours_wrap_edges``

Wraps the edges of the Canvas area both in X- and Y- direction

* ``get_living_neighbours_dead_edges``

Assumes that all cells out of the canvas borders are dead. Might lead to abnormal behaviour of known figures (such as a glider).