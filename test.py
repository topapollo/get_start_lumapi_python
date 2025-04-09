import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.constants import c
import scipy.io as sio  # 用于保存 MATLAB 兼容文件
import pickle  # 用于保存 Python 对象

# 添加 Lumerical API 路径
sys.path.append(r"C:\Program Files\Lumerical\v241\api\python\\")
import lumapi

mmi = lumapi.MODE("my_own_MMI_script.lsf")
mmi.save("my_own_mmi")
mmi.run()
mmi.feval("emesweep.lsf")
# 从 Lumerical 获取数据
s=mmi.getemesweep('S')
mmi.close()
print("Value of s:", s)
# 提取需要的数据
s51=s['s51']
length=s['group_span_2']




# 方法 1：保存为 MATLAB 格式 (.mat)
sio.savemat('results_matlab.mat', {'length': length, 's51': s51})

# 方法 2：保存为 NumPy 格式 (.npz)
np.savez('results_numpy.npz', length=length, s51=s51)

# 方法 3：保存为 Python pickle 格式 (.pkl)
with open('results_pickle.pkl', 'wb') as f:
    pickle.dump({'length': length, 's51': s51}, f)

# 数据处理示例
# 提取 s51 的幅值和相位
s51_abs = np.abs(s51)
s51_phase = np.angle(s51, deg=True)  # 相位转换为度

# 绘图
plt.figure(figsize=(12, 6))

# 绘制幅值
plt.subplot(121)
plt.plot(length, s51_abs)
plt.xlabel('Length (m)')
plt.ylabel('|S51|')
plt.title('S51 Amplitude')
plt.grid(True)

# 绘制相位
plt.subplot(122)
plt.plot(length, s51_phase)
plt.xlabel('Length (m)')
plt.ylabel('Phase (degrees)')
plt.title('S51 Phase')
plt.grid(True)

plt.tight_layout()
plt.savefig('s51_analysis.png')
plt.show()

print("数据已保存，并完成初步分析")