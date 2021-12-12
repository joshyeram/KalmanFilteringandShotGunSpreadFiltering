import numpy as np
import matplotlib.pyplot as plt

def problem2(N):
    sample = []
    for i in range(N):
        s = np.random.normal()
        while(s > 5 or s < -5):
            s = np.random.normal()
        sample.append(s)
    return sample

temp = problem2(100)
plt.hist(temp, 50, (-5,5))
plt.title("N = 100")
plt.show()