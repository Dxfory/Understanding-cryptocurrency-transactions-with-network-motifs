# import os
# import pandas as pd
#
#
# def merge_csv_files(folder_path, output_file):
#     # 获取文件夹中所有的CSV文件
#     csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
#
#     # 初始化一个空的DataFrame来存储合并的数据
#     combined_df = pd.DataFrame()
#
#     for csv_file in csv_files:
#         file_path = os.path.join(folder_path, csv_file)
#
#         # 读取每个CSV文件
#         df = pd.read_csv(file_path)
#
#         # 去除重复的行
#         df = df.drop_duplicates()
#
#         # 合并到总的DataFrame
#         combined_df = pd.concat([combined_df, df], ignore_index=True)
#     # 排序：按照 "DateTime (UTC)" 列进行升序排序
#     combined_df['DateTime (UTC)'] = pd.to_datetime(combined_df['DateTime (UTC)'], errors='coerce')  # 转换为日期时间格式
#     combined_df = combined_df.sort_values(by='DateTime (UTC)', ascending=True)  # 排序
#
#     # 保存合并后的DataFrame到一个新的CSV文件
#     combined_df.to_csv(output_file, index=False)
#     print(f"所有CSV文件已合并并保存为 {output_file}")
#
#
# # 示例用法
# folder_path = 'C:/Users/acer/OneDrive/桌面/USDT_2019'  # 文件夹路径
# output_file = 'USDT_2019'  # 输出的CSV文件路径
# merge_csv_files(folder_path, output_file)

# import pandas as pd
#
#
# def remove_duplicate_rows_and_sort(input_file, output_file):
#     # 读取CSV文件时禁用low_memory
#     df = pd.read_csv(input_file, low_memory=False)
#
#     # 将 timeStamp 转换为标准日期格式 (Unix timestamp 转换为 datetime)
#     df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')
#
#     # 按 timeStamp 排序，由远及近
#     df = df.sort_values(by='timeStamp', ascending=False)
#
#     # 删除重复的行，保留唯一的行
#     df = df.drop_duplicates()
#
#     # 将结果保存为新的CSV文件
#     df.to_csv(output_file, index=False)
#
#
# # 示例使用
# input_file = 'stablecoin_transactions_all1.csv'  # 输入文件路径
# output_file = 'stablecoin_transactions_all_clean1.csv'  # 输出文件路径
# remove_duplicate_rows_and_sort(input_file, output_file)
import pandas as pd

def rename_columns(input_file, output_file):
    """
    This function reads the input CSV file, renames the columns, and saves the modified DataFrame as a new CSV file.
    """
    # 读取输入数据
    df = pd.read_csv(input_file)

    # 字典映射：原列名 -> 新列名
    column_mapping = {
        'blockNumber': 'block_number',
        'transactionIndex': 'transaction_index',
        'from': 'from_address',
        'to': 'to_address',
        #'timeStamp': 'time_stamp',
        'contractAddress': 'contract_address',
        'value': 'value'
    }

    # 重命名列
    df = df.rename(columns=column_mapping)

    # 保存处理后的数据到新的 CSV 文件
    df.to_csv(output_file, index=False)

    print(f"文件已保存为 '{output_file}'")
    return output_file

# Example usage
input_file = 'stablecoin_transactions_all_clean1_1.csv.csv'  # Replace with your input file path
output_file = 'processed_transactions.csv'  # Output file name
rename_columns(input_file, output_file)
