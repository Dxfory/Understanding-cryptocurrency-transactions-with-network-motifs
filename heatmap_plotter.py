import matplotlib.pyplot as plt
from raphtory import plottingutils
import matplotlib


def plot_heatmap(motifs, title, filename):
    """
    绘制并保存热图
    Args:
        motifs: 要绘制的三角形模式数据
        title: 热图标题
        filename: 保存图像的文件名
    """
    fig, ax = plt.subplots(1, 1, figsize=(16, 16))  # 增大图像大小
    plottingutils.global_motif_heatplot(motifs, ax=ax)
    ax.set_title(title)
    plt.tight_layout(pad=4.0)  # 增加填充，避免标签重叠
    plt.savefig(filename, bbox_inches='tight')  # 保存图像
    plt.close()  # 关闭当前图像，避免不同图像之间重叠


def generate_and_save_heatmaps(motifs_original_1h, motifs_randomized_1h, motifs_original_1d, motifs_randomized_1d,
                               deltas):
    """
    生成并保存四个热图，原始图和随机化图在1小时和1天的时间窗口下
    Args:
        motifs_original_1h, motifs_randomized_1h: 原始图和随机化图的1小时三角形模式
        motifs_original_1d, motifs_randomized_1d: 原始图和随机化图的1天三角形模式
        deltas: 时间窗口列表，包含要计算的时间窗口（例如：[3600, 86400]）
    """
    # 绘制并保存原始图的1小时时间三角形模式热图
    plot_heatmap(motifs_original_1h, "原始图 - 1小时时间三角形模式热图", f"original_graph_1h_heatmap_{deltas[0]}.png")

    # 绘制并保存随机化图的1小时时间三角形模式热图
    plot_heatmap(motifs_randomized_1h, "随机化图 - 1小时时间三角形模式热图",
                 f"randomized_graph_1h_heatmap_{deltas[0]}.png")

    # 绘制并保存原始图的1天时间三角形模式热图
    plot_heatmap(motifs_original_1d, "原始图 - 1天时间三角形模式热图", f"original_graph_1d_heatmap_{deltas[1]}.png")

    # 绘制并保存随机化图的1天时间三角形模式热图
    plot_heatmap(motifs_randomized_1d, "随机化图 - 1天时间三角形模式热图",
                 f"randomized_graph_1d_heatmap_{deltas[1]}.png")

import matplotlib.pyplot as plt
# 假设 find_motif_counts、plottingutils.global_motif_heatplot 已在外部正确导入
# from raphtory.analysis import find_motif_counts  # 视你的实际环境而定

def plot_motifs_for_multiple_coins(coin_graphs):
    """
    参数
    ----
    coin_graphs: dict
        键为字符串(币种名称)，值为对应的 Graph 对象。
        例如: {
            "USDT": usdt_graph,
            "USDC": usdc_graph,
            ...
        }
    """

    # 要计算三角形模式的时间窗口：1小时(3600秒)、1天(86400秒)
    deltas = [3600, 86400]

    for coin_name, graph in coin_graphs.items():
        # 1) 计算该 Graph 在两个时间窗口下的三角形模式
        triangle_motifs = find_motif_counts(graph, deltas=deltas)
        # triangle_motifs 应该返回一个列表/元组，triangle_motifs[0] 表示1小时结果, [1]表示1天结果

        # 2) 绘制该币种的1小时三角形模式热图
        fig, ax = plt.subplots()
        ax = plottingutils.global_motif_heatplot(triangle_motifs[0], cmap="YlGnBu")
        ax.set_title(f"{coin_name} Graph - 1 Hour Temporal Motifs Heatmap")
        plt.savefig(f"{coin_name}_1h_motifs_heatmap.png")
        plt.show()

        # 3) 绘制该币种的1天三角形模式热图
        fig, ax = plt.subplots()
        ax = plottingutils.global_motif_heatplot(triangle_motifs[1], cmap="YlGnBu")
        ax.set_title(f"{coin_name} Graph - 1 Day Temporal Motifs Heatmap")
        plt.savefig(f"{coin_name}_1d_motifs_heatmap.png")
        plt.show()

    print("所有币种的三角形模式热图已绘制并保存。")
