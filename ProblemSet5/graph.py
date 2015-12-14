# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

class WeightedDigraph(Digraph):
    """
    A digraph containing Nodes and WeightedEdges
    """
    def __init__(self):
        Digraph.__init__(self)

    def addEdge(self, wEdge):
        src = wEdge.getSource()
        dest = wEdge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest,(int(wEdge.getTotalDistance()), int(wEdge.getOutdoorDistance()))])
        #self.edges[src].append(wEdge)
    def childrenOf(self, node):
        res = []
        for edge in self.edges[node]:
            res.append(edge[0])
        return res

    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2} {3}\n'.format(res, k, d[0],(float(d[1][0]),float(d[1][1])))
                #res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

class WeightedEdge(Edge):
    """
    An edge representing a path between two adjacent buildings
    the total distance of the path and the distance outside are
    contained as weight values
    """


    def __init__(self,src,dest,totalDist,outdoorDist):
        Edge.__init__(self,src,dest)
        if outdoorDist > totalDist:
            raise ValueError('Total Distance must be greater than Outdoor Distance')
        else:
            self.totalDistance = totalDist
            self.outdoorDistance = outdoorDist

    def getTotalDistance(self):
        return self.totalDistance

    def getOutdoorDistance(self):
        return self.outdoorDistance

    def __str__(self):
        return '{0}->{1} {2}'.format(self.src, self.dest,(self.getTotalDistance(),self.getOutdoorDistance()))




#Test Code

# nh = Node('h')
# nj = Node('j')
# nk = Node('k')
# nm = Node('m')
# ng = Node('g')
# g = WeightedDigraph()
# g.addNode(nh)
# g.addNode(nj)
# g.addNode(nk)
# g.addNode(nm)
# g.addNode(ng)
# randomEdge = WeightedEdge(nj, nm, 52, 16)
# g.addEdge(randomEdge)
# randomEdge = WeightedEdge(nm, nk, 40, 20)
# g.addEdge(randomEdge)
# randomEdge = WeightedEdge(nh, nk, 84, 72)
# g.addEdge(randomEdge)
# randomEdge = WeightedEdge(nj, nm, 91, 73)
# g.addEdge(randomEdge)
# randomEdge = WeightedEdge(nj, nk, 73, 11)
# g.addEdge(randomEdge)
# randomEdge = WeightedEdge(nm, nj, 45, 8)
# g.addEdge(randomEdge)
# randomEdge = WeightedEdge(nj, nh, 43, 26)
# g.addEdge(randomEdge)
# randomEdge = WeightedEdge(nj, nm, 53, 11)
# g.addEdge(randomEdge)
# print g.childrenOf(nh)

# nx = Node('x')
# ny = Node('y')
# nz = Node('z')
# e1 = WeightedEdge(nx, ny, 18, 8)
# e2 = WeightedEdge(ny, nz, 20, 1)
# e3 = WeightedEdge(nz, nx, 7, 6)
# g = WeightedDigraph()
# g.addNode(nx)
# g.addNode(ny)
# g.addNode(nz)
# g.addEdge(e1)
# g.addEdge(e2)
# g.addEdge(e3)
# print g

# nx = Node('x')
# ny = Node('y')
# nz = Node('z')
# e1 = WeightedEdge(nx, ny, 18, 8)
# e2 = WeightedEdge(ny, nz, 20, 1)
# e3 = WeightedEdge(nz, nx, 7, 6)
# g = WeightedDigraph()
# g.addNode(nx)
# g.addNode(ny)
# g.addNode(nz)
# g.addEdge(e1)
# g.addEdge(e2)
# g.addEdge(e3)
# print g