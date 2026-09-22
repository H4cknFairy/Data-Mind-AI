import pandas as pd


def load_dataset(uploaded_file):
    """
    Load a CSV or Excel file into a Pandas DataFrame.
    """

    if uploaded_file is None:
        return None

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)

        else:
            raise ValueError(
                "Unsupported file format. Please upload a CSV or Excel file."
            )

        return df

    except Exception as e:
        raise ValueError(f"Could not load the dataset: {str(e)}")