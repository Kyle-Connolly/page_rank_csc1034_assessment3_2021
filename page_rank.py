import sys
import os
import time
import argparse
from progress import Progress
# import random to randomly select a node to explore
import random

# dictionary holding all nodes and associated edges, represents the graph
network_graph = {}
# to store the number of edges in the graph
num_of_edges = 0
# to store the number of nodes in the graph
num_of_nodes = 0


# load graph by reading in from the text file and assigning each link/node (the key) and its outgoing links/edges
# (values) to a dictionary
def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapping a URL (str) to a list of target URLs (str).
    """
    # OPTIMISATION EXAMPLE 1 - set the current node to the first known node in the txt file
    # current_node = "http://www.ncl.ac.uk/computing/"

    # need to access the global variable storing the number of nodes
    global num_of_nodes
    # added the first node (current node) to the dictionary so increment the number of nodes
    num_of_nodes += 1

    # need to access the global variable storing the number of edges
    global num_of_edges
    # store the edges in a list
    edge_list = []

    # OPTIMISATION EXAMPLE 1 - set current node = None to be ready to read in first item from txt file
    current_node = None

    # iterate through the file line by line
    for line in args.datafile:
        # And split each line into two URLs
        node, target = line.split()

        # OPTIMISATION EXAMPLE 1 - if the current node is empty (None) then need to set it to first item/node it txt
        # file only runs once as current node is not null after first running
        if current_node is None:
            current_node = node

        # if current node = node then there are still edges to consider
        if current_node == node:
            # add edge to the list holding all edges
            edge_list.append(target)
            # update the number edges
            num_of_edges += 1
        # if current node != node then there aren't edges to consider, so need to move to next node
        elif current_node != node:
            # iterate over edge list, add the current_node
            network_graph[current_node] = tuple(edge_list)
            # set the current node equal to node as a new node needs to be considered
            current_node = node
            # empty list after the current node has been explored
            edge_list = []
            # update the number nodes
            num_of_nodes += 1

    return network_graph


def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    print("Number of nodes: " + str(num_of_nodes) + " " + "Number of edges: " + str(num_of_edges))


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    # dictionary to store the results of the stochastic page rank algorithm
    stochastic_rankings = {}

    # repeat n repetitions times
    for x in range(args.repeats):
        # choose a random node
        current_node = stochastic_random_val_dict(graph)
        # get outgoing links (edges) from the associated node (key) within the graph
        current_edges = graph.get(current_node)
        # obtain the number of edges (links) that the node has
        edge_num = len(current_edges)-1
        # if the user has entered a value that is different to the default number of steps use that, unless it is
        # greater than the number of edges returned above
        if args.steps <= edge_num:
            edge_num = args.steps

        # repeat n steps times:
        for i in range(edge_num):
            # current node = uniformly randomly chosen among the out edges of current_node
            current_node = stochastic_random_val_list(current_edges)

            # set hit count of current node += 1/n repetitions
            if current_node in stochastic_rankings:
                stochastic_rankings[current_node] += 1 / args.repeats
                # once it has been set move to the next node
                continue

            # Store current page and ranking value if not already
            rank = 0
            rank += 1 / len(graph)
            stochastic_rankings[current_node] = rank

    return stochastic_rankings


# given a dictionary, randomise a key to return
def stochastic_random_val_dict(nodes):
    # get a list of keys within the dictionary (graph)
    keys = list(nodes.keys())
    # randomise a node
    rand_node = random.choice(keys)
    return rand_node


# given a list, randomise a key to return
def stochastic_random_val_list(nodes):
    # randomise a node
    rand_node = random.choice(nodes)
    return rand_node


def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    # OPTIMISATION EXAMPLE 2 - dictionary to store the results of the distribution page rank algorithm
    # distribution_rankings = {}

    # store the current probability of being on each node within the graph
    distribution_node_prob = {}
    # store the current probability of being on a target node (a node's associated edges) within the graph
    distribution_next_prob = {}
    # set the initial probability to 0
    prob = 0
    # get the current
    links = list(graph.keys())

    # initialise node probability for each node = 1/(number of nodes) for all nodes
    for i in range(len(links)):
        distribution_node_prob[links[i]] = 1 / len(graph)

    # repeat n steps times:
    for j in range(args.steps):
        # for each node:
        for k in range(len(distribution_node_prob)-1):
            # get a list of keys (nodes) within the graph
            keys = list(graph.keys())

            # get the list of out edges of the current node
            out_edges = graph[keys[k]]

            # p = node prob[node] divided by its out degree
            prob += distribution_node_prob[keys[k]] / len(out_edges)

            # for each target among out edges of node:
            for x in range(len(out_edges)):
                # get the edge node at index "x"
                edge = out_edges[x]

                # set the next probability of the edge node to the probability of being on the current node
                distribution_next_prob[edge] = prob

        # get a list of keys within the dictionary of nodes that have has their probability set
        keys = list(distribution_next_prob.keys())
        # update each node's probability to the current probability in next_probability where the nodes in each match
        for p in range(len(distribution_next_prob)):
            # get the value within distribution_next_prob where the key matches that of a key within the list of
            # keys returned above
            val = distribution_next_prob[keys[p]]
            # set the value of the key to the probability within distribution_next_prob that matches that of a key
            # within the list fo keys returned above
            distribution_node_prob[keys[p]] = val

    distribution_rankings = distribution_node_prob
    return distribution_rankings


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
