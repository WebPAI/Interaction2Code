import json
import math
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from matplotlib import cm

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


def process_failure(prompt, model):
    # with open(f"failure/failure_{prompt}_{model}.json", "r") as fs:
    with open(f"failure/failure_{prompt}_{model}.json", "r") as fs:
        data = json.loads(fs.read())

    data = list(data.values())
    usable = []
    failure_type = []
    failure_and_usable = []
    for item in data:
        failure_and_usable.append(item)
        item = item.split("/")
        usable.append(item[1])
        failure_type.append(item[0])

    usable = Counter(usable)
    failure_type = Counter(failure_type)

    failure_and_usable = Counter(failure_and_usable)
    res = []
    for i in range(1, 11):
        failure_use = f'{i}/0'
        failure_unuse = f'{i}/1'

        if failure_use in failure_and_usable:
            failure_use = failure_and_usable[failure_use]
        else:
            failure_use = 0

        if failure_unuse in failure_and_usable:
            failure_unuse = failure_and_usable[failure_unuse]
        else:
            failure_unuse = 0

        # res.append((i, failure_use/(failure_use+failure_unuse), 1-failure_use/(failure_use+failure_unuse)))

        # if failure_use == 0 and failure_unuse == 0:
        #     res.append((i, 0, 0))
        # else:
        #     res.append(
        #         (i, failure_use / (failure_use + failure_unuse), 1 - failure_use / (failure_use + failure_unuse)))

        res.append((i, failure_use, failure_unuse))

    usable_rate = math.ceil(usable['0'] * 100 / (usable['0'] + usable['1']))
    print(usable, usable_rate, 100 - usable_rate)

    total_sample = 0

    failure_res = []
    for key in failure_type:
        total_sample += failure_type[key]
    for i in range(0, 11):
        if str(i) in failure_type:
            failure_res.append(round(failure_type[str(i)] * 100 / total_sample, 2))
        else:
            failure_res.append(0)

    # print(failure_type, total_sample)
    # print(failure_res)
    # tmp = sorted(failure_res, reverse=True)
    # print(sum(tmp[1:4]) / (100 - tmp[0]))

    print(failure_and_usable)
    print(res)
    return failure_res, res


def plot_usable():
    models = [
        'Qwen-3B (Direct)',
        'Qwen-3B (CoT)',
        'Qwen-3B (Mark)',
        'Qwen-7B (Direct)',
        'Qwen-7B (CoT)',
        'Qwen-7B (Mark)',
        'Qwen-72B (Direct)',
        'Qwen-72B (CoT)',
        'Qwen-72B (Mark)',
        'Gemini (Direct)',
        'Gemini (CoT)',
        'Gemini (Mark)',
        'GPT-4o (Direct)',
        'GPT-4o (CoT)',
        'GPT-4o (Mark)',
        'Claude (Direct)',
        'Claude (CoT)',
        'Claude (Mark)',
    ]

    # 反转列表顺序使图表从上到下显示
    models.reverse()

    # 胜率数据
    # wins = np.array([45, 49, 56, 66, 68, 78, 70, 69, 83])
    # ties = np.array([55, 51, 44, 34, 32, 22, 30, 31, 17])

    wins = np.array([17, 19, 18, 30, 22, 32, 41, 43, 54, 47, 53, 64, 73, 74, 81, 66, 69, 77])
    ties = np.array([83, 81, 82, 70, 78, 68, 59, 57, 46, 53, 47, 36, 27, 26, 19, 34, 31, 23])

    # 反转数组顺序
    wins = wins[::-1]
    ties = ties[::-1]

    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 11))

    # 绘制堆叠条形图
    height = 0.8
    y_pos = np.arange(len(models))
    ax.barh(y_pos, wins, color='#4B6BED', label='Usable', height=height)
    # ax.barh(y_pos, ties, left=wins, color='#7BB5ED', label='Tie', height=height)
    ax.barh(y_pos, ties, left=wins, color='#ED7B7B', label='Unusable', height=height)
    # ax.barh(y_pos, losses, left=wins + ties, color='#ED7B7B', label='Lose', height=height)

    # 在条形上添加百分比标签
    for i in range(len(models)):
        # Win percentage
        if wins[i] > 0:
            ax.text(wins[i] / 2, i, f'{wins[i]}%',
                    va='center', ha='center', color='white', fontsize=20)

        # Tie percentage
        if ties[i] > 0:
            ax.text(wins[i] + ties[i] / 2, i, f'{ties[i]}%',
                    va='center', ha='center', color='black', fontsize=20)

        # # Lose percentage
        # if losses[i] > 0:
        #     ax.text(wins[i] + ties[i] + losses[i] / 2, i, f'{losses[i]}%',
        #             va='center', ha='center', color='white', fontsize=20)

    # 设置图表样式
    ax.set_yticks(y_pos)
    ax.set_yticklabels(models)
    ax.set_xlabel('Percentage (%)', fontsize=20)
    ax.set_xlim(0, 100)

    # 添加图例
    plt.legend(bbox_to_anchor=(0.2, 1.1), loc='center left', ncol=3, fontsize=25, frameon=False)
    # plt.legend(loc='upper center', ncol=3, fontsize=20, frameon=False)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    # plt.xlabel(fontsize=20)
    # plt.(fontsize=20)

    # 设置标题和布局
    plt.tight_layout()
    plt.savefig("usable.pdf")
    plt.show()


