import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

# load the data
data = sio.loadmat('results_matlab.mat')
length = data['length'].flatten()  # 将长度展平为一维数组
s21 = data['s21'].flatten()  # 将 S21 参数展平为一维数组
s21_abs = np.abs(s21)*np.abs(s21)
s21_phase = np.angle(s21, deg=True)  # 相位转换为度

# Find the maximum S21 point
max_idx = np.argmax(s21_abs)
max_s21 = s21_abs[max_idx]
max_length = length[max_idx]

# Print the maximum value and corresponding length
print(f"Maximum |S21|²: {max_s21:.6f} at length = {max_length:.6e} m")

# part5: plot the figures
plt.figure(figsize=(12, 6))

# 绘制幅值
plt.subplot(121)
plt.plot(length, s21_abs)
# Mark the maximum point with a red circle
plt.plot(max_length, max_s21, 'ro', markersize=8)
plt.xlabel('Length (m)')
plt.ylabel('|S21|²')
plt.title('1to2 MMI |S21|²')
plt.grid(True)
# Annotate the maximum point
plt.annotate(f'Max: |S21|²={max_s21:.6f}\nLength: {max_length*1e6:.4f} um', 
             xy=(max_length, max_s21), 
             xytext=(max_length+0.1*(max(length)-min(length)), 
                     max_s21-0.2*(max(s21_abs)-min(s21_abs))),
             arrowprops=dict(facecolor='black', shrink=0.05),
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7))

plt.annotate(f'MMI Length: {max_length*1e6:.4f} um,\n MMI width: 2.28 um, \n with taper width: 0.76 um',
             xy=(max_length-0.3*(max(length)-min(length)), max_s21-0.7*(max(s21_abs)-min(s21_abs))))

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