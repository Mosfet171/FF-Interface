import tkinter as tk
import DraftMFE
from tkinter.colorchooser import askcolor

# Initializing window and frames
root = tk.Tk()
root.title('Dispatch GUI (MFE)')
root.geometry('500x200')

frm_type = tk.Frame(relief=tk.GROOVE, height=300)
frm_checkboxes = tk.Frame()
frm_bgcolor = tk.Frame()
frm_fgcolor = tk.Frame()
frm_alertfrm = tk.Frame()
frm_alert = tk.Frame()
frm_simulation = tk.Frame()
frm_interval = tk.Frame()

# Type of interface
checkboxes = []
var_type = tk.IntVar()
lbl_type = tk.Label(frm_type, text="Select type", font=("Helvetica Bold", 20)).pack()
checkboxes.append(tk.Checkbutton(frm_checkboxes, onvalue=0, variable=var_type, text="WiFi"))
checkboxes.append(tk.Checkbutton(frm_checkboxes, onvalue=1, variable=var_type, text="Fading"))
checkboxes.append(tk.Checkbutton(frm_checkboxes, onvalue=2, variable=var_type, text="Arrow"))

frm_type.place(x=10, y=20)
frm_checkboxes.place(x=30, y=50)
for i in range(3):
    checkboxes[i].pack(anchor=tk.W)

'''
# BG COLOR
BG_COLOR = "#000000"
frm_inbgcolor = tk.Frame(bg=BG_COLOR, height=50, width=50)
frm_inbgcolor.place(x=190, y=70)

def change_color_bg():
    global BG_COLOR
    colors = askcolor(title="Background Color")
    BG_COLOR = colors[1]
    frm_inbgcolor.configure(bg=BG_COLOR)

tk.Button(
    frm_bgcolor,
    text='Select BG Color',
    command=change_color_bg).pack(expand=True)

frm_bgcolor.place(x=150, y=30)

# FG COLOR
FG_COLOR = "#FF0000"
frm_infgcolor = tk.Frame(bg=FG_COLOR, height=50, width=50)
frm_infgcolor.place(x=340, y=70)

def change_color_fg():
    global FG_COLOR
    colors = askcolor(title="Foreground Color")
    FG_COLOR = colors[1]
    frm_infgcolor.configure(bg=FG_COLOR)

tk.Button(
    frm_fgcolor,
    text='Select FG Color',
    command=change_color_fg).pack(expand=True)

frm_fgcolor.place(x=300, y=30)
'''

# Alerts
var_alert = tk.IntVar()
var_circle = tk.IntVar()
tk.Label(frm_alertfrm, text="Select\n artefacts", font=("Helvetica Bold", 20)).pack()
tk.Checkbutton(frm_alert, onvalue=1, var=var_alert, text="Alert").pack(anchor=tk.W)
tk.Checkbutton(frm_alert, onvalue=1, var=var_circle, text="Circle").pack(anchor=tk.W)

#frm_alertfrm.pack()
#frm_alert.pack()

frm_alertfrm.place(x=135, y=20)
frm_alert.place(x=145, y=72)

var_interval = tk.StringVar()
tk.Label(root, text="R_MAX", font=("Helvetica Bold", 20)).place(x=240, y=20)
intBox = tk.Entry(root, textvariable=var_interval, width=5)
intBox.place(x=260, y=60)
intBox.insert(0, "100")

var_interval = tk.StringVar()
tk.Label(root, text="Ratio XY/Z", font=("Helvetica Bold", 20)).place(x=340, y=20)
intBox = tk.Entry(root, textvariable=var_interval, width=5)
intBox.place(x=360, y=60)
intBox.insert(0, "100")

'''
# Simulation or not
var_sim = tk.IntVar()
tk.Label(root, text="Matrix", font=("Helvetica Bold", 20)).place(x=130, y=170)
tk.Checkbutton(frm_simulation, onvalue=1, var=var_sim, text="Live").pack(anchor=tk.W)
tk.Checkbutton(frm_simulation, onvalue=0, var=var_sim, text="Recorded").pack(anchor=tk.W)
tk.Checkbutton(frm_simulation, onvalue=2, var=var_sim, text="Random").pack(anchor=tk.W)

frm_simulation.place(x=135, y=200)

# Interval
var_interval = tk.StringVar()
tk.Label(root, text="Interval\n (if Sim)", font=("Helvetica Bold", 20)).place(x=230, y=170)
intBox = tk.Entry(root, textvariable=var_interval, width=5)
intBox.place(x=240, y=230)
intBox.insert(0, "100")
'''

def launch():
    how = var_type.get()

    if how == 0:
        var_how = "wifi"
    elif how == 1:
        var_how = "fading"
    else:
        var_how = "arrow"

    interval = int(var_interval.get())

    params = [var_sim.get(), BG_COLOR, FG_COLOR, var_circle.get(), var_alert.get(), var_how, var_sim.get(), interval]
    DraftMFE.displayInterface(params=params)

tk.Button(root, text="Launch !", command=launch).place(x=200, y=150)


root.mainloop()