def plot_failure(data, file_name):
    # 准备数据
    data = {
        'Error Type': [
            'No failure',
            'Interactive element missing',
            'No interaction',
            'Wrong type of interactive element',
            'Wrong interactive element',
            'Wrong position of interactive element',
            'Wrong position after interaction',
            'Wrong type of interaction effects',
            'Effect on wrong element',
            'Partial Implementation',
            'Wrong function'
        ],
        # 'Percentage': [16.9, 11.27, 37.09, 2.82, 7.51, 0.47, 3.76, 0, 0.94, 8.45, 10.8]
        'Percentage': data
    }

    # 创建DataFrame并排序
    df = pd.DataFrame(data)
    df = df.sort_values('Percentage', ascending=True).reset_index(drop=True)

    # 设置图形大小
    plt.figure(figsize=(15, 7))
    max_value = df['Percentage'].max()

    # norm = plt.Normalize(-1, 1)
    # norm_values = norm(df['Percentage'])
    # map_vir = cm.get_cmap(name='inferno')
    # colors = map_vir(norm_values)

    colors = [mcolors.to_rgba('steelblue', alpha=0.1 + 0.9 * (value / max_value))
              for value in df['Percentage']]

    print(colors)

    # 创建横向柱状图，不显示y轴标签
    bars = plt.barh(range(len(df['Error Type'])), df['Percentage'],
                    color='steelblue', alpha=0.8)

    # bars = plt.barh(range(len(df['Error Type'])), df['Percentage'],
    #                 color=colors, alpha=0.8)

    # 移除y轴刻度标签
    plt.yticks([])

    # 为每个条形添加标签
    for i, (bar, error_type) in enumerate(zip(bars, df['Error Type'])):
        width = bar.get_width()

        # 添加错误类型标签（在条形图内部）
        plt.text(27, bar.get_y() + bar.get_height() / 2,
                 f'{error_type}',
                 va='center', ha='left', style='italic',
                 color='black' if width > 5 else 'black',
                 fontsize=20)
        # plt.text(28, bar.get_y() + bar.get_height() / 2,
        #          f'{error_type}',
        #          va='center', ha='left', style='italic',
        #          color='black' if width > 5 else 'black',
        #          fontsize=20)
        # plt.text(19, bar.get_y() + bar.get_height() / 2,
        #          f'{error_type}',
        #          va='center', ha='left', style='italic',
        #          color='black' if width > 5 else 'black',
        #          fontsize=20)

        # 添加百分比标签（在条形图右侧）
        plt.text(width, bar.get_y() + bar.get_height() / 2,
                 f'{width}%',
                 va='center', ha='left', fontsize=20)

    # 添加标题
    # plt.title('Error Types Distribution', pad=20)
    plt.xlabel('Percentage (%)', fontsize=20)

    # 添加网格线
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # 设置x轴范围，留出空间显示百分比标签
    # plt.xlim(0, max(df['Percentage']) * 1.2)
    plt.xlim(0, max(df['Percentage']) * 1.1)
    plt.xticks(fontsize=20)
    # 调整布局
    plt.tight_layout()
    # plt.savefig("failure.pdf")
    plt.savefig("./figure/" + file_name)
    # 显示图表
    plt.show()


