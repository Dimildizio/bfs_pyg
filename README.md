# bfs_pyg


Requires pygame

bfs_grid.py - example of Breadth first pathfinding algorithm

bfs_grid_settings.py - settings file to tinker with

everything is scallable with the TILE variable in bfs_grid_settings


Other:

bfs_simple.py - example of bfs. Does not require pygame

dijxstra.py - example of Dijkstra algorithm

astar.py - example of A* algorithm

LocationGraph.py is a part of a large code from a tile turn-based graphic rpg that is being refactored now. useless without other modules and assets




controls for bfs.grid.py:

    left mouse button click: set a destination point for pathfinding at mouse position

    right mouse button click: add or remove an obstacle at mouse position

    middle mouse button click: set the starting position for pathfinding at mouse position

    hold right mouse button: add wall at mouse position

    space pressed: clear map from obstacles

    g pressed: turn grid lines on/off
