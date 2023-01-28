import numpy as np
from numpy import linalg as la


np.set_printoptions(precision=3)



class DiGraph:
    """A class for representing directed graphs via their adjacency matrices.

    Attributes:
        (fill this out after completing DiGraph.__init__().)
    """
    # Problem 1
    def __init__(self, A, labels=None):
        """Modify A so that there are no sinks in the corresponding graph,
        then calculate Ahat. Save Ahat and the labels as attributes.

        Parameters:
            A ((n,n) ndarray): the adjacency matrix of a directed graph.
                A[i,j] is the weight of the edge from node j to node i.
            labels (list(str)): labels for the n nodes in the graph.
                If None, defaults to [0, 1, ..., n-1].                

        Examples
        ========
        >>> A = np.array([[0, 0, 0, 0],[1, 0, 1, 0],[1, 0, 0, 1],[1, 0, 1, 0]])
        >>> G = DiGraph(A, labels=['a','b','c','d'])
        >>> G.A_hat
        array([[0.   , 0.25 , 0.   , 0.   ],
               [0.333, 0.25 , 0.5  , 0.   ],
               [0.333, 0.25 , 0.   , 1.   ],
               [0.333, 0.25 , 0.5  , 0.   ]])
        >>> steady_state_1 = G.linsolve()
        >>> { k: round(steady_state_1[k],3) for k in steady_state_1}
        {'a': 0.096, 'b': 0.274, 'c': 0.356, 'd': 0.274}
        >>> steady_state_2 = G.eigensolve()
        >>> { k: round(steady_state_2[k],3) for k in steady_state_2}
        {'a': 0.096, 'b': 0.274, 'c': 0.356, 'd': 0.274}
        >>> steady_state_3 = G.itersolve()
        >>> { k: round(steady_state_3[k],3) for k in steady_state_3}
        {'a': 0.096, 'b': 0.274, 'c': 0.356, 'd': 0.274}
        >>> get_ranks(steady_state_3)
        ['c', 'b', 'd', 'a']
        """
        for i in range(len(A[:])):
            if sum(A[:,i]) == 0:
                A[:,i] = 1
        A = A.astype("float64")
        for column in A.T:
            column /= sum(column)
        self.A_hat = A
        if labels == None:
            self.labels = [range(len(A))]
        elif len(labels) == len(A):
            self.labels = labels
        else:
            raise(ValueError())


    def linsolve(self, epsilon=0.85):
        """Compute the PageRank vector using the linear system method.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.

        Returns:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        leftside = np.identity(len(self.A_hat))-epsilon*self.A_hat
        rightside = np.ones((len(self.A_hat),1))*(1-epsilon)/len(self.A_hat)*1
        res = np.linalg.solve(leftside, rightside)
        return {self.labels[i]: res[i][0] for i in range(len(res))}

    def eigensolve(self, epsilon=0.85):
        """Compute the PageRank vector using the eigenvalue method.
        Normalize the resulting eigenvector so its entries sum to 1.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.

        Return:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        A_line = epsilon*self.A_hat + (np.ones((len(self.A_hat),len(self.A_hat)))*(1-epsilon)/len(self.A_hat)).T
        w, v = np.linalg.eig(A_line)
        norm =  v[:,0] / sum(v[:,0])
        return {self.labels[i]: norm[i] for i in range(len(norm))}


    def itersolve(self, epsilon=0.85, maxiter=100, tol=1e-12):
        """Compute the PageRank vector using the iterative method.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.
            maxiter (int): the maximum number of iterations to compute.
            tol (float): the convergence tolerance.

        Return:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        x = np.ones((len(self.A_hat), 1)) / len(self.A_hat)
        for t in range(maxiter):
            xn = (epsilon*self.A_hat+(1-epsilon)*(np.ones((len(self.A_hat),len(self.A_hat)))*1/len(self.A_hat)).T) @ x
            xn = xn/(len(xn)**2)
            if len(xn-x) < tol:
                break
            x = xn
        norm =  x[:,0] / sum(x[:,0])
        return {self.labels[i]: norm[i] for i in range(len(norm))}

def get_ranks(d):
    """Construct a sorted list of labels based on the PageRank vector.

    Parameters:
        d (dict(str -> float)): a dictionary mapping labels to PageRank values.

    Returns:
        (list) the keys of d, sorted by PageRank value from greatest to least.
    """    
    res = [key for key, val in sorted(d.items(), key= lambda item: item[1], reverse=True)]
    return res

# Task 2
def rank_websites(filename="web_stanford.txt", epsilon=0.85):
    """Read the specified file and construct a graph where node j points to
    node i if webpage j has a hyperlink to webpage i. Use the DiGraph class
    and its itersolve() method to compute the PageRank values of the webpages,
    then rank them with get_ranks().

    Each line of the file has the format
        a/b/c/d/e/f...
    meaning the webpage with ID 'a' has hyperlinks to the webpages with IDs
    'b', 'c', 'd', and so on.

    Parameters:
        filename (str): the file to read from.
        epsilon (float): the damping factor, between 0 and 1.

    Returns:
        (list(str)): The ranked list of webpage IDs.

    Examples
    ========
    >>> print(rank_websites()[0:5])
    ['98595', '32791', '28392', '77323', '92715']
    """
    #Create dict for node index to name
    file = open(filename,"r")
    nodeDict = {}
    lines = file.readlines()
    labels =[]
    for i in range(len(lines)):
        nodes = lines[i].replace('\n','')
        nodes = nodes.replace(' ','')
        for node in nodes.split("/"):
            if node not in nodeDict:
                nodeDict[node] = len(labels)
                labels.append(node)
    A = np.zeros((len(labels), len(labels)))
    for line in lines:
        line = line.replace('\n','')
        line = line.replace(' ','')
        nodes = line.split("/")
        for i in range(1,len(nodes)):
            A[nodeDict.get(nodes[i]),nodeDict.get(nodes[0])] = 1
    file.close()
    G = DiGraph(A,labels)
    solve = G.eigensolve()
    res = {key: val for key, val in sorted(solve.items(), key= lambda item: item[0],reverse=True)}
    return get_ranks(res)

# Task 3
def rank_uefa_teams(filename, epsilon=0.85):
    """Read the specified file and construct a graph where node j points to
    node i with weight w if team j was defeated by team i in w games. Use the
    DiGraph class and its itersolve() method to compute the PageRank values of
    the teams, then rank them with get_ranks().

    Each line of the file has the format
        A,B
    meaning team A defeated team B.

    Parameters:
        filename (str): the name of the data file to read.
        epsilon (float): the damping factor, between 0 and 1.

    Returns:
        (list(str)): The ranked list of team names.

    Examples
    ========
    >>> rank_uefa_teams("psh-uefa-2018-2019.csv",0.85)[0:5]
    ['Liverpool', 'Ath Madrid', 'Paris SG', 'Genk', 'Barcelona']
    """
    file = open(filename,"r")
    teamDict = {}
    lines = file.readlines()
    labels =[]
    for line in lines:
        teams = line.split(",")
        for i in range(2):
            if teams[i] not in teamDict:
                teamDict[teams[i]] = len(labels)
                labels.append(teams[i])
    
    A = np.zeros((len(labels), len(labels)))
    for line in lines:
        nodes = line.split(",")
        if nodes[2] < nodes[3].replace("\n", ""):
            A[teamDict.get(nodes[1]),teamDict.get(nodes[0])] += 1
        elif nodes[2] > nodes[3].replace("\n", ""):
            A[teamDict.get(nodes[0]),teamDict.get(nodes[1])] += 1

    file.close()
    G = DiGraph(A,labels)
    solve = G.eigensolve(epsilon=epsilon)
    res = {key: val for key, val in sorted(solve.items(), key= lambda item: item[0],reverse=False)}
    return get_ranks(res)
    






if __name__ == "__main__":
    import doctest
    doctest.testmod()
