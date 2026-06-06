import numpy as np
import matplotlib
import matplotlib.pyplot as plt

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


def get_data():
    clip = [
        [0, 0.381, 0.75, 0.768, 0.832],
        [],
        [],
        []
    ]

    ssim = [
        [0, 0.2325, 0.7653, 0.679, 0.780],
        [],
        [],
        []
    ]

    text = [
        [0, 0.1835, 0.4376, 0.349, 0.5773],
        [],
        [],
        []
    ]

    pose = [
        [0, 0.3726, 0.42, 0.703, 0.695],
        [],
        [],
        []
    ]

    posi = [
        [0, 0.3365, 0.411, 0.512, 0.6005],
        [],
        [],
        []
    ]
    return clip, ssim, text, pose, posi


def plot_scale():
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示
    # plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 创建x轴数据
    x = np.array([1, 1.5, 2, 2.5, 3])

    # 创建5条线的y轴数据
    # y1 = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
    # y2 = np.array([0.15, 0.32, 0.48, 0.65, 0.85])
    # y3 = np.array([0.2, 0.35, 0.45, 0.6, 0.8])
    # y4 = np.array([0.25, 0.38, 0.52, 0.68, 0.75])
    # y5 = np.array([0.3, 0.42, 0.55, 0.7, 0.82])

    clip, ssim, text, pose, posi = get_data()
    y1 = np.array(clip[0])
    y2 = np.array(ssim[0])
    y3 = np.array(text[0])
    # y4 = np.array(pose[0])
    y5 = np.array(posi[0])

    # 设置图形大小
    plt.figure(figsize=(14, 6))

    # 绘制五条线
    # plt.plot(x, y1, 'o-', color='#8884d8', linestyle='--', linewidth=3, label='CLIP', markersize=10)
    # plt.plot(x, y2, 's-', color='#82ca9d', linestyle='--', linewidth=3, label='SSIM', markersize=10)
    # plt.plot(x, y3, '^-', color='#ffc658', linestyle='--', linewidth=3, label='Text', markersize=10)
    # plt.plot(x, y4, 'D-', color='#ff7300', linestyle='--', linewidth=3, label='Pos$_e$', markersize=10)
    # plt.plot(x, y5, 'v-', color='#0088fe', linestyle='--', linewidth=3, label='Pos$_i$', markersize=10)

    # plt.plot(x, y1, 'o-', linestyle='--', linewidth=3, label='CLIP', markersize=10)
    # plt.plot(x, y2, 's-', linestyle='--', linewidth=3, label='SSIM', markersize=10)
    # plt.plot(x, y3, '^-', linestyle='--', linewidth=3, label='Text', markersize=10)
    # # plt.plot(x, y4, 'D-', linestyle='--', linewidth=3, label='Pos$_e$', markersize=10)
    # plt.plot(x, y5, 'v-', linestyle='--', linewidth=3, label='Position', markersize=10)

    plt.plot(x, y1, 'o-', linewidth=3, label='CLIP', markersize=20)
    plt.plot(x, y2, 's-', linewidth=3, label='SSIM', markersize=20)
    plt.plot(x, y3, '^-', linewidth=3, label='Text', markersize=20)
    # plt.plot(x, y4, 'D-', linestyle='--', linewidth=3, label='Pos$_e$', markersize=10)
    plt.plot(x, y5, 'v-', linewidth=3, label='Position', markersize=20)

    # 设置图表标题和轴标签
    # plt.title('多条折线图示例', fontsize=14, pad=15)
    plt.xlabel('Scale', fontsize=32)
    # plt.ylabel('Metric', fontsize=32)
    plt.xticks(fontsize=32)
    plt.yticks(fontsize=32)

    # 设置刻度范围
    plt.xlim(0.8, 3.1)
    plt.ylim(-0.05, 1)

    # 添加网格线
    plt.grid(True, linestyle='--', alpha=0.7)

    # 添加图例
    plt.legend(loc='best', frameon=False, fancybox=True, shadow=True, fontsize=32)

    # 调整布局
    plt.tight_layout()

    # plt.savefig("scale.pdf")
    plt.savefig("./scale.pdf")

    plt.show()


plot_scale()
