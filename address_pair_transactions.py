def analyze_address_pair_transactions(address_a, address_b, df):
    """
    分析两个地址的交易情况，包括各自的交易量和相互之间的交易次数
    :param address_a: 第一个地址
    :param address_b: 第二个地址
    :param df: 交易数据的 DataFrame（应包含 from_address 和 to_address 列）
    """

    # address_a 的交易情况
    sent_a = df[df['from_address'] == address_a].shape[0]
    received_a = df[df['to_address'] == address_a].shape[0]
    total_a = sent_a + received_a

    # address_b 的交易情况
    sent_b = df[df['from_address'] == address_b].shape[0]
    received_b = df[df['to_address'] == address_b].shape[0]
    total_b = sent_b + received_b

    # address_a → address_b
    a_to_b = df[(df['from_address'] == address_a) & (df['to_address'] == address_b)]

    # address_b → address_a
    b_to_a = df[(df['from_address'] == address_b) & (df['to_address'] == address_a)]

    # 打印结果
    print(f"\n{address_a} → {address_b} 交易次数: {len(a_to_b)}")
    print(f"{address_b} → {address_a} 交易次数: {len(b_to_a)}\n")

    print(f"{address_a}：")
    print(f"  发出交易数量: {sent_a}")
    print(f"  接收交易数量: {received_a}")
    print(f"  总交易数量: {total_a}\n")

    print(f"{address_b}：")
    print(f"  发出交易数量: {sent_b}")
    print(f"  接收交易数量: {received_b}")
    print(f"  总交易数量: {total_b}")


def get_address_contact_counts(target_address, exclude_address, df):
    """
    统计目标地址与所有其他地址（排除指定地址）之间的交易次数（含发出与接收）

    :param target_address: 要分析的地址
    :param exclude_address: 要排除的地址（如：彼此之间不统计）
    :param df: 交易数据 DataFrame，需含 from_address 和 to_address 列
    :return: Series（索引为地址，值为交易次数）
    """

    # 发送交易：target_address → 其他地址
    sent_df = df[df['from_address'] == target_address][['to_address']]
    sent_df = sent_df.rename(columns={'to_address': 'other_address'})
    sent_df['direction'] = 'sent'

    # 接收交易：其他地址 → target_address
    received_df = df[df['to_address'] == target_address][['from_address']]
    received_df = received_df.rename(columns={'from_address': 'other_address'})
    received_df['direction'] = 'received'

    # 合并并去除被排除的地址
    all_df = pd.concat([sent_df, received_df])
    all_df = all_df[all_df['other_address'] != exclude_address]

    # 统计交易次数
    contact_counts = all_df['other_address'].value_counts()

    return contact_counts
