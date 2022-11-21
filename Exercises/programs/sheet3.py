import math
import numpy as np 
from matplotlib import pyplot as plt 

def plotting(): 
    x1 = np.linspace(1,7,50) 
    y1 = 1/(x1-1) 
    x2 = np.linspace(-2,1,50) 
    y2 = 1/(x2-1) 
    plt.xlim(-2,6)
    plt.ylim(-6,6)
    plt.plot(x1,y1,"m--",lw=4) 
    plt.plot(x2,y2,"m--",lw=4) 
    plt.show()

def trigonPlot():
    x = np.linspace(0,2*math.pi,50)
    p1 = np.sin(x)
    p2 = np.sin(2*x)
    p3 = 2*np.sin(x)
    p4 = 2*np.sin(2*x)
    fig, axes = plt.subplots(2,2)
    axes[0,0].plot(x,p1, "g-")
    axes[0,0].axis([0,2*math.pi,-2,2])
    axes[0,0].set_title("sin")
    axes[0,1].plot(x,p2, "r--")
    axes[0,1].axis([0,2*math.pi,-2,2])
    axes[0,1].set_title("sin(2x)")
    axes[1,0].plot(x,p3, "b--")
    axes[1,0].axis([0,2*math.pi,-2,2])
    axes[1,0].set_title("2sin")
    axes[1,1].plot(x,p4, "m.")
    axes[1,1].axis([0,2*math.pi,-2,2])
    axes[1,1].set_title("2sin(2x)")
    plt.show()

if __name__ == "__main__":
    trigonPlot()