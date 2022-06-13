import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from matplotlib.animation import FuncAnimation
import numpy as np
import socket
import time
import joblib

MAX_XY = 100
R_MAX = 1
MAX_Z = 25
MAX_ORDER = 5

TCP_IP = '127.0.0.1'
TCP_PORT = 2055
MAX_ERR_CNT = 3

fig, ax = plt.subplots(facecolor="#101010",subplot_kw={'projection': 'polar'})
ax.tick_params(labelcolor="#AAAAAA")
ax.set_rlim((0,MAX_XY+MAX_Z+20))
ax.grid(False)
ax.set_rticks([])
ax.xaxis.set_ticklabels([])
#ax.axis('off')
ax.patch.set_facecolor("#000000")
ax.plot(0,0, marker="+", color="#AAAAAA")

fullrads = np.arange(0,2*np.pi,0.01)
rbig = [MAX_XY*0.75+MAX_Z]*np.size(fullrads)
rsmall = [MAX_Z*0.75]*np.size(fullrads)

plt.polar(fullrads,rsmall,ls='--', color="#AAAAAA")
plt.polar(fullrads,rbig,ls='--', color="#AAAAAA")


wificolors = ['#00FF00','#00FF00','#E7E000','#E78500','#DE0000', '#FF0000']

angle = 0
order = 0
rads = np.arange(angle-0.05*order,angle+0.05*order,0.01)
r = [order/MAX_ORDER*MAX_XY+MAX_Z+5]*np.size(rads)
arc1, = ax.plot(rads,r,color=wificolors[1],lw=8)
arc2, = ax.plot(rads,r,color=wificolors[2],lw=8)
arc3, = ax.plot(rads,r,color=wificolors[3],lw=8)
arc4, = ax.plot(rads,r,color=wificolors[4],lw=8)
arc5, = ax.plot(rads,r,color=wificolors[5],lw=8)
arcs = [arc1, arc2, arc3, arc4, arc5]


angle, intensity = np.pi/13, 0.55
zintensity = 0.3

for order in range(1,int(np.ceil((intensity/R_MAX)*MAX_ORDER))+1):
    rads = np.arange(angle-0.05*order,angle+0.05*order,0.01)
    r = [order/MAX_ORDER*MAX_XY+MAX_Z+5]*np.size(rads)
    arcs[order-1].set_data(rads,r)
    arcs[order-1].set_visible(True)
for i in range(MAX_ORDER-order):
    arcs[MAX_ORDER-i-1].set_visible(False)

order_for_color = int(np.ceil((zintensity/R_MAX)*MAX_ORDER))
print(order_for_color)
zcolor = wificolors[order_for_color]

zr_value = zintensity/R_MAX*MAX_Z
zr = [zr_value]*np.size(fullrads)

# One working option:
zcircle = Circle((0, 0), zr_value, transform=ax.transData._b, color=zcolor)
ax.add_artist(zcircle)

# Test:
#plt.polar(fullrads,zr,color=zcolor)
#ax.fill_between([0.001]*fullrads,zr,color=zcolor)

plt.show()
