import pandas as pd
import os

def preprocess_data(input_file, output_folder='processed_data_all1', output_file_prefix='processed_transactions'):
    """
    预处理交易数据并根据 tokenSymbol 将其分组到不同的 CSV 文件中。
    """
    print("开始预处理数据...")

    # 读取输入数据
    df = pd.read_csv(input_file)

    # 按 'timeStamp' 排序，从小到大
    df = df.sort_values(by='timeStamp', ascending=True)

    # 删除包含 'from' 或 'to' 为 NaN 的行
    df = df.dropna(subset=['from', 'to'])

    # 将 'value' 转换为浮动类型
    df['value'] = df['value'].astype(float)

    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 按 'tokenSymbol' 分组并保存每个组到不同的 CSV 文件中
    token_symbols = df['tokenSymbol'].unique()  # 获取所有唯一的 tokenSymbol
    for token in token_symbols:
        token_df = df[df['tokenSymbol'] == token]
        output_file = os.path.join(output_folder, f'{output_file_prefix}_{token}.csv')
        token_df.to_csv(output_file, index=False)
        print(f"数据已保存为 '{output_file}'")

    print("预处理完成并保存所有 CSV 文件。")
    return output_folder

# 示例使用
input_file = 'stablecoin_transactions_all_clean1.csv'  # 输入文件路径
output_folder = 'processed_data_all1'  # 输出文件夹路径
preprocess_data(input_file, output_folder)
