import matplotlib.pyplot as plt
import csv
 
X = []
Y = []
 
with open('ke.txt', 'r') as datafile:
    plotting = csv.reader(datafile, delimiter=',')
     
    for i,ROWS in enumerate(plotting):
        X.append(i)
        Y.append(float(ROWS[0]))
 
plt.plot(X, Y)
plt.title('KE / step')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()