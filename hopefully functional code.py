# -*- coding: utf-8 -*-
"""
演示二维插值。
"""
## double sharp = modified code
# -*- coding: utf-8 -*-
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
from scipy import interpolate
import matplotlib.cm as cm
import matplotlib.pyplot as plt

#def func(x, y):
#    return (x+y)*np.exp(-5.0*(x**2 + y**2))

## X-Y轴分为5*5的网格
x = np.linspace(-50, 50, 5)
y = np.linspace(-50,50,5)
x, y = np.meshgrid(x, y)#5*5的网格数据

#fvals = func(x,y) # 计算每个网格点上的函数值  10*10的值
##manually input Z values
fvals = np.array([[0,1,2,1,0],
               [2,2,2,2,2],
               [3,5,9,7,2],
               [6,10,7,6,1],
               [4,3,3,3,10]])

fig = plt.figure(figsize=(9, 6))
#Draw sub-graph1
ax=plt.subplot(1, 2, 1,projection = '3d')
surf = ax.plot_surface(x, y, fvals, rstride=2, cstride=2, cmap=cm.coolwarm,linewidth=0.5, antialiased=True)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.colorbar(surf, shrink=0.5, aspect=5)#标注

#二维插值
newfunc = interpolate.interp2d(x, y, fvals, kind='cubic')#newfunc为一个函数

# 计算100*100的网格上的插值
xnew = np.linspace(-50,50,101)#x
ynew = np.linspace(-50,50,101)#y
fnew = newfunc(xnew, ynew)#仅仅是y值   100*100的值  np.shape(fnew) is 100*100
xnew, ynew = np.meshgrid(xnew, ynew)
ax2=plt.subplot(1, 2, 2,projection = '3d')
surf2 = ax2.plot_surface(xnew, ynew, fnew, rstride=2, cstride=2, cmap=cm.coolwarm,linewidth=0.5, antialiased=True)
ax2.set_xlabel('xnew')
ax2.set_ylabel('ynew')
ax2.set_zlabel('fnew(x, y)')
plt.colorbar(surf2, shrink=0.5, aspect=5)#标注

plt.show()
print(fnew)
#post-process fnew
def check(A,i,j,I,J):
    if A == True:
        return fnew[i][j] > fnew[I][J]
    return True
out = []
for i in range(len(fnew)):
    for j in range(len(fnew[0])):
        if check(i != 0,i,j,i-1,j) and check(i != len(fnew)-1,i,j,i+1,j) and check(j != 0,i,j,i,j-1) and check(j != len(fnew[0])-1,i,j,i,j+1):
            out.append([xnew[0][j],ynew[i][0],fnew[i][j]])
print(out)
#out = local maximums