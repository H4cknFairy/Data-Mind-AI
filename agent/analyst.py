import json
import pandas as pd

from agent.code_generator import generate_analysis_code
from agent.executor import execute_analysis
from agent.fallback_analyzer import local_analysis


# ============================================================
# DATASET PROFILE
# ============================================================

def build_dataset_profile(df: pd.DataFrame) -> str:
    """
    Creates a compact description of the uploaded dataset.
    This profile is provided to the AI so it can understand
    the uploaded dataset dynamically.
    """

    profile = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(df.columns),

        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },

        "missing_values": {
            column: int(df[column].isna().sum())
            for column in df.columns
        },
    }

    # --------------------------------------------------------
    # Numeric information
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        numeric_summary = {}

        for column in numeric_columns:

            values = df[column].dropna()

            numeric_summary[column] = {
                "min": float(values.min())
                if not values.empty else None,

                "max": float(values.max())
                if not values.empty else None,

                "mean": float(values.mean())
                if not values.empty else None,
            }

        profile["numeric_summary"] = numeric_summary

    # --------------------------------------------------------
    # Sample rows
    # --------------------------------------------------------

    sample = df.head(5).copy()

    profile["sample_rows"] = json.loads(
        sample.to_json(
            orient="records",
            date_format="iso"
        )
    )

    # --------------------------------------------------------
    # Categorical information
    # --------------------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    categorical_summary = {}

    for column in categorical_columns:

        values = (
            df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        # Limit prompt size
        categorical_summary[column] = values[:20]

    if categorical_summary:

        profile["categorical_values"] = (
            categorical_summary
        )

    return json.dumps(
        profile,
        indent=2,
        default=str
    )


# ============================================================
# RESULT FORMATTING
# ============================================================

def format_result(result):
    """
    Converts Pandas results into readable text.
    """

    # DataFrame
    if isinstance(result, pd.DataFrame):

        if result.empty:
            return (
                "The analysis returned "
                "no matching records."
            )

        return result.to_markdown(
            index=False
        )

    # Series
    if isinstance(result, pd.Series):

        if result.empty:
            return (
                "The analysis returned "
                "no results."
            )

        return result.to_frame().to_markdown(
            index=True
        )

    # Dictionary
    if isinstance(result, dict):

        return json.dumps(
            result,
            indent=2,
            default=str
        )

    # List / tuple
    if isinstance(result, (list, tuple)):

        return json.dumps(
            result,
            indent=2,
            default=str
        )

    # Scalar
    if isinstance(result, (int, float)):

        return f"{result:,.2f}"

    return str(result)


# ============================================================
# MAIN ANALYST
# ============================================================

def analyze_question(
    df: pd.DataFrame,
    question: str
) -> str:

    # --------------------------------------------------------
    # Validate dataset
    # --------------------------------------------------------

    if df is None or df.empty:

        return (
            "### ⚠️ Empty Dataset\n\n"
            "The uploaded dataset is empty. "
            "Please upload a dataset containing data."
        )

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    if not question or not question.strip():

        return (
            "### ⚠️ Missing Question\n\n"
            "Please enter a question about "
            "your uploaded dataset."
        )

    question = question.strip()

    # --------------------------------------------------------
    # Build dataset profile
    # --------------------------------------------------------

    dataset_profile = build_dataset_profile(df)

    # ========================================================
    # FIRST: TRY GEMINI AI
    # ========================================================

    try:

        generated_code = generate_analysis_code(
            question=question,
            dataset_profile=dataset_profile
        )

        # Make sure code was generated
        if not generated_code:

            raise ValueError(
                "The AI did not generate analysis code."
            )

        # ----------------------------------------------------
        # Execute generated Pandas code
        # ----------------------------------------------------

        result = execute_analysis(
            code=generated_code,
            df=df
        )

        # ----------------------------------------------------
        # Format verified result
        # ----------------------------------------------------

        formatted_result = format_result(result)

        return (
            "### 🤖 DataMind AI Analysis\n\n"

            f"**Question:** {question}\n\n"

            "### 📊 Verified Dataset Result\n\n"

            f"{formatted_result}\n\n"

            "---\n\n"

            "✅ This result was calculated directly "
            "from the uploaded dataset using Pandas."
        )

    # ========================================================
    # GEMINI FAILED → LOCAL FALLBACK
    # ========================================================

    except Exception as ai_error:

        # ----------------------------------------------------
        # Try local Pandas analyzer
        # ----------------------------------------------------

        try:

            fallback_result = local_analysis(
                df,
                question
            )

            # If fallback understands the question
            if fallback_result:

                return (
                    f"{fallback_result}\n\n"
                    "---\n\n"
                    "🛡️ **Fallback Mode:** "
                    "Gemini AI was temporarily unavailable, "
                    "so DataMind calculated this answer "
                    "directly from the uploaded dataset."
                )

        except Exception as fallback_error:

            return (
                "### ⚠️ DataMind AI could not complete "
                "the analysis\n\n"

                f"**AI Error:** {str(ai_error)}\n\n"

                f"**Fallback Error:** "
                f"{str(fallback_error)}"
            )

        # ----------------------------------------------------
        # Neither AI nor fallback understood question
        # ----------------------------------------------------

        return (
            "### ⚠️ DataMind AI could not complete "
            "the analysis\n\n"

            "Gemini AI was temporarily unavailable, "
            "and the local analyzer could not identify "
            "a suitable calculation for this question.\n\n"

            f"**AI Error:** {str(ai_error)}\n\n"

            "Try asking a question involving columns "
            "from your uploaded dataset."
        )