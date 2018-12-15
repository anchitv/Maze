# Maze
Code written as part of COMP9021


The code performs the following tasks :- 

* analyse the various characteristics of a maze, represented by a particular coding of its basic constituents into numbers stored in a file whose contents is read, and
* - either display those characteristics
  - or output some Latex code in a file, from which a pictorial representation of the maze can be
produced.


The representation of the maze is based on a coding with the four digits 0, 1, 2 and 3 such that

* 0 codes points that are connected to neither their right nor below neighbours.
* 1 codes points that are connected to their right neighbours but not to their below ones.
* 2 codes points that are connected to their below neighbours but not to their right ones.
* 3 codes points that are connected to both their right and below neighbours.


A point that is connected to none of their left, right, above and below neighbours represents a pillar.
