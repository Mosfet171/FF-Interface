
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from matplotlib.animation import FuncAnimation
import numpy as np
import socket
import time
import joblib

R_MAX = 1    # Maximum intensity before perforation (in Newtons)

# Parameters for drawing:
MAX_XY = 100
MAX_Z = 25
MAX_ORDER = 5 # Numbers of colors / arcs

# Parameters for TCP/IP connection
TCP_IP = '127.0.0.1'
TCP_PORT = 2055
MAX_ERR_CNT = 3 # Kill the connection after 3 consecutive errors

# SVMs:
svr_x = joblib.load('svr_fx2.joblib')
svr_y = joblib.load('svr_fy2.joblib')
svr_z = joblib.load('svr_fy2.joblib')

def data2force(dx, dy, dz):
    '''
    Predicts the forces based on the wavelength differences returned by the
    interrogator.
    '''
    Fx = svr_x.predict(np.array([dx,dy,dz]).reshape(1,-1))
    Fy = svr_y.predict(np.array([dx,dy,dz]).reshape(1,-1))
    Fz = svr_z.predict(np.array([dx,dy,dz]).reshape(1,-1))
    return Fx, Fy, Fz

def three2polar(Fx, Fy, Fz):
    '''
    Converts the X and Y components to "polar" coordinates (angles and intensity).
    Fz is returned untouched (just for simplicity in the code later).
    '''
    if Fx == 0 and Fy == 0:
        Fxy_angle = 1000
    elif Fx == 0:
        if Fy > 0:
            Fxy_angle = 90
        else:
            Fxy_angle = 270
    elif Fy == 0:
        if Fx > 0:
            Fxy_angle = 0
        else:
            Fxy_angle = 180
    else:
        Fxy_angle = int(np.arctan2(Fy,Fx)*360/(2*np.pi))

    # Intensity
    Fxy_intensity = np.sqrt(np.power(Fx,2) + np.power(Fy,2))

    return Fxy_angle, Fxy_intensity, Fz

def listen(s):
    '''
    Function (base for a generator) that listens through the socket s and
    provides the three wavelength received from the interrogator.
    '''
    while True:
        # First check the length of the message:
        BUFFER_SIZE = int.from_bytes(s.recv(4),"big",signed=False)
        # Then receive the data:
        rawdata = s.recv(BUFFER_SIZE)
        # If we don't receive anything for MAX_ERR_CNT times, we close the
        # connection.
        if not rawdata:
            if ERR_CNT > MAX_ERR_CNT:
                print("Connection lost with client. Closing connection ...")
                conn.close()
                print("Connection closed. Exiting.")
                exit(1)
            print("No data received ... Continuing ({} attempt(s) remaining)".format(MAX_ERR_CNT-ERR_CNT))
            ERR_CNT += 1
            dx, dy, dz = 0, 0, 0
        # Else we decode the data received
        else:
            textdata = rawdata.decode("utf-8").split("\t")[-3:]
            wavelength = [int(textdata[i].split(',')[0]) for i in range(3)]
            dx, dy, dz = wavelength[0],wavelength[1],wavelength[2]

        yield dx, dy, dz


def displayInt(testing=False):
    """
    Display the simulation using matplotlib. Main function.
    """

    # ---------- TCP/IP CONNECTION ---------- #
    # Creating a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to the server (the interrogator's software)
    print("Connecting to the server ...")
    s.connect((TCP_IP, TCP_PORT))
    print("Connected !")

    # ---------- MAIN INTERFACE ---------- #
    # Initializing the interface
    fig, ax = plt.subplots(facecolor="#101010",subplot_kw={'projection': 'polar'})
    ax.tick_params(labelcolor="#AAAAAA")
    ax.set_rlim((0,MAX_XY+MAX_Z+20))
    ax.grid(False)
    ax.set_rticks([])
    ax.patch.set_facecolor("#000000")
    # Small "+" in the center:
    ax.plot(0,0, marker="+", color="#AAAAAA")
    # Creating the dotted circles
    fullrads = np.arange(0,2*np.pi,0.01)
    rbig = [MAX_XY*0.75+MAX_Z]*np.size(fullrads)
    rsmall = [MAX_Z*0.75]*np.size(fullrads)
    plt.polar(fullrads,rsmall,ls='--', color="#AAAAAA")
    plt.polar(fullrads,rbig,ls='--', color="#AAAAAA")
    # Defining the colors for the arcs
    wificolors = ['#00FF00','#E7E000','#E78500','#DE0000', '#FF0000']

    # Preparation for alert:
    #plt.rcParams["figure.figsize"] = [7.00, 3.50]
    #plt.rcParams["figure.autolayout"] = True
    #im = plt.imread('warning.jpg') # insert local path of the image.
    #newax = fig.add_axes([0.75,0.75,0.25,0.25], anchor='NE', zorder=1)

    # Creating the generator
    lst = listen(s)
    # Initializing the arcs
    angle = 0
    order = 0
    rads = np.arange(angle-0.05*order,angle+0.05*order,0.01)
    r = [order/MAX_ORDER*MAX_XY+MAX_Z+5]*np.size(rads)
    arc1, = ax.plot(rads,r,color=wificolors[0],lw=7)
    arc2, = ax.plot(rads,r,color=wificolors[1],lw=7)
    arc3, = ax.plot(rads,r,color=wificolors[2],lw=7)
    arc4, = ax.plot(rads,r,color=wificolors[3],lw=7)
    arc5, = ax.plot(rads,r,color=wificolors[4],lw=7)
    arcs = [arc1, arc2, arc3, arc4, arc5]

    # Initialization function for the FuncAnimation class. Mainly useful
    # for blitting.
    def init():
        for arc in arcs:
            arc.set_data(0,0)

        return arc1, arc2, arc3, arc4, arc5,

    # Main function for the FuncAnimation class.
    def animate(i):
        tic = time.time()
        dx, dy, dz = next(lst) # Retrieve wavelengths
        tac1 = time.time()
        Fx, Fy, Fz = data2force(dx,dy,dz) # Transforming into forces
        #print("{}\t{}\t{}".format(Fx,Fy,Fz))
        angle, intensity, zintensity = three2polar(Fx, Fy, Fz) # Transforming into polar
        tac2 = time.time()
        # Drawing the arcs
        arcs = [arc1, arc2, arc3, arc4, arc5]
        for order in range(1,int(np.ceil((intensity/R_MAX)*MAX_ORDER))+1):
            rads = np.arange(angle-0.05*order,angle+0.05*order,0.01)
            r = [order/MAX_ORDER*MAX_XY+MAX_Z+5]*np.size(rads)
            arcs[order-1].set_data(rads,r)
            arcs[order-1].set_visible(True)
        if order > 0:
            for i in range(MAX_ORDER-order):
                arcs[MAX_ORDER-i-1].set_visible(False)
        else:
            for i in range(MAX_ORDER):
                arcs[i].set_visible(False)

        # Drawing the Z-circle
        order_for_color = int(np.ceil((zintensity/R_MAX)*MAX_ORDER))
        zcolor = wificolors[order_for_color]
        zr_value = zintensity/R_MAX*MAX_Z
        zr = [zr_value]*np.size(fullrads)
        zcircle = Circle((0, 0), zr_value, transform=ax.transData._b, color=zcolor)
        ax.add_artist(zcircle)

        return arc1, arc2, arc3, arc4, arc5, #zcircle

    anim = FuncAnimation(fig,animate,init_func=init,blit=True,interval=1,frames=1000,repeat=False)
    plt.show()

    plt.close(fig)

if __name__ == '__main__':
    displayInt(testing=True)
