import matplotlib.pyplot as plt
import numpy as np
import json
import math

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


def get_data(prompt_method, model):
    with open(f"./compare/compare_{prompt_method}_{model}.json", "r") as fs:
        # with open(f"failure_{prompt_method}_{model}.json", "r") as fs:
        data = json.loads(fs.read())
        tmp = []
        for key in data.keys():
            # print(key)
            web_number = key.split("/")[0]
            # print(web_number)

            # if int(web_number) > 100:
            #     continue
            if model == "gpt" or "72B" in model:
                if int(web_number) >= 46:
                    continue
            tmp.append(data[key])

        # data = np.array(list(data.values()))
        data = np.array(tmp)

        # print(data)

        data = data[0:-1]

        total = len(data)

        # print(total)

        # 使用numpy.unique()函数获取元素计数
        unique_elements, counts = np.unique(data, return_counts=True)

        # 打印每个元素及其计数
        for element, count in zip(unique_elements, counts):
            # print(f"元素 {element} 的计数为 {count}")
            if element == 0:
                win = count
            if element == 1:
                tie = count
            if element == 2:
                lose = count
        win = math.ceil(win * 100 / total)
        tie = math.ceil(tie * 100 / total)
        lose = 100 - win - tie
        print(win, tie, lose)
        return win, tie, lose
        # print(win * 100 / total, tie * 100 / total, lose * 100 / total)
        # return win * 100 / total, tie * 100 / total, lose * 100 / total


def plot_compare(wins, ties, losses):
    # models = [
    #     'Gemini (CoT)',
    #     'Gemini (Mark)',
    #     'GPT-4o (Direct)',
    #     'GPT-4o (CoT)',
    #     'GPT-4o (Mark)',
    #     'Claude (Direct)',
    #     'Claude (CoT)',
    #     'Claude (Mark)',
    # ]

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
    # wins = np.array([63, 68, 76, 34, 45, 54, 38])
    # ties = np.array([11, 14, 9, 26, 16, 11, 25])
    # losses = np.array([26, 18, 15, 40, 39, 35, 37])

    # wins = np.array([32, 32, 40, 42, 51, 47, 46, 53])
    # ties = np.array([50, 53, 57, 54, 46, 48, 50, 44])
    # loses = np.array([18, 15, 3, 4, 3, 5, 4, 3])

    # wins = np.array([9, 8, 9, 20, 15, 21, 54, 59, 63, 32, 32, 61, 65, 64, 47, 46, 53])
    # ties = np.array([36, 39, 37, 39, 52, 46, 26, 26, 20, 51, 53, 27, 25, 24, 48, 50, 44])
    # loses = np.array([55, 53, 54, 41, 33, 33, 20, 15, 17, 17, 15, 12, 10, 12, 5, 4, 3])

    wins = np.array(wins)
    ties = np.array(ties)
    loses = np.array(losses)
    # 反转数组顺序
    wins = wins[::-1]
    ties = ties[::-1]
    losses = loses[::-1]

    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 11))

    # 绘制堆叠条形图
    height = 0.8
    y_pos = np.arange(len(models))
    ax.barh(y_pos, wins, color='#4B6BED', label='Win', height=height)
    ax.barh(y_pos, ties, left=wins, color='#7BB5ED', label='Tie', height=height)
    ax.barh(y_pos, losses, left=wins + ties, color='#ED7B7B', label='Lose', height=height)

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

        # Lose percentage
        if losses[i] > 0:
            ax.text(wins[i] + ties[i] + losses[i] / 2, i, f'{losses[i]}%',
                    va='center', ha='center', color='white', fontsize=20)

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
    plt.savefig("compare.pdf")
    plt.show()


def plot_usable():
    models = [
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
    wins = np.array([45, 49, 56, 66, 68, 78, 70, 69, 83])
    ties = np.array([55, 51, 44, 34, 32, 22, 30, 31, 17])

    # 反转数组顺序
    wins = wins[::-1]
    ties = ties[::-1]

    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 8))

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
    plt.savefig("../figure/usable.pdf")
    plt.show()


# win, tie, lose = get_data()
#
# win = 68
# tie = 19
# lose = 100-win-tie
#
# num = 3
# # plot(models="", wins=np.array([win]*num), ties=np.array([tie]*num), loses=np.array([lose]*num))
#
# plot(models="", wins=np.array([68, 70, 75]), ties=np.array([19, 15, 14]), loses=np.array([13, 15, 11]))


if __name__ == '__main__':

    model_names = ["qwen-vl-3B", "qwen-vl-7B", "qwen-vl-72B",
                   "gemini", "gpt", "claude"]
    prompt_names = ["direct_prompt", "cot_prompt", "mark_prompt"]

    wins = []
    ties = []
    losses = []
    for model_name in model_names:
        for prompt_name in prompt_names:
            if model_name == "gemini" and prompt_name == "direct_prompt":
                continue
            else:
                print(model_name, prompt_name)
                win, tie, lose = get_data(prompt_method=prompt_name, model=model_name)
                wins.append(win)
                ties.append(tie)
                losses.append(lose)
    print(wins)
    print(ties)
    print(losses)

    # get_data(prompt_method="cot_prompt", model="gemini")
    # get_data(prompt_method="mark_prompt", model="gemini")
    #
    # get_data(prompt_method="direct_prompt", model="gpt")
    # get_data(prompt_method="cot_prompt", model="gpt")
    # get_data(prompt_method="mark_prompt", model="gpt")
    #
    # get_data(prompt_method="direct_prompt", model="claude")
    # get_data(prompt_method="cot_prompt", model="claude")
    # get_data(prompt_method="mark_prompt", model="claude")
    #
    plot_usable()

    plot_compare(wins, ties, losses)

    # plot()
