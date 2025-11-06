import pandas as pd

# 读取预处理后的交易数据
df = pd.read_csv('processed_transactions.csv')

# 确保时间戳列是日期格式
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

# 提取日期（不包含时间部分）
df['date'] = df['timeStamp'].dt.date

# 按日期分组并计算每一天的交易数量
daily_transactions = df.groupby('date').size()

# 打印每日交易数量
print(daily_transactions.head())

# 将每日交易数量保存到CSV文件（可选）
daily_transactions.to_csv('daily_transactions.csv', header=True)
