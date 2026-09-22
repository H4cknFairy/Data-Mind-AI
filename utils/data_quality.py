import pandas as pd
import numpy as np


# =========================================================
# DATA QUALITY SUMMARY
# =========================================================

def get_data_quality_summary(df: pd.DataFrame) -> dict:

    total_cells = df.shape[0] * df.shape[1]

    missing_cells = df.isnull().sum().sum()

    duplicate_rows = df.duplicated().sum()

    if total_cells > 0:
        completeness = (
            (total_cells - missing_cells)
            / total_cells
        ) * 100
    else:
        completeness = 100

    # Start with 100 and reduce score for issues
    score = 100

    # Missing value penalty
    if total_cells > 0:
        missing_percentage = (
            missing_cells / total_cells
        ) * 100

        score -= min(
            missing_percentage * 2,
            30
        )

    # Duplicate penalty
    if len(df) > 0:

        duplicate_percentage = (
            duplicate_rows / len(df)
        ) * 100

        score -= min(
            duplicate_percentage,
            20
        )

    score = max(
        0,
        round(score, 2)
    )

    return {
        "total_cells": total_cells,
        "missing_cells": int(missing_cells),
        "duplicate_rows": int(duplicate_rows),
        "completeness": round(
            completeness,
            2
        ),
        "quality_score": score,
    }


# =========================================================
# MISSING VALUES
# =========================================================

def get_missing_values(df: pd.DataFrame) -> pd.DataFrame:

    missing = df.isnull().sum()

    missing = missing[
        missing > 0
    ]

    if missing.empty:

        return pd.DataFrame(
            columns=[
                "Column",
                "Missing Values",
                "Missing Percentage",
            ]
        )

    result = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values,
    })

    result["Missing Percentage"] = (
        result["Missing Values"]
        / len(df)
        * 100
    ).round(2)

    return result.sort_values(
        "Missing Values",
        ascending=False
    )


# =========================================================
# DUPLICATE ROWS
# =========================================================

def get_duplicate_rows(
    df: pd.DataFrame
) -> pd.DataFrame:

    duplicates = df[
        df.duplicated(
            keep=False
        )
    ]

    return duplicates


# =========================================================
# NUMERICAL OUTLIERS
# =========================================================

def detect_outliers(
    df: pd.DataFrame
) -> dict:

    outliers = {}

    numeric_columns = (
        df.select_dtypes(
            include=np.number
        ).columns
    )

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = (
            q1 - 1.5 * iqr
        )

        upper_bound = (
            q3 + 1.5 * iqr
        )

        mask = (
            (df[column] < lower_bound)
            |
            (df[column] > upper_bound)
        )

        outlier_data = df[
            mask
        ]

        if not outlier_data.empty:

            outliers[column] = {
                "count": len(
                    outlier_data
                ),
                "lower_bound": round(
                    lower_bound,
                    2
                ),
                "upper_bound": round(
                    upper_bound,
                    2
                ),
                "rows": outlier_data,
            }

    return outliers


# =========================================================
# EXTREME TRANSACTIONS
# =========================================================

def detect_extreme_transactions(
    df: pd.DataFrame,
    column: str = "Revenue",
    top_n: int = 5
) -> pd.DataFrame:

    if column not in df.columns:

        return pd.DataFrame()

    return (
        df.sort_values(
            by=column,
            ascending=False
        )
        .head(top_n)
        .copy()
    )


# =========================================================
# DATA QUALITY RECOMMENDATIONS
# =========================================================

def get_quality_recommendations(
    df: pd.DataFrame
) -> list:

    recommendations = []

    # -----------------------------------------------------
    # Missing values
    # -----------------------------------------------------

    missing_count = (
        df.isnull().sum().sum()
    )

    if missing_count > 0:

        recommendations.append(
            "Handle missing values before "
            "performing advanced analysis."
        )

    else:

        recommendations.append(
            "No missing values detected."
        )


    # -----------------------------------------------------
    # Duplicate rows
    # -----------------------------------------------------

    duplicate_count = (
        df.duplicated().sum()
    )

    if duplicate_count > 0:

        recommendations.append(
            f"Review and remove {duplicate_count} "
            "duplicate rows if they are not legitimate."
        )

    else:

        recommendations.append(
            "No duplicate rows detected."
        )


    # -----------------------------------------------------
    # Numerical outliers
    # -----------------------------------------------------

    outliers = detect_outliers(df)

    if outliers:

        total_outliers = sum(
            item["count"]
            for item in outliers.values()
        )

        recommendations.append(
            f"{total_outliers} potential numerical "
            "outlier records detected. Review them "
            "before making business decisions."
        )

    else:

        recommendations.append(
            "No significant numerical outliers detected."
        )


    # -----------------------------------------------------
    # Constant columns
    # -----------------------------------------------------

    constant_columns = []

    for column in df.columns:

        if df[column].nunique(
            dropna=False
        ) <= 1:

            constant_columns.append(
                column
            )

    if constant_columns:

        recommendations.append(
            "Consider removing constant columns: "
            + ", ".join(
                constant_columns
            )
        )


    return recommendations