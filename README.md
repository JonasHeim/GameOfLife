# Conways Game of Life

Python reference implementation for [Conways Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
Drawing is done using a simple Canvas widget of the TKinter module.

The drawing area can be scaled (16x9) as well as the size of the single cells (squared cells).
It supports both interpreting the outer area (not within the Canvas) as constant dead cells or wrapping around edges by selecting which `get_living_neighbours_...` function is used within a simulation tick.