# def plot_failure():
#     models = [
#         'Interactive element missing',
#         'No interaction',
#         'Wrong type of interactive element',
#         'Wrong interactive element',
#         'Wrong position of interactive element',
#         'Wrong position after interaction',
#         'Wrong type of interaction effects',
#         'Effect on wrong element',
#         'Partial Implementation',
#         'Wrong function'
#     ]
#
#     # 反转列表顺序使图表从上到下显示
#     models.reverse()
#
#     # 胜率数据
#     # wins = np.array([3.62, 49, 56, 66, 68, 78, 70, 69, 83])
#     # ties = np.array([, 51, 44, 34, 32, 22, 30, 31, 17])
#
#     wins = np.array([0, 6.93, 88.89, 91.96, 97.83, 93.81, 55.88, 0, 75.29, 0])
#     ties = np.array([100, 93.07, 11.11, 8.04, 2.17, 6.19, 44.12, 100, 24.71, 100])
#
#     # 反转数组顺序
#     wins = wins[::-1]
#     ties = ties[::-1]
#
#     # 创建图表
#     fig, ax = plt.subplots(figsize=(16, 8))
#
#     # 绘制堆叠条形图
#     height = 0.8
#     y_pos = np.arange(len(models))
#     ax.barh(y_pos, wins, color='#4B6BED', label='Usable', height=height)
#     # ax.barh(y_pos, ties, left=wins, color='#7BB5ED', label='Tie', height=height)
#     ax.barh(y_pos, ties, left=wins, color='#ED7B7B', label='Unusable', height=height)
#     # ax.barh(y_pos, losses, left=wins + ties, color='#ED7B7B', label='Lose', height=height)
#
#     # 在条形上添加百分比标签
#     for i in range(len(models)):
#         # Win percentage
#         if wins[i] > 0:
#             ax.text(wins[i] / 2, i, f'{wins[i]}%',
#                     va='center', ha='center', color='white', fontsize=20)
#
#         # Tie percentage
#         if ties[i] > 0:
#             ax.text(wins[i] + ties[i] / 2, i, f'{ties[i]}%',
#                     va='center', ha='center', color='black', fontsize=20)
#
#         # # Lose percentage
#         # if losses[i] > 0:
#         #     ax.text(wins[i] + ties[i] + losses[i] / 2, i, f'{losses[i]}%',
#         #             va='center', ha='center', color='white', fontsize=20)
#
#     # 设置图表样式
#     ax.set_yticks(y_pos)
#     ax.set_yticklabels(models)
#     ax.set_xlabel('Percentage (%)', fontsize=20)
#     ax.set_xlim(0, 100)
#
#     # 添加图例
#     plt.legend(bbox_to_anchor=(0.2, 1.1), loc='center left', ncol=3, fontsize=25, frameon=False)
#     # plt.legend(loc='upper center', ncol=3, fontsize=20, frameon=False)
#     plt.xticks(fontsize=20)
#     plt.yticks(fontsize=20)
#     # plt.xlabel(fontsize=20)
#     # plt.(fontsize=20)
#
#     # 设置标题和布局
#     plt.tight_layout()
#     plt.savefig("../figure/usable_failure.pdf")
#     plt.show()


