# Detecting communities in network
Implements the Girvan-Newman algorithm and outputs the resultant hierarchical decomposition of the network and evaluating the optimal structure by computing the modularity of each decomposition.

* * *

## Pre-requisites
```
pip install numpy
pip install networkx
```
* * *
## Input file
The input file should be in `.txt` format
* The first line contains the number of nodes
* The remaining lines contain the adjacency matrix

* * *
## Running the program
```
python3 girvan.py [input file]
```
Here's the example:
```
python3 girvan.py input.txt
```

* * *
## Output
The output is divided into two parts.
1. The first part outputs the hierarchical decomposition produced by the Girvan-Newman algorithm, in the following format:
```
network decomposition
([0, 1, 2, 3], [4, 5, 6, 7], [8])
([0], [1], [2], [3], [4], [5], [6], [7], [8])
```

2.  The second part outputs the modularity results, in the following format:
```
3 clusters : modularity 0.4209
9 clusters : modularity -0.1148
optimal structure :  ([0, 1, 2, 3], [4, 5, 6, 7], [8])
```

* * *
## Program Detail
There are 7 functions implemented in `girvan.py`
* `get_input()` - to read the input file
* `girvan()`- the framework of Girvan-Newman
* `bfs()` - counting the number of shortest paths and calculating the node flow in the order of BFS traversal.
* `cal_betweenness()` - repeating the BFS procedure for each starting node in the network to calculate the betweenness of edges.
* `remove_edges()` - to remove the edges which have the highest betweenness
* `cal_moduality()`- calculating the modularity of the clusters.
* `ans_output()` - to show the result on the screen and produce a output.txt file

* * *
## Author
* Kuang Bingran - Initial work
