import pandas as pd


# 假设你已经有了 PageRank 和度中心性计算结果（pagerank_df 和 degree_centrality_df）

# 分析结果（这里假设你已经有了节点参与的 motif 类型计数，以下只是示例）
# 示例：根据 PageRank 和 Degree Centrality 分析节点角色

def classify_nodes_based_on_pagerank_and_degree(pagerank_df, degree_centrality_df):
    # 合并 PageRank 和 Degree Centrality 数据框
    df = pd.merge(pagerank_df, degree_centrality_df, on="Node", how="inner")

    # 定义分类函数
    def classify_node(row):
        if row["Pagerank"] > 0.05 and row["Degree Centrality"] > 0.5:
            return "Seller"  # 假设 PageRank 高且度中心性高的节点是卖家
        elif row["Pagerank"] > 0.05:
            return "Buyer"  # PageRank 高的节点可能是买家
        else:
            return "Shop"  # 其他节点为商家

    # 应用分类
    df["Role"] = df.apply(classify_node, axis=1)

    return df