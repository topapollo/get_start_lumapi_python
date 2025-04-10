import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.constants import c
import scipy.io as sio  
import pickle  

# add Lumerical API path
#sys.path.append(r"C:\Program Files\Lumerical\v241\api\python\\")
sys.path.append("/imec/software/lumericl/releases/2025R1.1/api/python/")
import lumapi
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

# part1: build the geometry
script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "1to2_my_own_mmi_structure.lsf")
mmi = lumapi.MODE(script_path, hide=True)
#mmi = lumapi.MODE("1to2_my_own_mmi_structure.lsf", hide=True)
mmi.save("my_own_mmi")

# part2: run the simulation
mmi.run()
print("Simulation completed.")


# part3: run the sweep to get E-field and s-parameters data
mmi.emepropagate()
print("E-field propagation completed.")
data = mmi.getresult("field_monitor","field profile");
x = data['x']
x = x[:,0]
y = data['y']
y = y[0,:]
E = data['E']
Ex = E[:,:,0,0,0]
Ey = E[:,:,0,0,1]
Ez = E[:,:,0,0,2]
Emag = np.sqrt(np.abs(Ex)**2 + np.abs(Ey)**2 + np.abs(Ez)**2)
print("Ex shape:", Ex.shape)

mmi.feval("emesweep.lsf")
s=mmi.getemesweep('S')
print("EME sweep completed.")
print("S-parameters shape:", s['s21'].shape)
mmi.close()
print("Value of s:", s)


# part4: save the data
s21=s['s21']
length=s['group_span_2']
s51_abs = np.abs(s21)
s51_phase = np.angle(s21, deg=True)  
sio.savemat('results_matlab.mat', {'length': length, 's21': s21,'Emag':Emag, 'x': x, 'y': y,'E':E})



print("All the data has been saved. mission accomplished.")