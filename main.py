# from pre_process import preprocess_data
from detail_process import daily_transaction_analysis, highlight_high_transactions
from graph_load import build_transaction_graph
from plot_transactions import plot_transactions_and_values
from motif_analysis import find_motif_counts
from Null_Model import generate_randomized_reference_model
from centrality_analysis import compute_degree_centrality, compute_pagerank, compute_betweenness_centrality,process_centrality_algorithm
from raphtory import plottingutils, algorithms
from classify_by_centrality import classify_nodes_based_on_pagerank_and_degree
import pandas as pd
import logging
import gc
import os
import matplotlib.pyplot as plt


def main():
    raw_data = 'token_transfers_V3.0.0.csv'
    processed_data = 'processed_transactions.csv'

    input_file = 'token_transfers_V3.0.0.csv'
    output_file = 'processed_transactions.csv'
    # Step 1: 数据预处理
    # processed_data = preprocess_data(input_file, output_file)
    # processed_data = pd.read_csv('processed_transactions.csv')

    # Step 2: 每日交易量分析
    daily_transactions = daily_transaction_analysis(processed_data)

    # Step 3: 高峰交易量检测与绘图
    highlight_high_transactions(daily_transactions)

    # Step 4: 构建交易图
    graph = build_transaction_graph(processed_data)

    # Step 5: **按节点存储三角形 motif
    deltas = [3600, 86400]  # 1小时(3600秒)和1天(86400秒)
    triangle_motifs = find_motif_counts(graph, deltas)

    # **打印所有三角形模式**
    print("所有三角形模式示例:")
    print(triangle_motifs)  # 输出所有找到的三角形模式

    # 存储所有三角形模式
    triangle_motifs_df = pd.DataFrame(triangle_motifs)

    # **保存为单个CSV文件**
    triangle_motifs_df.to_csv('triangle_motifs.csv', index=False)

    print("所有三角形模式已保存到 'triangle_motifs.csv'。")

    # 绘制原始图的1小时三角形模式热图
    fig, ax = plt.subplots()  # 创建一个新的图形和坐标轴
    ax = plottingutils.global_motif_heatplot(triangle_motifs[0], cmap="YlGnBu")  # 绘制1小时热图
    ax.set_title("Original Graph - 1 Hour Temporal Motifs Heatmap")
    plt.savefig("original_graph_1h_motifs_heatmap.png")  # 保存图像
    plt.show()  # 展示图形

    #绘制原始图的1天三角形模式热图
    fig, ax = plt.subplots()  # 创建一个新的图形和坐标轴
    ax = plottingutils.global_motif_heatplot(triangle_motifs[1], cmap="YlGnBu")  # 绘制1天热图
    ax.set_title("Original Graph - 1 Day Temporal Motifs Heatmap")
    plt.savefig("original_graph_1d_motifs_heatmap.png")  # 保存图像
    plt.show()  # 展示图形

    # Step 6: 可视化交易量与总额
    daily_transactions['total_value'] = daily_transactions['transaction_count'] * 10  # 假设总额计算逻辑
    plot_transactions_and_values(daily_transactions)

    gc.collect()
    # ------------------------- 空模型步骤 ---------------------------

    # 从Graph中提取边的数据（转换为Pandas DataFrame）
    graph_df = pd.read_csv(processed_data)

    # 使用空模型（打乱时间戳）生成随机化后的图数据
    time_col = "timeStamp"  # 假设时间戳列的名称为 "timestamp"
    randomized_graph_df = generate_randomized_reference_model(graph_df, time_col)
    randomized_graph_df.to_csv('randomized_graph.csv', index=False)
    randomized_graph='randomized_graph.csv'

    # 将打乱后的 DataFrame 用于构建 Raphtory 图对象
    graph_randomized = build_transaction_graph(randomized_graph)

    # Step 5: **按节点存储三角形 motif**
    deltas = [3600, 86400]  # 1小时(3600秒)和1天(86400秒)
    triangle_motifs_randomized = find_motif_counts(graph_randomized, deltas)

    # **打印所有三角形模式（空模型数据）**
    print("空模型的三角形模式示例:")
    print(triangle_motifs_randomized)  # 输出所有找到的三角形模式

    # 存储所有三角形模式
    triangle_motifs_randomized_df = pd.DataFrame(triangle_motifs_randomized)

    # **保存为单个CSV文件**
    triangle_motifs_randomized_df.to_csv('triangle_motifs_randomized.csv', index=False)

    print("空模型的三角形模式已保存到 'triangle_motifs_randomized.csv'。")

    # Step 6: 可视化交易量与总额
    daily_transactions['total_value'] = daily_transactions['transaction_count'] * 10  # 假设总额计算逻辑
    plot_transactions_and_values(daily_transactions)

    # 绘制打乱后的图的1小时三角形模式热图
    fig, ax = plt.subplots()  # 创建一个新的图形和坐标轴
    ax = plottingutils.global_motif_heatplot(triangle_motifs_randomized[0], cmap="YlGnBu")  # 绘制1小时热图
    ax.set_title("Randomized Graph - 1 Hour Temporal Motifs Heatmap")
    plt.savefig("randomized_graph_1h_motifs_heatmap.png")  # 保存图像
    plt.show()  # 展示图形

    # 绘制打乱后的图的1天三角形模式热图
    fig, ax = plt.subplots()  # 创建一个新的图形和坐标轴
    ax = plottingutils.global_motif_heatplot(triangle_motifs_randomized[1], cmap="YlGnBu")  # 绘制1天热图
    ax.set_title("Randomized Graph - 1 Day Temporal Motifs Heatmap")
    plt.savefig("randomized_graph_1d_motifs_heatmap.png")  # 保存图像
    plt.show()  # 展示图形

    process_centrality_algorithm(graph, algorithm_type="degree")   # 计算度中心性
    process_centrality_algorithm(graph, algorithm_type="pagerank")  # 计算Pagerank中心性
    #process_centrality_algorithm(graph, algorithm_type="betweenness")  # 计算介数中心性

    pagerank_df=pd.read_csv('pagerank.csv')
    degree_centrality_df=pd.read_csv('degree_centrality.csv')
    # 分析并分类
    classified_nodes = classify_nodes_based_on_pagerank_and_degree(pagerank_df, degree_centrality_df)
    print(classified_nodes.head())
    classified_nodes.to_csv('classified_nodes.csv', index=False)

if __name__ == "__main__":
    main()
