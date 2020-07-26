import numpy as np

predictions = np.array([2,3,4])
Y = np.array([4,5,6])


m = predictions.size
loss = (predictions-Y)**2
result = loss.sum()/m

print(result) 