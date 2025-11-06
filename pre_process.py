import pandas as pd
import os

# 预处理数据函数
def preprocess_data(input_file, output_file):
    """
    预处理交易数据并保存为 CSV 文件，如果文件不存在则创建它。如果文件已存在，则覆盖。
    参数:
    - input_file: 原始输入数据文件路径
    - output_file: 输出处理后的数据文件路径
    """
    print("开始预处理数据...")

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件 '{input_file}' 不存在，请检查文件路径。")

    # 读取输入数据
    df = pd.read_csv(input_file)

    # 处理数据，丢弃缺失的地址信息，并确保数据类型正确
    df = df.dropna(subset=['from_address', 'to_address'])  # 删除无效行
    df['value'] = df['value'].astype(float)  # 确保 'value' 列为浮动类型
    df['timeStamp'] = pd.to_datetime(df['time_stamp'], unit='s')  # 处理时间戳

    # 去除重复行，默认按所有列去重
    df = df.drop_duplicates()  # 去重操作，删除重复的整行数据

    # 如果只想去除特定列的重复，可以按以下方式操作：
    # df = df.drop_duplicates(subset=['from_address', 'to_address', 'value'])

    # 检查输出目录是否存在，如果不存在则创建它
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir) and output_dir != '':
        os.makedirs(output_dir)
        print(f"输出目录 '{output_dir}' 不存在，正在创建...")

    # 如果文件已存在，则覆盖
    df.to_csv(output_file, index=False, mode='w')  # 'w' 模式会覆盖文件

    print(f"预处理完成并保存为 '{output_file}'")
    return df  # 返回处理后的 DataFrame


# 使用示例：
input_file = 'token_transfers_V3.0.0.csv'
output_file = 'processed_transactions.csv'

# Step 1: 数据预处理
processed_data = preprocess_data(input_file, output_file)
