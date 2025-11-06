import pandas as pd
import raphtory

def generate_randomized_reference_model(graph_df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """
    使用空模型生成图的随机化参考模型，保留来源和目的地，打乱时间戳。

    Args:
        graph_df (DataFrame): 图的 DataFrame，包含时间戳的交易数据。
        time_col (str): 时间戳列的名称，用于打乱。

    Returns:
        DataFrame: 时间戳被打乱的图数据。
    """
    return permuted_timestamps_model(graph_df, time_col)


def permuted_timestamps_model(graph_df: pd.DataFrame, time_name: str) -> pd.DataFrame:
    """
    返回一个打乱时间戳列的 DataFrame。

    Args:
        graph_df (DataFrame): 输入的图数据。
        time_name (str): 要打乱的时间戳列名。

    Returns:
        DataFrame: 打乱时间戳后的图数据。
    """
    shuffled_df = shuffle_column(graph_df, time_name)
    return shuffled_df


def shuffle_column(graph_df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    打乱指定列的数据并返回一个新的 DataFrame。

    Args:
        graph_df (DataFrame): 输入的图数据。
        col_name (str): 要打乱的列名。

    Returns:
        DataFrame: 打乱后的 DataFrame。
    """
    shuffled_df = graph_df.copy()
    shuffled_df[col_name] = graph_df[col_name].sample(frac=1).reset_index(drop=True)
    return shuffled_df
