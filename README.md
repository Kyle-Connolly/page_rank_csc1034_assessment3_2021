# csc1034_project3_2021

Code Optimisation Report:
-------------------------
I considered using functions to complete common tasks such as returning a list of keys
within a dictionary, however I came to the conclusion that this would result in the same time for
output since the same task was being completed, or if not longer as a call to the function would
have to be made first.

I also considered using Dijkstra's algorithm to find the page rank, after 
evaluating it I concluded that it would result in the same output time if not longer, as the
requirement to access the graph (dictionary) and carry out associated operations would result in
the same constant access time as the original page rank algorithms.

Instead of hard coding a value to be the first current node (the first link within the txt file)
I opted to change the load_graph function to read in the first item from any txt file. This
resulted in a slightly faster time for the stochastic page rank algorithm with 14.92 seconds, versus the previous time 
of around 15
seconds on average. See optimisation example 1 in the code comments within page_rank.py.

In order to optimise my code, I aimed to delete as much duplicated code or unnecessary operations as possible, as this 
reduces the amount of instructions the interpreter has to go through therefore improving/speeding up execution of the 
program. In some cases, this involved deleting variables that where assigned later on and so had no use at a specific 
point before it was utilised in the algorithm. This had little affect on both page algorithms, resulting in the same 
times for the output. See optimisation example 2 in the code comments within page_rank.py.