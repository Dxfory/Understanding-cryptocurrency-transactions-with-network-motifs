import pandas as pd
import matplotlib.pyplot as plt

def plot_transactions_and_values(
    daily_transactions_file='daily_transactions.csv',
    processed_transactions_file='processed_transactions.csv',
    highlight_output='daily_transactions_plot_with_highlights.png',
    value_trend_output='daily_transactions_and_value_plot.png'
):
    """
    读取每日交易数量数据以及处理后的交易数据，计算滑动平均(7日均线)和高交易量阈值，
    并依次绘制：
        1）每日交易数量折线图（含 7 日均线和高交易量标记）
        2）每日交易数量与每日交易总额双轴趋势图

    参数：
    -------
    daily_transactions_file : str
        存放每日交易数量数据的 CSV 文件路径（默认 'daily_transactions.csv'）。
        文件中应至少包含 'date' 和 'transaction_count' 两列。
    processed_transactions_file : str
        存放处理后交易明细的 CSV 文件路径，用于计算每日总交易额（默认 'processed_transactions.csv'）。
        该文件应包含 ['timeStamp', 'value'] 等列。
    highlight_output : str
        第一张图表（含高亮）保存的文件名（默认 'daily_transactions_plot_with_highlights.png'）。
    value_trend_output : str
        第二张图表（交易量和总额双轴）保存的文件名（默认 'daily_transactions_and_value_plot.png'）。
    """

    # ========== 1. 第一次读取 daily_transactions.csv，仅保留 transaction_count 一列 ==========

    df_daily = pd.read_csv(daily_transactions_file)           # 读取 CSV
    df_daily['date'] = pd.to_datetime(df_daily['date'])       # 将 'date' 转为 datetime
    df_daily.set_index('date', inplace=True)                  # 将 'date' 列设为索引

    # 只保留 'transaction_count' 这一个列
    daily_transactions = df_daily[['transaction_count']]

    # 计算 7 日滑动平均线
    daily_transactions['7_day_avg'] = daily_transactions['transaction_count'].rolling(window=7).mean()

    # 定义高交易量阈值：mean + 2*std
    mean_count = daily_transactions['transaction_count'].mean()
    std_count = daily_transactions['transaction_count'].std()
    high_threshold = mean_count + 2 * std_count

    # 找到高峰日期
    high_transaction_days = daily_transactions[
        daily_transactions['transaction_count'] > high_threshold
    ]

    # ========== 2. 绘制第 1 张图：每日交易数量 + 7 日均线 + 高交易量高亮 ==========

    plt.figure(figsize=(14, 8))
    plt.plot(daily_transactions.index,
             daily_transactions['transaction_count'],
             label='Daily Transactions',
             color='blue',
             alpha=0.6)

    plt.plot(daily_transactions.index,
             daily_transactions['7_day_avg'],
             label='7-Day Moving Average',
             color='red',
             linestyle='--')

    # 高交易量日期标记
    plt.scatter(high_transaction_days.index,
                high_transaction_days['transaction_count'],
                color='orange',
                label='High Transaction Days',
                zorder=5)

    # 给高峰点添加数值标注
    for date, count in high_transaction_days['transaction_count'].items():
        plt.text(date,
                 count,
                 f'{int(count)}',
                 color='black',
                 fontsize=9,
                 rotation=45,
                 ha='right')

    # 图表设置
    plt.title('Number of Transactions per Day with Highlights', fontsize=18)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Transaction Count', fontsize=14)
    plt.axhline(y=high_threshold, color='green', linestyle='--', label='High Transaction Threshold')
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(highlight_output)
    plt.show()

    # ========== 3. 第二次读取 daily_transactions.csv，用来绘制双轴图 (交易量 + 总额) ==========

    # 与原脚本一样，再次读取
    df_daily_2 = pd.read_csv(daily_transactions_file)
    df_daily_2['date'] = pd.to_datetime(df_daily_2['date'])
    df_daily_2.set_index('date', inplace=True)

    # 同样只保留 'transaction_count' 这一列即可
    daily_transactions_2 = df_daily_2[['transaction_count']]

    # 读取处理后交易数据 processed_transactions.csv，用于计算每日总交易额
    df_processed = pd.read_csv(processed_transactions_file)
    df_processed['timeStamp'] = pd.to_datetime(df_processed['timeStamp'])
    df_processed['date'] = df_processed['timeStamp'].dt.date
    df_processed['value'] = df_processed['value'].astype(float)

    # 按日汇总交易总额
    daily_values = df_processed.groupby('date')['value'].sum()
    # 将索引转为 datetime，以便与 daily_transactions_2 对齐
    daily_values.index = pd.to_datetime(daily_values.index)

    # 把总额合并到 daily_transactions_2
    daily_transactions_2['total_value'] = daily_values

    # ========== 4. 绘制第 2 张图：双轴 (每日交易数量 vs. 每日交易总额) ==========

    fig, ax1 = plt.subplots(figsize=(14, 8))

    # 左 y 轴：每日交易数量
    ax1.plot(daily_transactions_2.index,
             daily_transactions_2['transaction_count'],
             label='Daily Transactions',
             color='blue',
             alpha=0.6)
    ax1.set_xlabel('Date', fontsize=14)
    ax1.set_ylabel('Transaction Count', color='blue', fontsize=14)
    ax1.tick_params(axis='y', labelcolor='blue')

    # 右 y 轴：每日交易总额
    ax2 = ax1.twinx()
    ax2.plot(daily_transactions_2.index,
             daily_transactions_2['total_value'],
             label='Total Transaction Value (ETH)',
             color='orange',
             alpha=0.6)
    ax2.set_ylabel('Total Transaction Value (ETH)', color='orange', fontsize=14)
    ax2.tick_params(axis='y', labelcolor='orange')

    # 标题与图例
    fig.suptitle('Daily Transactions and Total Value Over Time', fontsize=18)
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', fontsize=12)

    plt.tight_layout()
    plt.savefig(value_trend_output)
    plt.show()