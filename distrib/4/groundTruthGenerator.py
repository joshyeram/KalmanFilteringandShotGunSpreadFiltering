import numpy as np

def generateGroundTruth(K, init, maxRot, maxTrans, dt):
    x0 = init[0]
    y0 = init[1]
    rot0 = init[2]
    temp = []
    temp.append(init)
    for i in range(K):
        rot = np.random.uniform(low=-maxRot, high=maxRot)
        rot0 += rot
        rot0 %= np.pi * 2
        trans = np.random.uniform(high=maxTrans)
        movement = trans * dt
        deltaX = np.cos(rot0) * movement
        deltaY = np.sin(rot0) * movement
        x0 += deltaX
        y0 += deltaY
        temp.append((x0, y0, rot0))
    file = open("ground_truth_" + str(K) + ".txt", "w")
    file.write(str(K) + "\n")
    for i in temp:
        msg = str(i[0])+" "+str(i[1])+" "+ str(i[2])+"\n"
        file.write(msg)
    file.close()
    return temp

"""print(generateGroundTruth(100,(50,50, 0), .9, 2, 1))"""