import pandas as pd
from raphtory import algorithms

# 定义计算不同中心性的函数
def compute_degree_centrality(graph):
    """
    计算度中心性（Degree Centrality）并返回结果
    """
    degree_centrality_result = algorithms.degree_centrality(graph)
    return degree_centrality_result

def compute_pagerank(graph, iter_count=20, max_diff=None, damping_factor=0.85):
    """
    计算 Pagerank 中心性并返回结果
    """
    pagerank_result = algorithms.pagerank(graph, iter_count=iter_count, max_diff=max_diff,
                                          damping_factor=damping_factor)
    return pagerank_result

def compute_betweenness_centrality(graph, k=None, normalized=True):
    """
    计算介数中心性（Betweenness Centrality）并返回结果
    """
    betweenness_result = algorithms.betweenness_centrality(graph, k=k, normalized=normalized,)
    return betweenness_result

# 集中式执行中心性算法的处理
def process_centrality_algorithm(graph, algorithm_type="degree"):
    """
    选择中心性算法并执行相应操作：计算、排序、生成DataFrame、保存为CSV。
    """
    # Step 1: 根据算法类型调用相应的计算函数
    if algorithm_type == "degree":
        print("度中心性计算中")
        result = compute_degree_centrality(graph)
        result_name = "Degree Centrality"
        csv_name = "degree_centrality.csv"
    elif algorithm_type == "pagerank":
        print("Pagerank 计算结果中")
        result = compute_pagerank(graph, iter_count=20)
        result_name = "Pagerank"
        csv_name = "pagerank.csv"
    elif algorithm_type == "betweenness":
        print("介数中心性计算结果中")
        result = compute_betweenness_centrality(graph, k=None, normalized=True)
        result_name = "Betweenness Centrality"
        csv_name = "betweenness.csv"
    else:
        print(f"未知算法类型: {algorithm_type}")
        return

    # Step 2: 按值降序排序
    sorted_result = result.sort_by_value(reverse=True)

    # Step 3: 将排序后的结果转换为 pandas DataFrame
    sorted_data = [(key, value) for key, value in sorted_result]
    df = pd.DataFrame(sorted_data, columns=["Node", result_name])

    # Step 4: 显示前五个节点
    top_5 = df.head(5)
    print(f"{result_name} 计算结果：")
    print(top_5)

    # Step 5: 保存到CSV文件
    df.to_csv(csv_name, index=False)
    print(f"{result_name} 计算完成，结果已保存到 {csv_name}")