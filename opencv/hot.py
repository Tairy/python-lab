# encoding:utf-8
import numpy as np
from matplotlib import pyplot as plt

x = 10
y = 10
hist, xedges, yedges = np.histogram2d(x,y)
X,Y = np.meshgrid(xedges,yedges)
plt.imshow(hist)
plt.grid(True)
plt.colorbar()
plt.show()