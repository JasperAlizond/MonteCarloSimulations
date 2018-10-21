#%matplotlib inline


import numpy as np
from math import *
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import random

# a is length of triangle along x-axis, b is length along y-axis
def randomPosInsideTriangle(a, b):
    while(True):
        x = random.random() * a
        y = random.random() * b
        # test whether (x,y) is in the triangle
        if(y <= -(b / a) * x + b and y >= 0 and x >= 0):
            return (x, y)

# returns random angle in degree
def randomAngle():
    return random.random() * 360

# a, b = triangle measurements, x0,y0 = position, theta = angle in degree
def findExitSide(a, b, x0, y0, theta):

    # ANTS PATH: make a line from pos and angle
    # slope 
    m1 = tan(theta/360.*2*pi)
    # y-Intersept 
    c1 = y0 - tan(theta/360.*2*pi) * x0
    antsPath = (lambda x: m1 * x + c1)

    # HYPOTENUSE: make a line for side c of triangle
    # slope 
    m2 = -(b/a)
    # y-Intersept
    c2 = b
    hypotenuse_c = (lambda x: m1 * x + c1)
    
    # for the next part divide by angles to know where to look for a intersection:
    section = [0, 0, 0, 0] # left and right x values, lower and upper y values
    tolerance = 0.0001 
    # top right -> ant leaves at side c no matter where it is
    if(( theta >= 0 and theta <= 90) or theta == 360) :
        return 'c'
    # top left
    if( theta > 90 and theta <= 180):
        # then look for an interception :
        section[0] = 0 - tolerance
        section[1] = x0
        section[2] = y0
        section[3] = b
    # bottom left
    if( theta > 180 and theta <= 270):
        section[0] = 0 - tolerance
        section[1] = x0
        section[2] = 0 - tolerance
        section[3] = y0
    # bottom right
    if( theta > 270 and theta < 360):
        section[0] = x0
        section[1] = a
        section[2] = 0 - tolerance
        section[3] = y0
    
    # inSection(x) returns true if (x, antsPath(x)) is in section, false otherwise
    inSection = lambda x: x >= section[0] and x <= section[1] and antsPath(x) >= section[2] and antsPath(x) <= section[3]
    
    # look for intersections in the section given:
    intersection_with_c = (c2 - c1)/(m1 - m2)
    if( inSection(intersection_with_c)):
        return 'c'
    intersection_with_b = 0
    if( inSection(intersection_with_b)):
        return 'b'
    intersection_with_a = -c1 / m1
    if( inSection(intersection_with_a)):
        return 'a'
    

    

# a, b = two sides of triangle next to right angle, N = no of iterations
def monteCarloApproach(a, b, N):
    #   |\
    #   | \
    #  b|  \
    #   |   \
    #   |    \
    #   |_____\
    #      a

    #x1 = linspace(0, a, 2)
    #y1 = -(b / a) * x1 + b
    #pyplot.grid(True)
    #pyplot.plot(x1,y1)
    exit_a = 0.
    exit_b = 0.
    exit_c = 0.
    error = 0
    count = 0
    
    while (count < N):
        # (x0,y0) = position of ant
        (x0,y0) = randomPosInsideTriangle(a,b)
        # theta = angle of ant in degree (e.g. looking to the right = 0 degrees, looking up = 90 degrees, etc.)
        theta = randomAngle()
        exitSide = findExitSide(a, b, x0, y0, theta)
        if(exitSide == 'c'):
            exit_c += 1
        elif(exitSide == 'b'):
            exit_b += 1
        elif(exitSide == 'a'):
            exit_a += 1
        else:
            error += 1
        #pyplot.plot(x0,y0,'r.')
        #pyplot.axis('equal')
        #pyplot.axis([-1, a+1, -1, b+1])
        count += 1
    
    return (exit_a/N, exit_b/N, exit_c/N)




def main():
    infile = open('triangle_triples.data', 'r')
    outfile = open('output.txt', 'w')
    # triple with smallest probability that ant leaves at hypotenuse
    smallestPTriple = (None, None, None)
    smallestP = 1
    # triple with largest probability that ant leaves at hypotenuse
    largestPTriple = (None, None, None)
    largestP = 0
    # larger number of ants --> more precise probability
    noOfAnts = 10000.
    histArray = []
    for line in infile:
        strlist = line.split()
        a = float(strlist[0])
        b = float(strlist[1])
        c = float(strlist[2])
        (probOfA, probOfB, probOfC) = monteCarloApproach(a, b, noOfAnts)
        # add the exit probabilities to the histogram data
        histArray.append(probOfC)
        outfile.write("({},{},{}): \t P(a) = {} \t P(b) = {} \t P(c) = {} \n".format(int(a), int(b), int(c), probOfA, probOfB, probOfC))
        if(probOfC < smallestP):
            smallestP = probOfC
            smallestPTriple = (int(a), int(b), int(c))
        if(probOfC > largestP):
            largestP = probOfC
            largestPTriple = (int(a), int(b), int(c))
    #pyplot.show()
    infile.close()
    outfile.close()
    print("smallest: {}: {}".format(smallestPTriple, smallestP))
    print("largest: {}: {}".format(largestPTriple, largestP))
    #print (monteCarloApproach(3., 4., 100000000.))

    # the histogram of the data
    n, bins, patches = plt.hist(histArray,bins=20, facecolor='green')

    # plot the histogram
    plt.xlabel('Exit probability')
    plt.ylabel('No. of triangles')
    plt.title(r'$\mathrm{Histogram\ of\ Pythagorean Triangles}\ $')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()