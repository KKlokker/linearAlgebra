"""polygon.py

Lab: Wiener Index / Polygons
------------------------------
This lab has two independent parts based on wiener.py and
polygon.py (this file). 

Hint: Start with the implementations for polygon.py, to ensure you get
most of the points with a small amount of work.

Number of point to be achieved in polygon.py : 92
Number of point to be achieved in wiener.py :   8


norm(x):                      15 
mean(x):                      15 
initPoints(num):              20 
matrixM(num):                 20 
invMatrixM(M):                10
updatePoints(M, x, y):        10
pairCS(num):                   1 (more complicated)
convEllipse(x, y):             1 (more complicated)


In this part of the lab assignment you basically have to implement
methods to allow you to visualize the series of polygons as shown and
explained in the lecture "From Random Polygon to Ellipse".  We will
provide an additional file which will use this file via an import.


Do not touch the imports in this file, and specifically, do not import
matplotlib in this file! Use the provided file linalg-ellipse.py for
visualization. The imports listed below should be enough.

The functions /docstring/s again contain some real examples and usage
of the functions. You can run these examples by executing the script
from command line:

python3 polygon.py

Note that the unit tests for the final grading may contain different
tests, and that certain requirements given below are not tested in the
tesing before the final testing.

"""

import numpy as np
import math

def norm(x):
    """
    Returns the L^2 norm of a vector x

    Parameters
    ----------
    x       : np.ndarray : a numpy array of floats

    Returns
    -------
    float   : the L^2 norm of x

    Examples
    --------
    >>> A = np.array([1.0, 2.0, 3.0, 3.0, 1.0, 1.0])
    >>> norm(A)
    5.0
    """
    sum = 0
    for n in x:
        sum += n**2
    return math.sqrt(sum)

def mean(x): 
    """
    Returns the mean of a the values of vector x

    Parameters
    ----------
    x       : np.ndarray : a numpy array of floats

    Returns
    -------
    float   : the mean of all values of vector x

    Examples
    --------
    >>> A = np.array([1.0, 2.0, 3.0, 3.0, 1.0, 1.0])
    >>> mean(A)
    1.8333333333333333
    """
    sum = 0
    for n in x:
        sum += n
    return sum/len(x)


def initPoints(num):
    """
    Randomly chose the points of the initial polygon. As described on
    the slides and in the additional material, we chose all the
    points (x_i, y_i), such that for the vector x=(x_1, ..., x_n) as
    well as y=(y_1, ..., y_n) it will hold that mean(x) = 0.0 and
    norm(x) = 1.0 (resp. mean(y) = 0.0 and norm(y) = 1.0 )

    Parameter
    ---------
    int  :  num  : the number of points of the initial polygon

    Returns
    -------
    tuple : (x,y) where x as well as y is a 1-dimensional np.ndarray of floats (length num)

    Raises
    ------
    ValueError    if num<=2

    Examples
    --------
    >>> round(norm(initPoints(5)[0]),2)
    1.0
    >>> abs(round(mean(initPoints(5)[1]),2))
    0.0
    >>> print(type(initPoints(5)))
    <class 'tuple'>
    >>> print(type(initPoints(5)[0]))
    <class 'numpy.ndarray'>
    >>> len(initPoints(5)[0])
    5
    """
    if(num <= 2):
        raise(ValueError)
    x = np.random.uniform(-10*num, 10*num, num)
    x = x-mean(x)
    x = x/norm(x)
    y = np.random.uniform(-10*num, 10*num, num)
    y = y-mean(y)
    y = y/norm(y)
    return (x,y)

def matrixM(num):
    """ 
    Returns the matrix used for the matrix vector multiplication for one iteration
    as explained on page 11 on the slide set

    Parameter
    ---------
    int  :  num  : the number of points of the initial polygon

    Returns
    -------
    2-dimensional numpy.ndarray of shape (num, num)

    Example
    -------
    matrixM(4)
    array([[ 0.5,  0.5,  0. ,  0. ],
           [ 0. ,  0.5,  0.5,  0. ],
           [ 0. ,  0. ,  0.5,  0.5],
           [ 0.5,  0. ,  0. ,  0.5]])
    """
    M = np.zeros((num,num))
    for i in range(num):
        M[i,i] = 0.5
        M[i,(i+1)%num] = 0.5
    return M

def invMatrixM(M):
    """ 
    Returns the inverse of matrix M, where M can be assumed to
    be a matrix which results from the method matrixM.

    Parameter
    ---------
    M : 2-dimensional squared numpy.ndarray 

    Returns
    -------
    a 2-dimensional squared numpy.ndarray : the inverse of matrix M

    Raises
    ------
    ValueError : if the number of rows or columns is not odd

    Example
    -------
    >>> invMatrixM(matrixM(3))
    array([[ 1., -1.,  1.],
           [ 1.,  1., -1.],
           [-1.,  1.,  1.]])
    """
    if(len(M) % 2 == 0 or len(M[0]) % 2 == 0):
        raise(ValueError)
    return np.linalg.inv(M)

