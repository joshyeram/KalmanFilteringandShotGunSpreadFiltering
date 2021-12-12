import numpy as np

def generateLandmark(N):
    file = open("landmark_"+str(N)+".txt", "w")
    temp = np.random.randint(100, size=(N,2))
    file.write(str(N)+"\n")
    for i in temp:
        msg = str(i[0])+" "+str(i[1])+"\n"
        file.write(msg)
    file.close()
