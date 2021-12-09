import sys
import matplotlib.pyplot as plt

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

def do(control, measurement, init, scaler):
    x0 = init[0]
    y0 = init[1]
    Q = None
    R = None

    return

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

    measurement.insert(0, (0,0))
    g = guess(control, (x0, y0))
    g.insert(0,(0,0))
    draw(measurement, g)
    
