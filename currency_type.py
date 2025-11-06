import pandas as pd

def get_dataframes_by_token(df, address_col="contract_address"):
    """
    根据合约地址将 df 划分为 6 个币种的 DataFrame，并在内存中返回。

    参数
    ----
    df : pd.DataFrame
        待处理的数据，其中必须至少包含一列合约地址 (默认为 'contract_address')。
    address_col : str
        合约地址所在列名，默认 'contract_address'。

    返回
    ----
    dict[str, pd.DataFrame]
        字典形式，键为币种名称('USDT','USDC'等)，值为对应筛选后的 DataFrame。
        若某币种在 df 中不存在，则返回的 DataFrame 为空 (shape = (0, ncols))。
    """

    # 定义 6 个合约地址到币种的映射表
    address_to_token = {
        "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC",
        "0x6b175474e89094c44da98b954eedeac495271d0f": "DAI",
        "0xd2877702675e6ceb975b4a1dff9fb7baf4c91ea9": "LUNA",
        "0xa47c8bf37f92abed4a126bda807a7b7498661acd": "UST",
        "0x8e870d67f660d95d5be530380d0ec0bd388289e1": "PAX"
    }

    # 先将合约地址映射到相应的币种；不在映射表中的地址视为 "UNKNOWN"
    df["token_name"] = df[address_col].map(address_to_token).fillna("UNKNOWN")

    # 准备一个结果字典，用于存储 6 种币的 DataFrame
    result = {}
    tokens = ["USDT", "USDC", "DAI", "LUNA", "UST", "PAX"]  # 6 种币

    for token in tokens:
        # 使用布尔索引挑选此币种的数据，并拷贝到新的 DataFrame（避免 SettingWithCopyWarning）
        token_df = df[df["token_name"] == token].copy()
        result[token] = token_df

    return result
