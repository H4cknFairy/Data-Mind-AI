import pandas as pd
import plotly.express as px


# ============================================================
# DETECT COLUMN TYPES
# ============================================================

def get_column_types(df):

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    datetime_columns = []

    for column in df.columns:

        try:

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            if converted.notna().sum() > 0:
                datetime_columns.append(column)

        except Exception:
            pass

    return (
        numeric_columns,
        categorical_columns,
        datetime_columns,
    )


# ============================================================
# FIND BEST VISUALIZATION
# ============================================================

def create_visualization(
    df,
    question,
    result=None,
):

    if df is None or df.empty:
        return None


    question_lower = question.lower()


    numeric_columns, categorical_columns, datetime_columns = (
        get_column_types(df)
    )


    # ========================================================
    # DATE / TIME TREND
    # ========================================================

    if datetime_columns and numeric_columns:

        date_column = datetime_columns[0]

        numeric_column = numeric_columns[0]

        trend_df = df.copy()

        trend_df[date_column] = pd.to_datetime(
            trend_df[date_column],
            errors="coerce"
        )

        trend_df = (
            trend_df
            .dropna(
                subset=[
                    date_column,
                    numeric_column
                ]
            )
            .sort_values(date_column)
        )


        if (
            "trend" in question_lower
            or "over time" in question_lower
            or "time" in question_lower
            or "monthly" in question_lower
            or "daily" in question_lower
            or "yearly" in question_lower
        ):

            chart = px.line(
                trend_df,
                x=date_column,
                y=numeric_column,
                title=(
                    f"{numeric_column} Over Time"
                ),
                markers=True,
            )

            return chart


    # ========================================================
    # CATEGORY COMPARISON
    # ========================================================

    if categorical_columns and numeric_columns:

        category_column = categorical_columns[0]

        numeric_column = numeric_columns[0]


        grouped = (
            df.groupby(
                category_column,
                dropna=False
            )[numeric_column]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(15)
            .reset_index()
        )


        if (
            "compare" in question_lower
            or "by" in question_lower
            or "highest" in question_lower
            or "lowest" in question_lower
            or "top" in question_lower
            or "most" in question_lower
            or "best" in question_lower
            or "show" in question_lower
        ):

            chart = px.bar(
                grouped,
                x=category_column,
                y=numeric_column,
                title=(
                    f"{numeric_column} by "
                    f"{category_column}"
                ),
            )

            return chart


    # ========================================================
    # DISTRIBUTION
    # ========================================================

    if numeric_columns:

        numeric_column = numeric_columns[0]


        if (
            "distribution" in question_lower
            or "spread" in question_lower
            or "frequency" in question_lower
            or "histogram" in question_lower
        ):

            chart = px.histogram(
                df,
                x=numeric_column,
                title=(
                    f"Distribution of "
                    f"{numeric_column}"
                ),
            )

            return chart


    # ========================================================
    # CORRELATION
    # ========================================================

    if len(numeric_columns) >= 2:

        if (
            "correlation" in question_lower
            or "relationship" in question_lower
            or "related" in question_lower
        ):

            correlation_df = (
                df[numeric_columns]
                .corr()
            )


            chart = px.imshow(
                correlation_df,
                text_auto=True,
                title="Correlation Matrix",
            )

            return chart


    # ========================================================
    # DEFAULT VISUALIZATION
    # ========================================================

    if (
        categorical_columns
        and numeric_columns
    ):

        category_column = (
            categorical_columns[0]
        )

        numeric_column = (
            numeric_columns[0]
        )


        grouped = (
            df.groupby(
                category_column,
                dropna=False
            )[numeric_column]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )


        chart = px.bar(
            grouped,
            x=category_column,
            y=numeric_column,
            title=(
                f"{numeric_column} by "
                f"{category_column}"
            ),
        )

        return chart


    return None