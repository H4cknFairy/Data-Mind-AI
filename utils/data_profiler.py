import pandas as pd


def get_dataset_overview(df):
    """
    Generate basic information about the dataset.
    """

    overview = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_columns": len(df.select_dtypes(include="number").columns),
        "categorical_columns": len(
            df.select_dtypes(include=["object", "category"]).columns
        ),
    }

    return overview


def get_column_info(df):
    """
    Return information about each column.
    """

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values,
    })

    return column_info


def get_statistics(df):
    """
    Generate statistical summary for numeric columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    return numeric_df.describe().T