if __name__ == '__main__':
    # process_failure(prompt="direct_prompt", model="gemini")
    # print("---------------------------------------------")
    # process_failure(prompt="cot_prompt", model="gemini")
    # print("---------------------------------------------")
    # process_failure(prompt="mark_prompt", model="gemini")
    # print("---------------------------------------------")
    # process_failure(prompt="direct_prompt", model="gpt")
    # print("---------------------------------------------")
    # process_failure(prompt="cot_prompt", model="gpt")
    # print("---------------------------------------------")
    # process_failure(prompt="mark_prompt", model="gpt")
    # print("---------------------------------------------")
    # process_failure(prompt="direct_prompt", model="claude")
    # print("---------------------------------------------")
    # process_failure(prompt="cot_prompt", model="claude")
    # print("---------------------------------------------")
    # process_failure(prompt="mark_prompt", model="claude")

    data10, res10 = process_failure(prompt="direct_prompt", model="qwen-vl-3B")
    data11, res11 = process_failure(prompt="cot_prompt", model="qwen-vl-3B")
    data12, res12 = process_failure(prompt="mark_prompt", model="qwen-vl-3B")

    data13, res13 = process_failure(prompt="direct_prompt", model="qwen-vl-7B")
    data14, res14 = process_failure(prompt="cot_prompt", model="qwen-vl-7B")
    data15, res15 = process_failure(prompt="mark_prompt", model="qwen-vl-7B")

    data16, res16 = process_failure(prompt="direct_prompt", model="qwen-vl-72B")
    data17, res17 = process_failure(prompt="cot_prompt", model="qwen-vl-72B")
    data18, res18 = process_failure(prompt="mark_prompt", model="qwen-vl-72B")

    data1, res1 = process_failure(prompt="direct_prompt", model="gemini")
    data2, res2 = process_failure(prompt="cot_prompt", model="gemini")
    data3, res3 = process_failure(prompt="mark_prompt", model="gemini")

    data4, res4 = process_failure(prompt="direct_prompt", model="gpt")
    data5, res5 = process_failure(prompt="cot_prompt", model="gpt")
    data6, res6 = process_failure(prompt="mark_prompt", model="gpt")

    data7, res7 = process_failure(prompt="direct_prompt", model="claude")
    data8, res8 = process_failure(prompt="cot_prompt", model="claude")
    data9, res9 = process_failure(prompt="mark_prompt", model="claude")

    results = [res1, res2, res3, res4, res5, res6, res7, res8, res9]

    total_res = []

    tmp1 = []
    tmp2 = []
    for i in range(0, 10):
        total_use = 0
        total_unuse = 0

        for res in results:
            # print(res[i])
            total_use += res[i][1]
            total_unuse += res[i][2]

        tmp = round(100 * total_use / (total_use + total_unuse), 2)
        tmp1.append(tmp)
        tmp2.append(round(100 - tmp, 2))
        total_res.append((tmp, round(100 - tmp, 2)))

    # print(total_res)
    # print(tmp1)
    # print(tmp2)

    # plot_usable()

    # data = np.array([data1, data2, data3, data4, data5, data6, data7, data8, data9])
    # print(np.sum(data, axis=0))

    # data1 = np.array([data1, data2, data3])
    # data2 = np.array([data4, data5, data6])
    # data3 = np.array([data7, data8, data9])
    # data4 = np.array([data10, data11, data12])
    # data5 = np.array([data13, data14, data15])
    # data6 = np.array([data16, data17, data18])
    #
    # data1 = np.round(np.sum(data1, axis=0) * 100 / 300, 2)
    # data2 = np.round(np.sum(data2, axis=0) * 100 / 300, 2)
    # data3 = np.round(np.sum(data3, axis=0) * 100 / 300, 2)
    #
    #
    # data4 = np.round(np.sum(data4, axis=0) * 100 / 300, 2)
    # data5 = np.round(np.sum(data5, axis=0) * 100 / 300, 2)
    # data6 = np.round(np.sum(data6, axis=0) * 100 / 300, 2)

    # plot_failure(data1, "gemini_failure.pdf")
    # plot_failure(data2, "gpt_failure.pdf")
    # plot_failure(data3, "claude_failure.pdf")

    plot_failure(data4, "qwen3B_failure.pdf")
    plot_failure(data5, "qwen7B_failure.pdf")
    plot_failure(data6, "qwen72B_failure.pdf")

    plot_failure(data1, "gemini1.pdf")
    plot_failure(data2, "gemini2.pdf")
    plot_failure(data3, "gemini3.pdf")
    plot_failure(data4, "gpt1.pdf")
    plot_failure(data5, "gpt2.pdf")
    plot_failure(data6, "gpt3.pdf")
    plot_failure(data7, "claude1.pdf")
    plot_failure(data8, "claude2.pdf")
    plot_failure(data9, "claude3.pdf")

    # plot_failure()
