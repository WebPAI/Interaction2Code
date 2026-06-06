import matplotlib.pyplot as plt
import numpy as np


def plot_pie_chart():

    #
    data = {'homepage': 4, 'study': 3, 'blog': 8, 'business': 6, 'encyclopedia': 3, 'shop': 11, 'sport': 3, 'entertainment': 2, 'content': 1, 'hotel': 4, 'product': 3, 'news': 6, 'library': 1, 'job': 2, 'politico': 1, 'conference': 1, 'report': 1, 'video': 3, 'form': 4, 'education': 1, 'culture': 1, 'social': 1, 'technology': 3, 'finance': 1, 'music': 1, 'government': 3, 'comment': 1, 'book': 6, 'food': 4, 'menu': 1, 'design': 1, 'electronic': 1, 'travel': 2, 'health': 1, 'manufacturer': 1, 'car': 1, 'search': 1, 'home': 1, 'medical': 1}
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    top_categories = dict(list(sorted_data.items())[:15])
    other = sum(list(sorted_data.values())[15:])
    top_categories['Other'] = other

    labels = list(top_categories.keys())
    sizes = list(top_categories.values())

    colors = plt.cm.Spectral(np.linspace(0.1, 0.9, len(labels)))

    fig, ax = plt.subplots(figsize=(12, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels,
                                      # autopct=lambda pct: f'{pct:.1f}%' if pct > 2 else '',
                                      autopct=lambda pct: f'{pct:.0f}%' if pct > 2 else '',
                                      pctdistance=0.75,  # 调整百分比标签的位置
                                      startangle=90, colors=colors,
                                      wedgeprops=dict(width=0.6, edgecolor='black'),
                                      textprops={'fontsize': 25},  # 增大标签字体大小
                                      )
    plt.setp(autotexts, size=25, weight="bold", color="black")

    # 添加图例
    # ax.legend(wedges, labels, fontsize=20,
    #           title="Categories",
    #           loc="center left",
    #           bbox_to_anchor=(1, 0, 0.5, 1))
    # ax.legend(wedges, labels, fontsize=20,
    #           title="Categories",
    #           loc="center left",
    #           bbox_to_anchor=(1, 0, 0.5, 1))

    # 设置标题
    # plt.title("Website Category Distribution", fontsize=20, pad=20)

    plt.axis('equal')

    plt.tight_layout()
    plt.savefig("domain.pdf")
    plt.show()


def plot_interact():
    data = {'color': 26, 'text': 41, 'new component': 37, 'new window': 13, 'size': 5, 'position': 2,
            'switch': 1, 'disappear': 1, 'sidebar': 1, 'list': 2}

    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    top_categories = dict(list(sorted_data.items())[:-1])
    other = sum(list(sorted_data.values())[-1:])
    top_categories['Other'] = other

    labels = list(top_categories.keys())
    sizes = list(top_categories.values())

    colors = plt.cm.Spectral(np.linspace(0.3, 1, len(labels)))

    fig, ax = plt.subplots(figsize=(12, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels,
                                      autopct=lambda pct: f'{pct:.1f}%' if pct > 2 else '',
                                      pctdistance=0.75,  # 调整百分比标签的位置
                                      startangle=90, colors=colors,
                                      wedgeprops=dict(width=0.6, edgecolor='black'),
                                      textprops={'fontsize': 20},  # 增大标签字体大小
                                      )
    plt.setp(autotexts, size=16, weight="bold", color="black")

    # 添加图例
    # ax.legend(wedges, labels, fontsize=20,
    #           title="Categories",
    #           loc="center left",
    #           bbox_to_anchor=(1, 0, 0.5, 1))
    # ax.legend(wedges, labels, fontsize=20,
    #           title="Categories",
    #           loc="center left",
    #           bbox_to_anchor=(1, 0, 0.5, 1))

    # 设置标题
    # plt.title("Website Category Distribution", fontsize=20, pad=20)

    plt.axis('equal')

    plt.tight_layout()
    plt.savefig("interact_type1.pdf")
    plt.show()


# plot_interact()

plot_pie_chart()
