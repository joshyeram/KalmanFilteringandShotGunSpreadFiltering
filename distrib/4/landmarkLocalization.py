import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import inv
import math

robot = (8,4)

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

def drawOdom(coords):
    xi, yi, rot = zip(*coords)
    plt.plot(xi,yi,color="blue", markersize=1)
    plt.show(block=False)
    return

def drawpart(coords):
    xi, yi, rot = zip(*coords)
    plt.plot(xi,yi,color="gray", markersize=1)
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

def sample(enviro, groundTruth):
    env = readEnv(enviro)
    gt = readGroundTruth(groundTruth)
    tempMake = []
    for i in range(len(gt)-1):
        diff = np.subtract(gt[i+1], gt[i])
        trans = np.sqrt(diff[0]**2 + diff[1]**2)
        rot = diff[2]
        while (rot < 0):
            rot += np.pi * 2
        rot %= np.pi * 2
        sT = np.random.normal(trans, .1)
        sR = np.random.normal(rot, .1)
        if(sR<0):
            sR += np.pi * 2
        sR2 = np.random.normal(rot, .1)
        tempMake.append((sR, sT, sR2))
    tempObs = []
    for i in range(1,len(gt)):
        tempB = []
        for j in env:
            b = math.atan2(j[1] - gt[i][1], j[0] - gt[i][0]) - gt[i][2]
            sB = np.random.normal(b, .0523)
            while(sB<0):
                sB += np.pi*2
            sB %= np.pi*2
            tempB.append(sB)
        tempObs.append(tempB)
    name = "measurement_"+enviro[enviro.find("_")+1: enviro.find(".")] + ".txt"
    file = open(name, "w")
    file.write(str(gt[0][0])+" "+str(gt[0][1])+" "+str(gt[0][2])+"\n")
    file.write(str(len(gt))+"\n")
    for i in range(len(tempMake)):
        file.write(str(tempMake[i][0]) + " " + str(tempMake[i][1]) + " " + str(tempMake[i][2]) + "\n")
        for j in range(len(tempObs[i])):
            file.write(str(tempObs[i][j]))
            if(j==(len(tempObs[i])-1)):
                file.write("\n")
            else:
                file.write(" ")
    file.close()
    return

def readMeasurementOdom(fileName):
    file = open(fileName, "r")
    temp = file.readline().rstrip("\n").split(" ")
    init = (float(temp[0]), float(temp[1]), float(temp[2]))
    x0 = init[0]
    y0 = init[1]
    r0 = init[2]
    K = int(file.readline().rstrip("\n"))
    control = []
    observ = []
    for i in range(K-1):
        temp = file.readline().rstrip("\n").split(" ")
        c = (float(temp[0]), float(temp[1]), float(temp[2]))
        control.append(c)
        temp = file.readline().rstrip("\n").split(" ")
        o = []
        for j in temp:
            o.append(float(j))
        observ.append(o)
    odom = []
    odom.append(init)
    for i in control:
        r0 += i[0]
        while (r0 < 0):
            r0 += np.pi * 2
        r0 %= np.pi * 2
        x0 += np.cos(r0) * i[1]
        y0 += np.sin(r0) * i[1]
        odom.append((x0, y0, r0))
    return odom

def readMeasurement(fileName):
    file = open(fileName, "r")
    temp = file.readline().rstrip("\n").split(" ")
    init = (float(temp[0]), float(temp[1]), float(temp[2]))
    x0 = init[0]
    y0 = init[1]
    r0 = init[2]
    K = int(file.readline().rstrip("\n"))
    control = []
    observ = []
    for i in range(K-1):
        temp = file.readline().rstrip("\n").split(" ")
        c = (float(temp[0]), float(temp[1]), float(temp[2]))
        control.append(c)
        temp = file.readline().rstrip("\n").split(" ")
        o = []
        for j in temp:
            o.append(float(j))
        observ.append(o)

    return (init, control, observ)

def particleFilter(landmark, measurement, particle):
    env = readEnv(landmark)
    m = readMeasurement(measurement)
    init = m[0]
    odom = m[1]
    obv = m[2]
    x0 = init[0]
    y0 = init[1]
    r0 = init[2]
    all =[]
    all.append(init)
    for i in range(len(odom)):
        temp = []
        prob = []
        trans = odom[i][1]
        rot = odom[i][0]
        samples = particleSample((x0, y0, r0), trans, rot, particle)
        #samples = [(50.296, 49.904, 5.9),(50.2, 49.9, 5.89),(50.3, 50.1, .1),(50.28146311952254 ,49.89341963677278, 5.921204956923461)]
        for j in samples:
            temp.append(bearing(j, env))
        for j in temp:
            prob.append(avgError(j, obv[i]))
        pos = samples[prob.index(min(prob))]
        all.append(pos)
        x0 = pos[0]
        y0 = pos[1]
        r0 = pos[2]
        if i == 10000:
            return (pos, samples, all)
    return all

def bearing(pose, env):
    temp = []
    for j in env:
        b = math.atan2(j[1] - pose[1], j[0] - pose[0]) - pose[2]
        while (b < 0):
            b += np.pi * 2
        b %= np.pi * 2
        temp.append(b)
    return temp

def avgError(bearing, obs):
    temp = 0
    for i in range(len(bearing)):
        t = obs[i] - bearing[i]
        tPrime = bearing[i] - obs[i]
        if(t>np.pi):
            t-=np.pi*2
        if (tPrime > np.pi):
            tPrime -= np.pi * 2
        temp += min(abs(t), abs(tPrime))/obs[i]
    return temp

def particleSample(pose, trans, rot, k):
    temp = []
    for i in range(k):
        sT = np.random.normal(trans, .1)
        sR = np.random.normal(rot, .1)
        roto = pose[2] + sR
        while (roto < 0):
            roto += np.pi * 2
        roto %= np.pi * 2
        msg = (pose[0] + np.cos(roto) * sT, pose[1] + np.sin(roto) * sT, roto)
        temp.append(msg)
    return temp

def drawEnv(coords, env, truth, odom):
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
    drawOdom(odom)
    plt.show()
    return

def drawParticle(coords, env, truth, odom, particle):
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
    drawOdom(odom)
    if(len(particle)!=3):
        drawpart(particle)
    else:
        for i in particle[1]:
            plt.plot(i[0],i[1], ".", color = "black", markersize=5)
            #plt.arrow(i[0],i[1], 5*np.cos(i[2]), 5*np.sin(i[2]))
        plt.plot(particle[0][0], particle[0][1], ".", color="yellow", markersize=10)
        drawpart(particle[2])

    plt.show()
    return



#sample("landmark_2.txt","ground_truth_2.txt")

route = particleFilter("landmark_2.txt", "measurement_2.txt", 100)

env = readEnv("landmark_2.txt")
truth = readGroundTruth("ground_truth_2.txt")
measurement = readMeasurementOdom("measurement_2.txt")
#drawEnv((50,50,0), env, truth, route)
drawParticle((50,50,0), env, truth, measurement, route)