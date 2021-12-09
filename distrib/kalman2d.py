import sys
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import inv

def drawMeasurement(coords):
    if (coords == None):
        return
    for i in range(len(coords) - 1):
        x = [coords[i][0], coords[i + 1][0]]
        y = [coords[i][1], coords[i + 1][1]]
        plt.plot(x, y, 'yo', linestyle='solid', markersize=1)
    plt.show(block=False)
    return

def drawCorrected(coords):
    if(coords == None):
        return
    for i in range(len(coords) - 1):
        x = [coords[i][0], coords[i + 1][0]]
        y = [coords[i][1], coords[i + 1][1]]
        plt.plot(x, y, 'bo', linestyle='solid', markersize=1)
    plt.show(block=False)
    return

def draw(measurement, corrected):
    fig = plt.figure()
    axis = fig.gca()
    axis.spines["top"].set_linewidth(1.5)
    axis.spines["right"].set_linewidth(1.5)
    axis.spines["left"].set_linewidth(1.5)
    axis.spines["bottom"].set_linewidth(1.5)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.gca().set_aspect('equal', adjustable='box')
    drawMeasurement(measurement)
    drawCorrected(corrected)
    plt.show()
    return

def kalmanFilterTimeUpdate(x, A, B, u, P, Q):
    xTemp = np.dot(A, x) + np.dot(B, u)
    pTemp = np.dot(A, np.dot(P, np.transpose(A))) + Q
    return xTemp, pTemp

def kalmanFilterMeasurementUpdate(P, H, R, x, z, l):
    temp = np.dot(H, np.dot(P, np.transpose(H))) + R
    inverse = inv(temp)
    K = np.dot(P, np.dot(np.transpose(H), inverse))
    xTemp = x + np.dot(K, (z - np.dot(H, x)))
    pTemp = np.dot(((np.identity(2)*l) - np.dot(K, H)), P)
    return xTemp, pTemp

def guess(control, init):
    x0 = init[0]
    y0 = init[1]
    location = []
    for i in control:
        x0 += i[0]
        y0 += i[1]
        location.append((x0,y0))
    return location

if __name__ == "__main__":
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    # Retrive file name for input data
    if (len(sys.argv) < 5):
        print("Four arguments required: python kalman2d.py [datafile] [x1] [x2] [lambda]")
        exit()

    filename = sys.argv[1]
    x0 = float(sys.argv[2])
    y0 = float(sys.argv[3])
    scaler = float(sys.argv[4])

    # Read data
    lines = [line.rstrip('\n') for line in open(filename)]
    data = []
    for line in range(0, len(lines)):
        temp = lines[line].split(' ')
        data.append((float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3])))

    # Print out the data
    print("The input data points in the format of 'k [u1, u2, z1, z2]', are:")
    for it in range(0, len(data)):
        print(str(it + 1) + ": ", end='')
        print(*data[it])

    control = []
    measurement = []
    for i in data:
        control.append((i[0],i[1]))
        measurement.append((i[2], i[3]))

    print(control)
    print(measurement)

    Q = np.array([[0.0001, 0.00002], [0.00002, 0.0001]])
    R = np.array([[0.01, 0.005], [0.005, 0.02]])

    updated = []
    coords = None
    P = np.identity(2)
    x = np.array([[x0], [y0]], dtype=object)
    H = np.identity(2)
    A = np.identity(2)
    B = np.identity(2)
    for i in range(len(data)):
        u = np.array([[data[i][0]],[data[i][1]]])
        (x, P) = kalmanFilterTimeUpdate(x, A, B, u, P, Q)
        z = np.array([[data[i][2]], [data[i][3]]])
        (x, P) = kalmanFilterMeasurementUpdate(P, H, R, x, z, scaler)
        updated.append(x)

    measurement.insert(0, (x0, y0))
    updated.insert(0, (x0, y0))
    draw(measurement, updated)
    
