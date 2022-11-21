from matplotlib import pyplot as plt
import numpy as np
import scipy.linalg as la


def ex1():
    #[bias (1), x, x^2]
    A = np.array([[1,5,25],[1,7,49],[1,9,81],[1,4,16]])
    #[bias, x1, x2, x1x2]
    A = np.array([[1,1,1,1],[1,6,5,30],[1,7,6,42],[1,7,7,49]])

def ex2(A,b):
    Q, R = np.linalg.qr(A)
    rightside = Q.T @ b
    solution = la.solve_triangular(R,rightside)
    return solution

def ex5():
    A = np.load("housing.npy")
    plt.plot(A) 
    test = np.column_stack((np.ones((len(A),1)), A[:,[0]]))
    x = np.linspace(0,30) 
    result = ex2(test ,A[:,[1]])
    y = result[0][0]+x*result[1][0]
    plt.plot(x,y)
    plt.show()

def ex6():
    A = np.load("housing.npy")
    x = A[:,[0]]
    y = A[:,[1]]
    a_0 = len(x)
    a_1 = sum(x)
    a_2 = sum(x**2)
    a_3 = sum(x**3)
    b_0 = sum(y)
    a_4 = sum(x**4)
    b_1 = sum(x*y)
    a_5 = sum(x**5)
    b_2 = sum((x**2)*y)
    a_6 = sum(x**6)
    b_3 = sum((x**3)*y)
    A = np.array([[a_0, a_1, a_2,a_3], [a_1,a_2,a_3,a_4], [a_2,a_3,a_4,a_5], [a_3,a_4,a_5,a_6]])
    b = np.array([b_0,b_1,b_2,b_3])
    A = np.float64(A)
    b = np.float64(b)
    coeff = np.linalg.solve(A,b)
    y2 = coeff[0] + coeff[1]*x+coeff[2]*x**2+coeff[3]*x**3
    x2 = x
    plt.plot(x2,y) 
    plt.plot(x2,y2) 
    print(coeff)
    plt.show()


if __name__ == "__main__":
    ex6()
