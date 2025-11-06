import pandas as pd
import matplotlib.pyplot as plt
from raphtory import Graph
import numpy as np
from sklearn.cluster import DBSCAN
import gc
from collections import defaultdict
from tqdm import tqdm
import time
import plotly.graph_objs as go
import plotly.io as pio

# ========== 日志函数 ==========
def log(message):
    """简单的日志函数，打印当前时间和消息"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{current_time}] {message}")

# ========== 数据加载与预处理 ==========
def load_and_preprocess_data(input_file='processed_transactions.csv'):
    log("开始加载和预处理数据...")

    # 读取原始交易数据
    df = pd.read_csv(input_file)
    df['timeStamp'] = pd.to_datetime(df['timeStamp'])
    df['date'] = df['timeStamp'].dt.date


    log("数据加载完成。")
    return df

def daily_transaction_analysis(input_file):
    """
    分析每日交易量。
    """
    print("开始每日交易量分析...")
    df = pd.read_csv(input_file)
    df['timeStamp'] = pd.to_datetime(df['timeStamp'])
    df['date'] = df['timeStamp'].dt.date
    df['value'] = df['value'].astype(float)
    daily_transactions = df.groupby('date').size().reset_index(name='transaction_count')
    print("每日交易量分析完成。")
    return daily_transactions

# ========== 交易关系图构建 ==========
from raphtory import Graph

def build_transaction_graph(df):
    log("Starting to build the transaction graph...")

    # Convert timestamp column to datetime format if not already done
    df["timeStamp"] = pd.to_datetime(df["timeStamp"])

    # Initialize Raphtory graph
    graph = Graph()

    # Load edges efficiently
    graph.load_edges_from_pandas(
        df=df,
        src="from_address",
        dst="to_address",
        time="timeStamp",
        properties=["value"],  # Store transaction value
    )

    log("Transaction graph construction completed.")
    return graph
# graph_build.py
def build_transaction_graph_with_nodes(df):
    from raphtory import Graph

    df["timeStamp"] = pd.to_datetime(df["timeStamp"])

    # Step 1: Build graph
    graph = Graph()

    # Step 2: Load edges
    graph.load_edges_from_pandas(
        df=df,
        src="from_address",
        dst="to_address",
        time="timeStamp",
        properties=["value"]
    )

    # Step 3: Build and load nodes
    unique_nodes = pd.unique(df[["from_address", "to_address"]].values.ravel())
    nodes_df = pd.DataFrame({"address": unique_nodes})

    address_first_seen = df.groupby("from_address")["timeStamp"].min()
    to_first_seen = df.groupby("to_address")["timeStamp"].min()
    first_seen = pd.concat([address_first_seen, to_first_seen]).groupby(level=0).min()
    nodes_df["timeStamp"] = nodes_df["address"].map(first_seen)

    # 可选添加属性
    nodes_df["node_type"] = "unknown"

    graph.load_nodes_from_pandas(
        df=nodes_df,
        id="address",
        time="timeStamp",
        constant_properties=["node_type"],
        shared_constant_properties={"source": "processed_transactions.csv"}
    )

    return graph

# ========== 计算交易量分布 ==========
def calculate_transaction_volume(df):
    log("开始计算交易量分布...")

    # 计算每个地址的交易总额（包括发送和接收）
    from_address_volume = df.groupby('from_address')['value'].sum()
    to_address_volume = df.groupby('to_address')['value'].sum()

    # 合并发送和接收的交易量
    address_volume = pd.concat([from_address_volume, to_address_volume], axis=0).groupby(level=0).sum()

    log("交易量分布计算完成。")
    return address_volume

# ========== 创建概率分布函数 (PDF) ==========
def create_pdf(address_volume):
    log("开始创建概率分布函数 (PDF)...")

    # 计算交易量的累计分布
    sorted_volumes = address_volume.sort_values(ascending=False)
    total_transactions = sorted_volumes.sum()

    # 计算每个地址的交易量占比
    pdf = sorted_volumes / total_transactions

    log("概率分布函数 (PDF) 创建完成。")
    return pdf

# ========== 找出前0.1%的一批地址 ==========
def find_top_0_1_percent_addresses(pdf):
    log("开始识别前0.1%的一批地址（累积交易量达到99.9%）...")

    # 计算累积概率分布
    cumulative_pdf = pdf.cumsum()

    # 找到累积概率达到或超过99.9%的地址
    threshold_index = cumulative_pdf[cumulative_pdf >= 0.999].index[0]

    # 获取前一批地址，直到累积概率达到99.9%
    top_0_1_percent_addresses = pdf.loc[:threshold_index]

    log("前0.1%交易者的地址（按交易量排序）:")
    print(top_0_1_percent_addresses)
    top_0_1_percent_addresses_df = pd.DataFrame(top_0_1_percent_addresses).reset_index()
    top_0_1_percent_addresses_df.columns = ['Address', 'Transaction Volume']

    # 保存为 Excel 文件
    top_0_1_percent_addresses_df.to_excel('top_0_1_percent_addresses.xlsx', index=False)

    log("前0.1%交易者的地址已保存为 Excel 文件。")
    return top_0_1_percent_addresses_df

# ========== 可视化交易量分布 ==========
def plot_transaction_volume_distribution(pdf):
    log("开始可视化交易量分布...")

    # 创建排名序列
    rank = np.arange(1, len(pdf) + 1)
    
    # 可视化代码
    trace = go.Scatter(
        x=rank,
        y=pdf.cumsum(),
        mode='lines',
        name='Cumulative PDF',
        line=dict(color='blue')
    )
    
    layout = go.Layout(
        title='Cumulative Probability Distribution of Transaction Volume',
        xaxis=dict(title='Rank of Address'),
        yaxis=dict(title='Cumulative Probability'),
        showlegend=True
    )

    fig = go.Figure(data=[trace], layout=layout)
    pio.write_image(fig, 'transaction_volume_cdf_plotly.png')
    fig.show()

    log("交易量分布可视化完成。")

# ========== 高频交易关系分析 ==========
def analyze_high_frequency_transactions(graph, start_date, end_date):
    log("开始高频交易关系分析...")

    # 设置时间窗口以查询特定时间段内的交易关系
    windowed_graph = graph.window(start_date, end_date)

    log("开始统计每对地址之间的交易次数...")

    # 统计每对地址之间的交易次数
    relationship_counts = defaultdict(int)
    for edge in tqdm(windowed_graph.edges, desc="统计交易关系"):
        relationship_counts[(edge.src, edge.dst)] += 1

    log("每对地址之间的交易次数统计完成。")

    # 转换为列表
    edges_data = [(src, dst, count) for (src, dst), count in relationship_counts.items()]

    log("开始计算每对关系的交易量占比...")

    # 计算每对关系的交易量占比
    total_relationships = sum([count for _, _, count in edges_data])
    relationship_pdf = pd.Series({(src, dst): count / total_relationships for src, dst, count in edges_data})

    log("交易量占比计算完成。")

    # 排序并获取前0.1%的一批交易关系
    top_0_1_percent_count = max(1, int(len(edges_data) * 0.001))  # 确保至少选择一个
    most_active_relationships = relationship_pdf.sort_values(ascending=False).head(top_0_1_percent_count)

    log("\n高峰期最频繁的交易对（前 0.1%）:")
    for (src, dst), count in most_active_relationships.items():
        print(f"From: {src} -> To: {dst}, Count: {count}")

    log("高频交易关系分析完成。")

# ========== 时间序列交易量分析 ==========
def time_series_transaction_analysis(df):
    log("开始时间序列交易量分布分析...")

    # 按时间分组，计算每日交易量
    time_series = df.groupby('date').size()

    log("时间序列交易量分布计算完成。")

    # 可视化每日交易量变化
    plt.figure(figsize=(10, 6))
    time_series.plot(kind='bar', color='orange', alpha=0.7)
    plt.title('Transaction Volume Over Time (Daily)', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Transaction Volume', fontsize=12)

    # 设置 X 轴坐标减少一些时间坐标
    step = max(1, len(time_series) // 10)  # 每 10 个日期取一个
    xticks = range(0, len(time_series), step)  # 设置 X 轴刻度
    plt.xticks(xticks, time_series.index[xticks], rotation=45)  # 设置显示的日期并旋转 45 度

    plt.tight_layout()  # 调整布局
    plt.savefig('transaction_volume_over_time.png')
    plt.show()

    log("时间序列交易量分布可视化完成。")


# ========== 内存优化 ==========
def optimize_memory():
    log("开始内存优化...")

    # 释放不必要的内存
    gc.collect()

    log("内存优化完成。")



def highlight_high_transactions(daily_transactions, output_file='daily_transactions_plot.png'):
    """
    绘制每日交易量趋势并高亮高峰交易量日期。
    """
    print("开始高峰交易量检测...")
    daily_transactions['7_day_avg'] = daily_transactions['transaction_count'].rolling(window=7).mean()
    mean_count = daily_transactions['transaction_count'].mean()
    std_count = daily_transactions['transaction_count'].std()
    high_threshold = mean_count + 2 * std_count

    high_transaction_days = daily_transactions[daily_transactions['transaction_count'] > high_threshold]

    plt.figure(figsize=(14, 8))
    plt.plot(daily_transactions['date'], daily_transactions['transaction_count'], label='Daily Transactions', color='blue')
    plt.plot(daily_transactions['date'], daily_transactions['7_day_avg'], label='7-Day Moving Average', color='red', linestyle='--')
    plt.scatter(high_transaction_days['date'], high_transaction_days['transaction_count'], color='orange', label='High Transaction Days')
    plt.axhline(y=high_threshold, color='green', linestyle='--', label='High Transaction Threshold')
    plt.title('Daily Transactions with Highlights', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Transaction Count')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()
    print(f"高峰交易量检测完成，图表已保存为 '{output_file}'")
