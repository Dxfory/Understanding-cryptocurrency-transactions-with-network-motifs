import pandas as pd

# 读取 CSV 文件
file_path = 'token_transfers.csv'
df = pd.read_csv(file_path)

# 提取 'contract_address' 列，并找出唯一的值
unique_contract_addresses = df['contract_address'].unique()

# 输出所有唯一的 contract_address
print("所有唯一的 contract_address:")
for address in unique_contract_addresses:
    print(address)
