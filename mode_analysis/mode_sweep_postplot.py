import numpy as np
import matplotlib.pyplot as plt
import mat73
from scipy.interpolate import interp1d

# 设置全局字体样式
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']
plt.rcParams['font.size'] = 16
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

data = mat73.loadmat('mode_analysis\mode_sweep_result.mat')
# Extract the data from the loaded dictionary
width = data['W'].flatten()*1e6
n_TE0 = data['n0'].flatten()
n_TM1 = data['n1'].flatten()
L_beating = data['L_MMI'].flatten()*1e6
est_MMI_length = L_beating*3/8
P_TE = data['P_TE']

# Find the specific values at width = 2.28um and 3.04um
target_widths = [2.28, 3.04]

# Use interpolation to find exact values
interp_n_TE0 = interp1d(width, n_TE0, kind='linear')
interp_n_TM1 = interp1d(width, n_TM1, kind='linear')
interp_L_beating = interp1d(width, L_beating, kind='linear')
interp_est_MMI = interp1d(width, est_MMI_length, kind='linear')

# Get the values at target widths
for target_width in target_widths:
    if target_width >= min(width) and target_width <= max(width):
        n_te0_val = interp_n_TE0(target_width)
        n_tm1_val = interp_n_TM1(target_width)
        l_beat_val = interp_L_beating(target_width)
        est_mmi_val = interp_est_MMI(target_width)
        
        print(f"At width = {target_width} μm:")
        print(f"  TE0 index: {n_te0_val:.4f}")
        print(f"  TM1 index: {n_tm1_val:.4f}")
        print(f"  Beating length: {l_beat_val:.4f} μm")
        print(f"  Estimated MMI length: {est_mmi_val:.4f} μm")
    else:
        print(f"Width {target_width} μm is outside the data range ({min(width):.2f}-{max(width):.2f} μm)")

# 增加图形高度以提供更多垂直空间，减小图形数量占比
plt.figure(figsize=(12, 14))

# Colors for target widths
target_colors = ['#FF5733', '#33A2FF']  # Orange and blue

# First subplot - Effective Index
plt.subplot(3, 1, 1)
plt.plot(width, n_TE0, 'b-o', linewidth=2, markersize=4, label='TE0')
plt.plot(width, n_TM1, 'r--s', linewidth=2, markersize=4, label='TM1')

# Add vertical lines and markers for target widths
for i, (target_width, color) in enumerate(zip(target_widths, target_colors)):
    if target_width >= min(width) and target_width <= max(width):
        # Add vertical line
        plt.axvline(x=target_width, color=color, linestyle='--', alpha=0.7, 
                    label=f'Width = {target_width} μm')
        # Add markers at intersection points
        plt.plot(target_width, interp_n_TE0(target_width), 'o', color=color, 
                markersize=8, markeredgecolor='k', markeredgewidth=1.5)
        plt.plot(target_width, interp_n_TM1(target_width), 'o', color=color, 
                markersize=8, markeredgecolor='k', markeredgewidth=1.5)

plt.xlabel('Width (μm)')
plt.ylabel('Effective Index')
plt.title('Effective Index vs Width')
plt.legend(fontsize=12, frameon=True, facecolor='white', edgecolor='gray')
plt.grid(True, linestyle='--', alpha=0.7)

# Second subplot - Beating Length
plt.subplot(3, 1, 2)
plt.plot(width, L_beating, 'g-^', linewidth=2, markersize=5)

# Add vertical lines and markers
for i, (target_width, color) in enumerate(zip(target_widths, target_colors)):
    if target_width >= min(width) and target_width <= max(width):
        plt.axvline(x=target_width, color=color, linestyle='--', alpha=0.7)
        plt.plot(target_width, interp_L_beating(target_width), 'o', color=color, 
                markersize=8, markeredgecolor='k', markeredgewidth=1.5)

plt.xlabel('Width (μm)')
plt.ylabel('Beating Length (μm)')
plt.title('Beating Length vs Width')
plt.grid(True, linestyle='--', alpha=0.7)

# Third subplot - Estimated MMI Length
plt.subplot(3, 1, 3)
plt.plot(width, est_MMI_length, 'm-D', linewidth=2, markersize=5)

# Add vertical lines and markers
for i, (target_width, color) in enumerate(zip(target_widths, target_colors)):
    if target_width >= min(width) and target_width <= max(width):
        plt.axvline(x=target_width, color=color, linestyle='--', alpha=0.7)
        plt.plot(target_width, interp_est_MMI(target_width), 'o', color=color, 
                markersize=8, markeredgecolor='k', markeredgewidth=1.5)
        
        # Add text annotation with the y-value (est. MMI length)
        plt.annotate(f'{interp_est_MMI(target_width):.2f} μm', 
                    xy=(target_width, interp_est_MMI(target_width)),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7))
        
        # Add text annotation with the x-value (width)
        plt.annotate(f'Width: {target_width} μm', 
                    xy=(target_width, interp_est_MMI(target_width)),
                    xytext=(10, -30), textcoords='offset points',
                    fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', fc=color, alpha=0.7))

plt.xlabel('Width (μm)')
plt.ylabel('Estimated MMI Length (μm)')
plt.title('Estimated MMI Length vs Width')
plt.grid(True, linestyle='--', alpha=0.7)

# 增加子图之间的垂直间距
plt.tight_layout(pad=3.0)  # 增加内边距值
plt.subplots_adjust(hspace=0.4)  # 增加高度间距

# 保存图表（可选）
# plt.savefig('mmi_analysis.png', dpi=300, bbox_inches='tight')

plt.show()