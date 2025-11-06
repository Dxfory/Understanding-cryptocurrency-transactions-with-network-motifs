import raphtory
import pandas as pd


def find_motif_counts(graph, deltas):
    """
    使用Raphtory API查找不同时间窗口下的三节点时间模式，并返回每种模式的计数。

    Args:
        graph (GraphView): 已构建的Raphtory图对象。
        deltas (list[int]): 最大时间差值，定义时间窗口。

    Returns:
        list: 每种模式的计数，按顺序给出，总共40种模式。
    """
    print("开始查找所有时间模式...")

    # 使用Raphtory API获取每个时间窗口下的模式计数
    motif_counts = raphtory.algorithms.global_temporal_three_node_motif_multi(graph, deltas)

    # 创建一个用于存储模式计数的列表
    all_motif_counts = []

    total_deltas = len(deltas)

    # 遍历时间窗口中的模式计数
    for i, delta_motif_counts in enumerate(motif_counts):
        # 只取前40个元素，因为每个返回的数组包含40个模式的计数
        all_motif_counts.append(delta_motif_counts)


    print(f"找到的所有模式计数: {len(all_motif_counts)}")

    # 返回所有模式计数的列表
    return all_motif_counts


def save_motif_counts(motif_counts, filename="motif_counts.csv"):
    """
    将模式计数结果保存为 CSV 文件。

    Args:
        motif_counts (list): 每个时间窗口下的40维模式计数。
        filename (str): 保存的文件名。
    """
    # 将模式计数转换为DataFrame以便保存
    columns = [f"Motif{i + 1}" for i in range(40)]  # 40个模式
    motif_df = pd.DataFrame(motif_counts, columns=columns)

    # 保存为CSV文件
    motif_df.to_csv(filename, index=False)
    print(f"模式计数数据已保存至 '{filename}'。")


