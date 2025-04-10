import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.constants import c
import scipy.io as sio  # 用于保存 MATLAB 兼容文件
import pickle  # 用于保存 Python 对象

# add Lumerical API path
sys.path.append(r"C:\Program Files\Lumerical\v241\api\python\\")
#sys.path.append("/imec/software/lumericl/releases/2025R1.1/api/python/")
import lumapi
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

taper_widths = np.linspace(0.54e-6,1.14e-6,13)  # 0.5 um

for width in taper_widths:
    print("Taper width:", width)
    # part1: build the geometry
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "1to2_my_own_mmi_structure.lsf")
    #mmi = lumapi.MODE(script_path, hide=True)
    mmi = lumapi.MODE(script_path)
    
    # 获取必要的几何参数
    coupler_length = mmi.getnamed("::model::MMI::MMI_core", "x span")
    taper_length = mmi.getv("taper_length")
    waveguide_width = mmi.getv("waveguide_width")
    separation = mmi.getv("separation")    
    # 构建 input1 锥形波导的顶点
    x_input1 = np.array([-coupler_length/2 - taper_length, -coupler_length/2, -coupler_length/2, -coupler_length/2 - taper_length])
    y_input1 = np.array([waveguide_width/2, width/2, -width/2, -waveguide_width/2])
    # 创建符合 Lumerical 要求的顶点矩阵（按列组织）
    V_input1 = np.vstack((x_input1, y_input1))  # 使用 vstack 垂直堆叠，创建 2 行 n 列矩阵

    # 同理，对 output1 和 output2 构造矩阵
    x_output1 = np.array([coupler_length/2 + taper_length, coupler_length/2, coupler_length/2, coupler_length/2 + taper_length])
    y_output1 = np.array([waveguide_width/2 + separation*0.5, width/2 + separation*0.5, -width/2 + separation*0.5, -waveguide_width/2 + separation*0.5])
    V_output1 = np.vstack((x_output1, y_output1))

    x_output2 = np.array([coupler_length/2 + taper_length, coupler_length/2, coupler_length/2, coupler_length/2 + taper_length])
    y_output2 = np.array([waveguide_width/2 - separation*0.5, width/2 - separation*0.5, -width/2 - separation*0.5, -waveguide_width/2 - separation*0.5])
    V_output2 = np.vstack((x_output2, y_output2))
    
    # 使用 setnamed 更新锥形波导的顶点
    mmi.setnamed("::model::MMI::input1", "vertices", V_input1)
    mmi.setnamed("::model::MMI::output1", "vertices", V_output1)
    mmi.setnamed("::model::MMI::output2", "vertices", V_output2)


    

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

    index_data = mmi.getresult("index_monitor","index profile")
    x_index = index_data['x']   
    
    y_index = index_data['y']
    
    index = index_data['index_x']
    print("index derived!")


    mmi.setemeanalysis("propagation sweep",1)
    mmi.setemeanalysis("parameter","group span 2")
    mmi.setemeanalysis("start",6e-6)
    mmi.setemeanalysis("stop",8e-6)
    mmi.setemeanalysis("number of points",41)


    s=mmi.getemesweep('S')
    print("EME sweep completed.")
    print("S-parameters shape:", s['s21'].shape)
    mmi.save(f"my_own_mmi_taper_width_{width*1e9}")
    mmi.close()
    


    # part4: save the data
    s21=s['s21']
    length=s['group_span_2']

    sio.savemat(f'results_matlab_taper_width_{width*1e9}.mat', {'length': length, 's21': s21,'Emag':Emag, 'x': x, 'y': y,'E':E,'index':index,'x_index':x_index,'y_index':y_index})



print("All simulations completed and data saved.")