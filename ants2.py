#%matplotlib inline


from numpy import *
from math import *
from matplotlib import pyplot
import random
from scipy.optimize import fsolve

# a is length of triangle along x-axis, b is length along y-axis
def randomPosInsideTriangle(a, b):
    while(True):
        x = random.random() * a
        y = random.random() * b
        # test whether (x,y) is in the triangle
        if(y <= -(b / a) * x + b and y >= 0 and x >= 0):
            return (x, y)

def randomAngle():
    return random.random() * 360

# a, b = triangle measurements, x0,y0 =pos, theta = angle in degree
def findExitSide(a, b, x0, y0, theta):
    # make a line from pos and angle
    antsPath = (lambda x: tan(theta/360.*2*pi) * x + y0 - tan(theta/360.*2*pi) * x0)
    #print theta
    #pyplot.plot([-1, a+1], [antsPath(-1), antsPath(a+1)], 'g--')
    # make a line for side c of triangle
    hypotenuse_c = (lambda x: -(b / a) * x + b)
    
    # for the next part divide by angles to know where to look for a intersection:
    section = [0, 0, 0, 0] # left and right x values, lower and upper y values
    # top right -> ant leaves at side c no matter where it is
    if(( theta >= 0 and theta <= 90) or theta == 360) :
        return 'c'
    # top left
    if( theta > 90 and theta <= 180):
        # then look for an interception :
        section[0] = 0
        section[1] = x0
        section[2] = y0
        section[3] = b
    # bottom left
    if( theta > 180 and theta <= 270):
        section[0] = 0
        section[1] = x0
        section[2] = 0
        section[3] = y0
    # bottom right
    if( theta > 270 and theta < 360):
        section[0] = x0
        section[1] = a
        section[2] = 0
        section[3] = y0
    # look for intersections in the section given:
    # lambda for (point is in section)
    inSection = lambda x: x >= section[0] and x <= section[1] and antsPath(x) >= section[2] and antsPath(x) <= section[3]
    intersection_with_c = fsolve(lambda x: antsPath(x) - hypotenuse_c(x), 0.0)[0]
    if( inSection(intersection_with_c)):
        return 'c'
    intersection_with_b = antsPath(0)
    if( inSection(intersection_with_b)):
        return 'b'
    intersection_with_a = fsolve(antsPath, 0.0)[0]
    if( inSection(intersection_with_a)):
        return 'a'
    

    
    

# a, b = two sides of triangle next to right angle, N = no of iterations
def monteCarloApproach(a, b, N):
    x1 = linspace(0, a, 2)
    y1 = -(b / a) * x1 + b
    pyplot.grid(True)
    pyplot.plot(x1,y1)
    exit_a = 0.
    exit_b = 0.
    exit_c = 0.
    count = 0
    
    while (count < N):
        # (x,y) = pos of ant
        (x0,y0) = randomPosInsideTriangle(a,b)
        # theta = angle of ant in degree
        theta = randomAngle()
        exitSide = findExitSide(a, b, x0, y0, theta)
        if(exitSide == 'c'):
            exit_c += 1
        pyplot.plot(x0,y0,'r.')
        #pyplot.axis('equal')
        #pyplot.axis([-1, a+1, -1, b+1])
        count += 1
    
    print exit_c, N
    print exit_c/N
    return exit_c/N




def main():
    print (monteCarloApproach(3.0, 4.0, 1000.))
    pyplot.show()
    
    


if __name__ == '__main__':
    main()