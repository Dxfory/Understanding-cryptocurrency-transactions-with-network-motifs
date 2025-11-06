import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import os

# 设置API密钥和智能合约地址列表（包括常见和使用频繁的稳定币）
api_key = '22A8JRCHS4G9NDXX711I6NR1B6MIES91V7'
contract_addresses = [
    #'0xdac17f958d2ee523a2206206994597c13d831ec7',
    #'0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    #'0xa47c8bf37f92abed4a126bda807a7b7498661acd',
    #'0x6b175474e89094c44da98b954eedeac495271d0f',
    #'0x8e870d67f660d95d5be530380d0ec0bd388289e1',
    '0xd2877702675e6ceb975b4a1dff9fb7baf4c91ea9',
]

# 设置读取数据的起始和结束区块号
start_block = 6914000  # 从2019年1月的区块开始（假设已知的起始区块号）
end_block = 9200000  # 假设这是2019年1月结束的区块号

# 将区块范围切割为每次查询90,000个区块（减少分页请求次数）
block_size = 90000
block_ranges = [(i, min(i + block_size - 1, end_block)) for i in range(start_block, end_block + 1, block_size)]

# 设置重试策略
retry_strategy = Retry(
    total=5,  # 总共重试5次
    backoff_factor=1,  # 重试间隔倍数
    status_forcelist=[500, 502, 503, 504],  # 对于这些状态码进行重试
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # 重试的请求方法
)

# 创建一个会话对象
session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)


# 分页获取数据，减少每页返回的数据量（offset=1000）
def fetch_transactions(start_block, end_block, contract_address, page=1, offset=500):
    url = (f'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={contract_address}'
           f'&startblock={start_block}&endblock={end_block}&page={page}&offset={offset}&sort=asc&apikey={api_key}')

    try:
        response = session.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == '1' and data['result']:
                return data['result'], None  # 返回数据和分页信息
            elif data['status'] == '0' or not data['result']:
                if "No transactions found" in data['message']:
                    return [], None  # 返回空列表，跳过这次请求
                print(f"错误：{data['message']} for contract {contract_address}")
                return [], None
            else:
                print(f"错误：{data['message']} for contract {contract_address}")
                return [], None
        else:
            print(f"请求失败，状态码：{response.status_code} for contract {contract_address}")
            return [], None
    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")
        return [], None



# 用来追踪每个合约的分页进度
progress_tracker = {}

# 获取多个合约的交易数据
for contract_address in contract_addresses:
    # 每个合约开始前清空交易列表
    all_transactions = []

    # 如果有进度信息，继续从上次的位置开始
    last_page = progress_tracker.get(contract_address, {}).get("page", 1)
    last_block = progress_tracker.get(contract_address, {}).get("block", start_block)

    # 确保每个合约的区块范围从头开始，而不是从上次的区块开始
    for start_block, end_block in block_ranges:
        # 如果区块范围已经处理过，跳过
        if start_block < last_block:
            continue

        page = last_page
        print(f"正在获取合约 {contract_address} 从区块 {start_block} 到 {end_block} 的交易数据...")

        while True:
            print(f"正在获取第 {page} 页的数据...")
            transactions, next_page = fetch_transactions(start_block, end_block, contract_address, page=page)

            if not transactions:  # 如果没有获取到数据，跳出
                break

            all_transactions.extend(transactions)  # 将返回的交易数据加入到总列表中
            page = next_page if next_page else page + 1  # 更新页面或继续下一页
            time.sleep(5)  # 防止API速率限制

            # 在每次请求后检查当前获取的数据量
            if len(all_transactions) >= 10000:
                # 达到一定数量后，立即保存到文件
                df = pd.DataFrame(all_transactions)
                df.to_csv('stablecoin_transactions_all1.csv', mode='a',
                          header=not os.path.exists('stablecoin_transactions_all1.csv'),
                          index=False)
                print(
                    f"当前合约 {contract_address} 的 {len(all_transactions)} 条交易数据已保存为 stablecoin_transactions_all1.csv")
                all_transactions = []  # 清空数据，准备处理下一批数据

        # 将当前合约的剩余数据写入文件
        if all_transactions:
            df = pd.DataFrame(all_transactions)
            df.to_csv('stablecoin_transactions_all1.csv', mode='a',
                      header=not os.path.exists('stablecoin_transactions_all1.csv'),
                      index=False)
            print(
                f"合约 {contract_address} 的剩余 {len(all_transactions)} 条交易数据已保存为 stablecoin_transactions_all1.csv")

        # 更新进度信息
        progress_tracker[contract_address] = {
            "page": page,
            "block": end_block + 1  # 更新为下一个区块的开始
        }

    # 每次处理完一个合约时清空 all_transactions，准备处理下一个合约
    all_transactions = []

# 关闭session
session.close()
