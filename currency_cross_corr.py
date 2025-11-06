
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: 数据读取
df = pd.read_csv('token_transfers.csv')

# Step 2: 数据预处理
df['date'] = pd.to_datetime(df['time_stamp'], unit='s').dt.date

stablecoin_contracts = {
    '0xdac17f958d2ee523a2206206994597c13d831ec7': 'USDT',
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': 'USDC',
    '0x6b175474e89094c44da98b954eedeac495271d0f': 'DAI',
    '0xd2877702675e6ceb975b4a1dff9fb7baf4c91ea9': 'UST',
    '0xa47c8bf37f92abed4a126bda807a7b7498661acd': 'UST_Wormhole',
    '0x8e870d67f660d95d5be530380d0ec0bd388289e1': 'USDP'
}

df['stablecoin'] = df['contract_address'].map(stablecoin_contracts)
df = df.dropna(subset=['stablecoin'])

# 每日交易金额统计
daily_value = df.groupby(['date', 'stablecoin'])['value'].sum().unstack(fill_value=0)

# Step 3: 定义crash事件日期
crash_date = pd.Timestamp('2022-05-11').date()

pre_crash_data = daily_value.loc[daily_value.index < crash_date]
post_crash_data = daily_value.loc[daily_value.index >= crash_date]

# Step 4: 定义计算最大互相关系数的函数
def max_cross_corr(series1, series2):
    lags = range(-7, 8)  # 滞后窗口为-7到7天
    corr_values = [series1.corr(series2.shift(lag)) for lag in lags]
    return np.nanmax(corr_values)

# Step 5: 计算最大互相关系数矩阵
def compute_max_cross_corr_matrix(data):
    coins = data.columns
    cross_corr_matrix = pd.DataFrame(np.zeros((len(coins), len(coins))), columns=coins, index=coins)
    for coin1 in coins:
        for coin2 in coins:
            cross_corr_matrix.loc[coin1, coin2] = max_cross_corr(data[coin1], data[coin2])
    return cross_corr_matrix

pre_crash_cross_corr = compute_max_cross_corr_matrix(pre_crash_data)
post_crash_cross_corr = compute_max_cross_corr_matrix(post_crash_data)

# Step 6: 绘制热图
fig, axs = plt.subplots(1, 2, figsize=(18, 7))

sns.heatmap(pre_crash_cross_corr, annot=True, cmap="coolwarm", vmin=0, vmax=1, linewidths=.5, ax=axs[0], square=True)
axs[0].set_title("Pre-crash Max Cross-correlation", fontsize=14)
axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45, ha='right')

sns.heatmap(post_crash_cross_corr, annot=True, cmap="coolwarm", vmin=0, vmax=1, linewidths=.5, ax=axs[1], square=True)
axs[1].set_title("Post-crash Max Cross-correlation", fontsize=14)
axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.show()