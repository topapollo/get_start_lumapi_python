import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

# load the data
data = sio.loadmat('results_matlab.mat')
length = data['length'].flatten()  # 将长度展平为一维数组
s21 = data['s21'].flatten()  # 将 S21 参数展平为一维数组
s21_abs = np.abs(s21)*np.abs(s21)
s21_phase = np.angle(s21, deg=True)  # 相位转换为度

# part5: plot the figures
plt.figure(figsize=(12, 6))

# 绘制幅值
plt.subplot(121)
plt.plot(length, s21_abs)
plt.xlabel('Length (m)')
plt.ylabel('|S21|')
plt.title('S21 Amplitude')
plt.grid(True)

# 绘制相位
plt.subplot(122)
plt.plot(length, s21_phase)
plt.xlabel('Length (m)')
plt.ylabel('Phase (degrees)')
plt.title('S21 Phase')
plt.grid(True)

plt.tight_layout()
plt.savefig('s21_analysis.png')
plt.show()