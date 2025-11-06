from raphtory import Graph
import pandas as pd

# 初始化图表
g = Graph()

# 加载交易数据
df = pd.read_csv('processed_transactions.csv')

# 确保时间戳为 Unix 时间戳（整数）
df['timeStamp'] = pd.to_datetime(df['timeStamp']).view('int64') // 10**9

# 遍历数据集，逐条添加到图表
for _, row in df.iterrows():
    timestamp = row['timeStamp']
    src = str(row['from']).strip()  # 确保是字符串
    dst = str(row['to']).strip()    # 确保是字符串
    value = row['value']

    # 调试输出
    print(f"Processing transaction: timestamp={timestamp}, src={src}, dst={dst}, value={value}")

    if src and dst:
        # 使用正确的 add_edge 签名
        g.add_edge(timestamp, src, dst, properties={"value": value})
    else:
        print("Skipping invalid transaction due to missing src or dst")

# 打印图表的最终信息
print("加载完成后图表信息：")
print(g)

# 保存图表
g.save("raphtory_graph.json")
print("图表已保存为 'raphtory_graph.json'")

# 加载保存的图表
g_loaded = Graph.load("raphtory_graph.json")

# 打印加载后的图表信息
print("加载后的图表信息：")
print(g_loaded)