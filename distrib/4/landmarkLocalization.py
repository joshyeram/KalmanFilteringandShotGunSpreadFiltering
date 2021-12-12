import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import inv

robot = (4,8)

def transform(coords):
    width = robot[0]
    height = robot[1]
    rotation = coords[2]
    translation = (coords[0], coords[1])
    trX = np.cos(rotation) * (width / 2.) - np.sin(rotation) * (height / 2.)
    trY = np.sin(rotation) * (width / 2.) + np.cos(rotation) * (height / 2.)

    tlX = np.cos(rotation) * -1 * (width / 2.) - np.sin(rotation) * (height / 2.)
    tlY = np.sin(rotation) * -1 * (width / 2.) + np.cos(rotation) * (height / 2.)

    tl = (tlX, tlY)
    tr = (trX, trY)
    bl = (-1 * trX, -1 * trY)
    br = (-1 * tlX, -1 * tlY)

    dtl = tuple(np.add(tl, translation))
    dtr = tuple(np.add(tr, translation))
    dbl = tuple(np.add(bl, translation))
    dbr = tuple(np.add(br, translation))

    return [dbl, dtl, dtr, dbr]

def drawRobot(coords):
    temp = transform(coords)
    xi, yi = zip(*temp)
    plt.fill(xi, yi, color="green")
    plt.show(block=False)
    return

def drawGroundTruth(coords):
    xi, yi, rot = zip(*coords)
    plt.plot(xi,yi,color="black", markersize=1)
    plt.show(block=False)
    return

def readEnv(fileName):
    file = open(fileName, "r")
    temp = int(file.readline())
    pos = []
    for i in range(temp):
        t = file.readline().rstrip("\n")
        s = t.split(" ")
        pos.append((float(s[0]),float(s[1])))
    return np.array(pos)

def readGroundTruth(fileName):
    file = open(fileName, "r")
    temp = int(file.readline())
    pos = []
    for i in range(temp):
        t = file.readline().rstrip("\n")
        s = t.split(" ")
        pos.append((float(s[0]), float(s[1]), float(s[2])))
    return np.array(pos)

def drawEnv(coords, env, truth):
    fig = plt.figure()
    axis = fig.gca()
    axis.spines["top"].set_linewidth(1.5)
    axis.spines["right"].set_linewidth(1.5)
    axis.spines["left"].set_linewidth(1.5)
    axis.spines["bottom"].set_linewidth(1.5)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.gca().set_aspect('equal', adjustable='box')

    drawRobot(coords)

    for i in env:
        plt.plot(i[0],i[1], ".", color = "black", markersize=10)

    drawGroundTruth(truth)

    plt.show()
    return

env = readEnv("landmark_2.txt")
truth = readGroundTruth("ground_truth_2.txt")
drawEnv((50,50,0), env, truth)