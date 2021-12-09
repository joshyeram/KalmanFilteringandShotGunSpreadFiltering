import sys

if __name__ == "__main__":
    # Retrive file name for input data
    if (len(sys.argv) < 5):
        print("Four arguments required: python kalman2d.py [datafile] [x1] [x2] [lambda]")
        exit()

    filename = sys.argv[1]
    x10 = float(sys.argv[2])
    x20 = float(sys.argv[3])
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
    