def updatePoints(M, x, y):
    """
    Update the arrays x and y according to slide 15 on the slide set, i.e.,
    the the vector x (resp. y) result from a multiplication M*x and a subsequent
    normalization of the result

    Paramaters
    ----------
    M, x, y (see above definitions)

    Returns
    --------
    tuple : (newx,newy) where newx as well as newy is a 1-dimensional np.ndarray of floats 

    Raises
    ------
    ValueError : if the L2 norm of either x or y is not 1.0 (allow a small deviation of 1e-06

    Example
    -------
    >>> (x,y)=(np.array([ 0.09335276, -0.39213569,  0.45454744,  0.47834171, -0.63410622]),np.array([-0.25395211,  0.1276667 ,  0.80838746, -0.21242824, -0.46967381]))
    >>> M = matrixM(len(x))
    >>> np.around(updatePoints(M@M@M,x,y),3)
    array([[ 0.282,  0.659,  0.03 , -0.571, -0.4  ],
           [ 0.607,  0.375, -0.387, -0.585, -0.01 ]])
    """
    if(round(norm(x),6) != 1.000000 or round(norm(y),6) != 1.000000):
        raise(ValueError)

    y = M@y
    x = M@x
    x = x/norm(x)
    y = y/norm(y)
    return (x,y)

def pairCS(num):
    """ 
    Returns the vectors c and s as explained on slide 21/27 of the lecture slides
    (https://dm561.github.io/assets/DM561-RandomPolygon-2021.pdf).
    (see also page 11 in the article https://epubs.siam.org/doi/pdf/10.1137/090746707)

    Parameter
    ---------
    int  :  num  : the number of points of the initial polygon

    Returns 
    -------
    tuple : (c,s) where c as well as s are a 1-dimensional np.ndarray of floats (of length num)
    
    Raises
    ------
    ValueError    if num<=2

    Examples
    --------
    >>> np.around(pairCS(5),3)
    array([[ 0.632,  0.195, -0.512, -0.512,  0.195],
           [ 0.   ,  0.602,  0.372, -0.372, -0.602]])
    """
    if num <= 2:
        raise(ValueError)
    
    d = np.zeros(num)
    for i in range(1,num+1):
        d[i-1] = (2*(i-1)*math.pi) / num
    c = [math.cos(e)*math.sqrt(2/num) for e in d]
    s = [math.sin(e)*math.sqrt(2/num) for e in d]
    return (c,s)

def convEllipse(x, y):
    """Returns the converged ellipse-like polygon u^{(0)} and v^{(o)} as
    explained on slide 21/27 of the lecture slides
    (https://dm561.github.io/assets/DM561-RandomPolygon-2021.pdf).

    (see also page 17 in the article
    https://epubs.siam.org/doi/pdf/10.1137/090746707, but
    note that the formulas in the article have typos. The ellipse-like
    polygon is the converged polygon for even iterations, the polygon
    for odd iterations would look different)

    Parameter
    ---------
    x, y  : the x coordinates and y coorindates of the initial point set,
            both x and y are 1-dimensional np.ndarrays (the length corresponds
            to the number of initial points)
                  

    Returns 
    -------
    np.array of points where each points is a 1-dimensional np.ndarray of 
             length 2, encoding the x and y coordinate of a point of the
             converged ellipse-like polygon.
    
    Raises
    ------
    ValueError    if num<=2

    Examples
    --------
    >>> (x,y)=(np.array([ 0.09335276, -0.39213569,  0.45454744,  0.47834171, -0.63410622]),np.array([-0.25395211,  0.1276667 ,  0.80838746, -0.21242824, -0.46967381]))
    >>> np.around(convEllipse(x,y),3)
    array([[-0.618, -0.37 ],
           [-0.061,  0.374],
           [ 0.58 ,  0.601],
           [ 0.419, -0.002],
           [-0.321, -0.602]])

    """
    C,S = pairCS(len(x))
    C = np.array(C)
    S = np.array(S)
    cosAu = np.transpose(C)@x/(math.sqrt((np.transpose(C)@x)**2+(np.transpose(S)@x)**2))
    sinAu = np.transpose(S)@x/(math.sqrt((np.transpose(C)@x)**2+(np.transpose(S)@x)**2))
    u = cosAu*C + sinAu*S
    cosAv = np.transpose(C)@y/(math.sqrt((np.transpose(C)@y)**2+(np.transpose(S)@y)**2))
    sinAv = np.transpose(S)@y/(math.sqrt((np.transpose(C)@y)**2+(np.transpose(S)@y)**2))
    v = cosAv*C + sinAv*S
    return np.column_stack((u,v))



if __name__ == "__main__":
    import doctest
    (x,y)=(np.array([ 0.09335276, -0.39213569,  0.45454744,  0.47834171, -0.63410622]),np.array([-0.25395211,  0.1276667 ,  0.80838746, -0.21242824, -0.46967381]))
    result = np.around(convEllipse(x,y),3).tolist()
    print(result)
