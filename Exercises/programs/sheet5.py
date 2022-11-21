import numpy as np
def itersolve(A, epsilon=0.85, maxiter=100, tol=1e-12):
    
    """Compute the PageRank vector using the iterative method.

    Parameters:
        epsilon (float): the damping factor, between 0 and 1.
        maxiter (int): the maximum number of iterations to compute.
        tol (float): the convergence tolerance.

    Return:
        dict(str -> float): A dictionary mapping labels to PageRank values.
    """
    A = A.astype("float64")
    for column in A.T:
        column /= sum(column)
    A_hat = A

    x = A
    for t in range(maxiter):
        xn = (epsilon*A_hat+(1-epsilon)*(np.ones((len(A_hat),len(A_hat)))*1/len(A_hat)).T) @ x
        xn = xn/(len(xn)**2)
        if len(xn-x) < tol:
            break
        x = xn
    norm =  x[:,0] / sum(x[:,0])
    return norm

def ex1():
    A = np.array([
        [1,0,0,0.5,0,0],
        [0,0,1,0.5,1/3,0.5],
        [0,1,0,0,0,0],
        [0,0,0,0,1/3,0],
        [0,0,0,0,0,0.5],
        [0,0,0,0,1/3,0]])
    v,w = np.linalg.eig(A);    
    print(itersolve(A,maxiter=50))


if __name__ == "__main__":
    ex1()
