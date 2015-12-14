# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph.
# Each building will be a node, edges represent a path between adjacent locations
# and will contain the distance traveled and the distance travelled outside. Edges will
# be directional and stored in a dictionary with each key being the node name and each
# value being the list of edges that originate at that node. Nodes will be stored as a
# set of strings that is a field of the weighted digraph.

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."

    g = WeightedDigraph()

    file = open(mapFilename,'r')
    raw_data = file.read()
    lines = raw_data.splitlines()
    file.close()


    for n in xrange(len(lines)):
        #break each string representing an edge into a list of form ['src', 'dest', totalDistance, outdoorsDistance]
        lines[n] = lines[n].split()
        #convert the source and destination field to Node objects
        lines[n][0] = Node(lines[n][0])
        lines[n][1] = Node(lines[n][1])
        #convert the total distance and outdoors distance of each entry from strings to ints
        lines[n][2] = int(lines[n][2])
        lines[n][3] = int(lines[n][3])

    #Process each file entry and add to graph
    for line in lines:
        if not g.hasNode(line[0]):
            g.addNode(Node(line[0]))
        if not g.hasNode(line[1]):
            g.addNode(Node(line[1]))
        g.addEdge(WeightedEdge(line[0], line[1], line[2], line[3]))
    return g

        

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#
def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors, path=[], shortest=None):

    path = bruteForceSearchEngine(digraph, start, end, maxTotalDist, maxDistOutdoors, path=[], shortest=None)

    # if pathTotalDist(digraph,path) > maxTotalDist:
    #     raise ValueError('Total Distance > Max Allowed, Total Distance = ' + str(pathTotalDist(digraph,path)))
    # if pathOutdoorDist(digraph,path) > maxDistOutdoors:
    #     raise ValueError('Outdoor Distance > Max Allowed, Outdoor Distance =  ' + str(pathOutdoorDist(digraph,path)))

    if path == None:
        raise ValueError("No Valid Path Found")
    for node in range(len(path)):
        path[node]=str(path[node])


    return path

def pathTotalDist(digraph,path):
    totalDist = 0

    for n in range(len(path)-1):
        currentNode = path[n]
        nextNode = path[n+1]
        for edge in digraph.edges[currentNode]:
            if edge[0] == nextNode:
                totalDist += edge[1][0]
    return totalDist

def pathOutdoorDist(digraph,path):
    outdoorsDist = 0

    for n in range(len(path)-1):
        currentNode = path[n]
        nextNode = path[n+1]
        for edge in digraph.edges[currentNode]:
            if edge[0] == nextNode:
                outdoorsDist += edge[1][1]
    return outdoorsDist



def bruteForceSearchEngine(digraph, start, end, maxTotalDist, maxDistOutdoors, path = [], shortest = None):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    start = Node(start)
    end = Node(end)
    path = path + [start]

    #print 'Current dfs path:' + str(path)
    if start == end and pathOutdoorDist(digraph,path) <= maxDistOutdoors and pathTotalDist(digraph,path) <= maxTotalDist:
        return path
    #elif start == end:
        #print 'path rejected due to constraints'
    for node in digraph.childrenOf(start):
        #print 'checking children of ' + str(start) + '. children should be ' + str(digraph.childrenOf(start))
        if node not in path: # Avoid cycles
            #print 'checking ' + str(node)
            #Check against max distance constraints
            if (pathOutdoorDist(digraph, path) <= maxDistOutdoors and
                pathTotalDist(digraph,path) <= maxTotalDist and shortest is None):

                newPath = bruteForceSearchEngine(digraph, node, end, maxTotalDist, maxDistOutdoors, path, shortest)
                if newPath is not None:
                    shortest = newPath

            elif (pathOutdoorDist(digraph,path) <= maxDistOutdoors and
                  pathTotalDist(digraph,path) <= maxTotalDist and
                  pathTotalDist(digraph,path) < pathTotalDist(digraph,shortest)):

                newPath = bruteForceSearchEngine(digraph,node, end, maxTotalDist, maxDistOutdoors, path, shortest)
                if newPath is not None and (pathTotalDist(digraph, newPath) < pathTotalDist(digraph,shortest)):
                    shortest = newPath
            #else:
                #print 'node rejected because of constraints. Path total distance ' + str(pathTotalDist(digraph,path)) + 'shortest total distance ' + str(pathTotalDist(digraph, shortest))

    return shortest

# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    path = bruteForceSearchEngine(digraph, start, end, maxTotalDist, maxDistOutdoors, path=[], shortest=None)

    # if pathTotalDist(digraph,path) > maxTotalDist:
    #     raise ValueError('Total Distance > Max Allowed, Total Distance = ' + str(pathTotalDist(digraph,path)))
    # if pathOutdoorDist(digraph,path) > maxDistOutdoors:
    #     raise ValueError('Outdoor Distance > Max Allowed, Outdoor Distance =  ' + str(pathOutdoorDist(digraph,path)))

    if path == None:
        raise ValueError("No Valid Path Found")
    for node in range(len(path)):
        path[node]=str(path[node])


    return path


#mitMap = load_map("mit_map.txt")
#
#
# edges = mitMap.edges
#
# print edges



# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
    #Test cases
    mitMap = load_map("mit_map.txt")
    print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges


    LARGE_DIST = 1000000

    #Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    #dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    #print "DFS: ", dfsPath1
    #print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
#     dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
#     print "DFS: ", dfsPath2
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

# #     Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
#     print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
#    print "DFS: ", dfsPath6
#    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
#    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    # try:
    #     directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
    # except ValueError:
    #     dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
#    print "Did DFS search raise an error?", dfsRaisedErr

#    Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
#    try:
#        directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
#    except ValueError:
#        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
#    print "Did DFS search raise an error?", dfsRaisedErr
