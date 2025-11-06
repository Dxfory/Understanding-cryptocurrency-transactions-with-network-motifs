from raphtory import Graph
import pandas as pd
import os
import shutil

# 初始化图表
g = Graph()

# 加载交易数据（作为边的输入数据框）
edges_df = pd.read_csv('processed_transactions.csv')

# 确保时间戳为日期格式
edges_df['timeStamp'] = pd.to_datetime(edges_df['timeStamp'])

# 重命名列以适配 Raphtory 要求
edges_df = edges_df.rename(columns={
    'timeStamp': 'timestamp',         # 更正字段名称
    'from_address': 'source',         # 更正字段名称
    'to_address': 'destination',      # 更正字段名称
})

# 确保交易金额是浮点数
edges_df['value'] = edges_df['value'].astype(float)

# 模拟节点数据框（如交易地址的属性等）
nodes_df = edges_df[['source', 'timestamp']].rename(columns={
    'source': 'node_id'               # 更正字段名称
}).drop_duplicates()

# 添加额外的模拟属性
nodes_df['node_name'] = nodes_df['node_id']
nodes_df['node_type'] = 'wallet'

# 打印数据框信息
pd.set_option('display.max_columns', None)
print("--- Edge Dataframe ---")
print(edges_df.head(2))
print("\n--- Node Dataframe ---")
print(nodes_df.head(2))

# 从 Pandas 数据框加载边
g.load_edges_from_pandas(
    df=edges_df,
    time="timestamp",         # 时间列
    src="source",             # 源节点
    dst="destination",        # 目标节点
    properties=["value"],     # 动态属性
    shared_constant_properties={"datasource": "processed_transactions.csv"}  # 共享常量属性
)

# 从 Pandas 数据框加载节点
g.load_nodes_from_pandas(
    df=nodes_df,
    time="timestamp",         # 时间列
    id="node_id",             # 节点 ID
    properties=["node_name"], # 动态属性
    constant_properties=["node_type"],  # 常量属性
    shared_constant_properties={"datasource": "processed_transactions.csv"}  # 共享常量属性
)

# 打印生成的图表和示例节点/边
print("生成的图表和示例节点/边：")
print(g)
print(g.node(nodes_df['node_id'].iloc[0]))  # 打印第一个节点的属性
print(g.edge(edges_df['source'].iloc[0], edges_df['destination'].iloc[0]))  # 打印第一条边的属性

# 新增功能：保存图表到文件
save_path = "/tmp/saved_graph"

# 确保保存路径为空
if os.path.exists(save_path):
    shutil.rmtree(save_path)  # 清空非空目录
os.makedirs(save_path, exist_ok=True)  # 创建空目录

g.save_to_file(save_path)
print(f"\n图表已保存为 '{save_path}'")

# 新增功能：从文件加载图表
loaded_graph = Graph.load_from_file(save_path)
print("\n重新加载的图表信息：")
print(loaded_graph)

print("Nodes 类型:", type(g.nodes))
print("Edges 类型:", type(g.edges))
print("Nodes 示例:", list(g.nodes)[:5])  # 打印前 5 个节点
print("Edges 示例:", list(g.edges)[:5])  # 打印前 5 条边

# 验证保存和加载后的图表一致性
print("\n验证保存和加载后的图表一致性：")
try:
    node_count_original = len(list(g.nodes))
    node_count_loaded = len(list(loaded_graph.nodes))
    print("节点数是否一致：", node_count_original == node_count_loaded)

    edge_count_original = len(list(g.edges))
    edge_count_loaded = len(list(loaded_graph.edges))
    print("边数是否一致：", edge_count_original == edge_count_loaded)

    time_range_original = (g.earliest_time, g.latest_time)
    time_range_loaded = (loaded_graph.earliest_time, loaded_graph.latest_time)
    print("时间范围是否一致：", time_range_original == time_range_loaded)

except Exception as e:
    print(f"一致性验证失败：{e}")

def build_transaction_graph(input_file, save_path='/tmp/saved_graph'):
    """
    基于交易数据构建 Raphtory 图并保存到文件。
    """
    print("开始构建交易图...")
    g = Graph()
    edges_df = pd.read_csv(input_file)
    edges_df['timeStamp'] = pd.to_datetime(edges_df['timeStamp'])
    edges_df = edges_df.rename(columns={
        'timeStamp': 'timestamp',
        'from_address': 'source',
        'to_address': 'destination',
    })
    edges_df['value'] = edges_df['value'].astype(float)

    g.load_edges_from_pandas(
        df=edges_df,
        time="timestamp",
        src="source",
        dst="destination",
        properties=["value"],
    )

    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)
    g.save_to_file(save_path)
    print(f"交易图已保存到 '{save_path}'")
    return g