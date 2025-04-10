import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.constants import c
import scipy.io as sio  
import pickle  

# add Lumerical API path
sys.path.append(r"C:\Program Files\Lumerical\v241\api\python\\")
#sys.path.append("/imec/software/lumericl/releases/2025R1.1/api/python/")
sys.path.append(os.path.dirname(__file__))
import lumapi
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

# part1: build the geometry amd collect parameters from lumerical
script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "1to2_my_own_mmi_structure.lsf")
mmi = lumapi.FDTD(script_path, hide=False)
#mmi = lumapi.FDTD("1to2_my_own_mmi_structure.lsf", hide=True)
mmi.eval("?'start, press spacebar to continue';")
coupler_length = mmi.getv("coupler_length")
coupler_width = mmi.getv("coupler_width")
taper_length = mmi.getv("taper_length")
wavelength = 785e-9



# part2: run the simulation
mmi.addfdtd()
mmi.set("x span",coupler_length+2*taper_length+0.5e-6)
mmi.set("y span",4*coupler_width)
mmi.set("x",0)
mmi.set("y",0)
mmi.set("z",0)
mmi.set("z span", 4e-6)
mmi.set("y min bc","Metal")
mmi.set("y max bc","Metal")
mmi.set("z min bc","Metal")
mmi.set("z max bc","Metal")



mmi.setglobalsource("center wavelength", wavelength)
mmi.setglobalsource("wavelength span", 0)
mmi.setglobalmonitor("frequency points",1)

mmi.addpower()
mmi.set("name","field_monitor")
mmi.set("simulation type","3D")
mmi.set("monitor type","2D Z-normal")
mmi.set("x",0)
mmi.set("x span",coupler_length+taper_length*2+0.5e-6)
mmi.set("y",0)
mmi.set("y span",coupler_width*3)
mmi.set("z",0)
mmi.set("override global monitor settings",1)
mmi.set("use wavelength spacing",1)
mmi.set("frequency points",1)


mmi.addport()
mmi.set("x",-coupler_length/2-taper_length-0.25e-6)
mmi.set("mode selection","fundamental TE mode")


mmi.addport()
mmi.set("x",coupler_length/2+taper_length+0.25e-6)
mmi.set("mode selection","fundamental TE mode")
mmi.set("y min",0)
mmi.set("y max",2*coupler_width)


mmi.addport()
mmi.set("x",coupler_length/2+taper_length+0.25e-6)
mmi.set("mode selection","fundamental TE mode")
mmi.set("y max",0)
mmi.set("y min",-2*coupler_width)


mmi.pause(10000)
mmi.save("check")
