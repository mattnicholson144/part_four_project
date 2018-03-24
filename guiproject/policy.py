import numpy as np
class Policy():
    def __init__(self, ):
        self.i_history = []
        self.j_history = []
    
    def valueFunction(self, i_next, j_next, k, l):
        values = []
        if len(self.i_history) > 1:
            index = -2
        else:
            index = -1
        for element in range(len(i_next)):
            dist_MH = np.abs(i_next[element] - k) + np.abs(j_next[element] - l)
            dist_EU = np.sqrt(np.power(i_next[element] - k, 2) + np.power(j_next[element] - l, 2))
            dist_prev = np.sqrt(np.power(i_next[element] - self.i_history[index], 2) + np.power(j_next[element] - self.j_history[index], 2))
            values.append(-(100*dist_MH + 100*dist_EU - dist_prev))
        return np.argmax(values)
    