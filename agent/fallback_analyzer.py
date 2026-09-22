import re
import pandas as pd


# ============================================================
# HELPERS
# ============================================================

def normalize(text):
    """Normalize text for easier matching."""
    return re.sub(r"[^a-z0-9\s]", " ", str(text).lower()).strip()


def find_column(df, words):
    """
    Find a dataset column related to given words.
    """

    normalized_columns = {
        col: normalize(col)
        for col in df.columns
    }

    # Exact match
    for col, normalized in normalized_columns.items():
        if normalized in words:
            return col

    # Partial match
    for col, normalized in normalized_columns.items():
        for word in words:
            if word in normalized or normalized in word:
                return col

    return None


def numeric_columns(df):
    return df.select_dtypes(include="number").columns.tolist()


def categorical_columns(df):
    return df.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()


# ============================================================
# LOCAL ANALYSIS
# ============================================================

def local_analysis(df: pd.DataFrame, question: str):

    if df is None or df.empty:
        return "The uploaded dataset is empty."

    q = normalize(question)

    numeric = numeric_columns(df)
    categorical = categorical_columns(df)

    # --------------------------------------------------------
    # 1. TOTAL / SUM
    # --------------------------------------------------------

    if any(word in q for word in [
        "total",
        "sum",
        "overall"
    ]):

        column = find_column(
            df,
            [
                word
                for word in df.columns
                if normalize(word) in q
            ]
        )

        if column is None:

            for col in numeric:
                if normalize(col) in q:
                    column = col
                    break

        if column is None and numeric:
            column = numeric[-1]

        if column is not None:

            value = df[column].sum()

            return (
                f"### 📊 Local Data Analysis\n\n"
                f"**Total {column}:** "
                f"{value:,.2f}\n\n"
                f"This value was calculated directly "
                f"from the uploaded dataset."
            )

    # --------------------------------------------------------
    # 2. AVERAGE / MEAN
    # --------------------------------------------------------

    if any(word in q for word in [
        "average",
        "mean",
        "avg"
    ]):

        target = None

        for col in numeric:
            if normalize(col) in q:
                target = col
                break

        if target is None:

            # Try common words
            for col in numeric:

                normalized = normalize(col)

                if any(
                    word in normalized
                    for word in [
                        "salary",
                        "revenue",
                        "price",
                        "quantity",
                        "amount",
                        "score",
                        "age",
                        "profit",
                        "income"
                    ]
                ):
                    target = col
                    break

        if target is None and numeric:
            target = numeric[0]

        # Check for grouping
        group = None

        for col in categorical:

            normalized = normalize(col)

            if normalized in q:
                group = col
                break

            if any(
                word in normalized
                for word in q.split()
            ):
                if normalized not in ["product"]:
                    group = col

        if group is not None:

            result = (
                df.groupby(group)[target]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
            )

            result[target] = result[target].round(2)

            return (
                f"### 📊 Average {target} by {group}\n\n"
                f"{result.to_markdown(index=False)}"
            )

        value = df[target].mean()

        return (
            f"### 📊 Average {target}\n\n"
            f"**{value:,.2f}**"
        )

    # --------------------------------------------------------
    # 3. MAXIMUM / HIGHEST
    # --------------------------------------------------------

    if any(word in q for word in [
        "highest",
        "maximum",
        "max",
        "largest",
        "most"
    ]):

        target = None

        for col in numeric:

            if normalize(col) in q:
                target = col
                break

        if target is None and numeric:
            target = numeric[-1]

        if target:

            idx = df[target].idxmax()
            row = df.loc[idx]

            output = pd.DataFrame([row])

            return (
                f"### 🏆 Highest {target}\n\n"
                f"**Value:** {row[target]:,.2f}\n\n"
                f"### Related Record\n\n"
                f"{output.to_markdown(index=False)}"
            )

    # --------------------------------------------------------
    # 4. MINIMUM / LOWEST
    # --------------------------------------------------------

    if any(word in q for word in [
        "lowest",
        "minimum",
        "min",
        "smallest",
        "least"
    ]):

        target = None

        for col in numeric:

            if normalize(col) in q:
                target = col
                break

        if target is None and numeric:
            target = numeric[-1]

        if target:

            idx = df[target].idxmin()
            row = df.loc[idx]

            output = pd.DataFrame([row])

            return (
                f"### 📉 Lowest {target}\n\n"
                f"**Value:** {row[target]:,.2f}\n\n"
                f"### Related Record\n\n"
                f"{output.to_markdown(index=False)}"
            )

    # --------------------------------------------------------
    # 5. TOP N
    # --------------------------------------------------------

    top_match = re.search(
        r"top\s+(\d+)",
        q
    )

    if top_match:

        n = int(top_match.group(1))

        target = None

        for col in numeric:

            if normalize(col) in q:
                target = col
                break

        if target is None and numeric:
            target = numeric[-1]

        if target:

            result = (
                df.nlargest(n, target)
            )

            return (
                f"### 🔝 Top {n} by {target}\n\n"
                f"{result.to_markdown(index=False)}"
            )

    # --------------------------------------------------------
    # 6. GROUP BY / BREAKDOWN
    # --------------------------------------------------------

    if any(word in q for word in [
        "by",
        "breakdown",
        "group",
        "per",
        "region",
        "category",
        "department",
        "product",
        "salesperson"
    ]):

        group = None

        # Detect categorical column
        for col in categorical:

            normalized = normalize(col)

            if normalized in q:
                group = col
                break

        if group:

            target = None

            for col in numeric:

                if normalize(col) in q:
                    target = col
                    break

            if target is None and numeric:
                target = numeric[-1]

            if target:

                result = (
                    df.groupby(group)[target]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                    .reset_index()
                )

                result[target] = result[target].round(2)

                return (
                    f"### 📊 {target} by {group}\n\n"
                    f"{result.to_markdown(index=False)}"
                )

    # --------------------------------------------------------
    # 7. COUNT ROWS
    # --------------------------------------------------------

    if any(word in q for word in [
        "how many rows",
        "number of rows",
        "how many records",
        "record count",
        "row count"
    ]):

        return (
            f"### 📊 Dataset Record Count\n\n"
            f"**{len(df):,} records**"
        )

    # --------------------------------------------------------
    # 8. UNIQUE VALUES
    # --------------------------------------------------------

    if any(word in q for word in [
        "unique",
        "distinct",
        "different"
    ]):

        for col in df.columns:

            if normalize(col) in q:

                count = df[col].nunique()

                return (
                    f"### 🔍 Unique {col}\n\n"
                    f"**{count:,} unique values**"
                )

    # --------------------------------------------------------
    # 9. MISSING VALUES
    # --------------------------------------------------------

    if any(word in q for word in [
        "missing",
        "null",
        "empty"
    ]):

        missing = (
            df.isna()
            .sum()
            .sort_values(
                ascending=False
            )
        )

        result = missing[
            missing > 0
        ]

        if result.empty:
            return (
                "### ✅ Missing Values\n\n"
                "There are no missing values "
                "in the dataset."
            )

        return (
            "### ⚠️ Missing Values\n\n"
            f"{result.to_frame('Missing Values').to_markdown()}"
        )

    # --------------------------------------------------------
    # 10. DATASET SIZE
    # --------------------------------------------------------

    if any(word in q for word in [
        "dataset size",
        "how large",
        "how big",
        "dimensions"
    ]):

        return (
            f"### 📊 Dataset Size\n\n"
            f"**Rows:** {len(df):,}\n\n"
            f"**Columns:** {len(df.columns):,}"
        )

    # --------------------------------------------------------
    # 11. DESCRIBE DATASET
    # --------------------------------------------------------

    if any(word in q for word in [
        "describe",
        "summary",
        "overview",
        "statistics"
    ]):

        if numeric:

            result = df[numeric].describe().T

            return (
                "### 📊 Statistical Summary\n\n"
                f"{result.round(2).to_markdown()}"
            )

    # --------------------------------------------------------
    # 12. CORRELATION
    # --------------------------------------------------------

    if any(word in q for word in [
        "correlation",
        "correlate",
        "relationship"
    ]):

        if len(numeric) >= 2:

            result = df[numeric].corr()

            return (
                "### 🔗 Correlation Analysis\n\n"
                f"{result.round(2).to_markdown()}"
            )

    # --------------------------------------------------------
    # NO MATCH
    # --------------------------------------------------------

    return None