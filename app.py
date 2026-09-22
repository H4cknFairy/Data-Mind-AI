
import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DataMind AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# BRIGHT SKY BLUE + DARK BLUE UI
# ============================================================

st.markdown(
    """
    <style>
        :root {
            --navy: #0b1f3a;
            --navy-2: #12345b;
            --blue: #0ea5e9;
            --blue-dark: #0284c7;
            --sky: #e0f2fe;
            --sky-soft: #f0f9ff;
            --page: #f5faff;
            --text: #0f172a;
            --muted: #64748b;
            --border: #dbe7f2;
            --white: #ffffff;
        }

        /* ---------- APP ---------- */

        .stApp {
            background:
                radial-gradient(circle at 85% 5%, rgba(14,165,233,0.10), transparent 24%),
                linear-gradient(180deg, #f8fcff 0%, #f3f8fd 100%);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu,
        footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 1250px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }

        /* ---------- GLOBAL TEXT ---------- */

        h1, h2, h3, h4 {
            color: var(--text) !important;
            letter-spacing: -0.025em;
        }

        p, label, .stCaption {
            color: var(--muted);
        }

        hr {
            border: 0;
            border-top: 1px solid var(--border);
            margin: 2rem 0;
        }

        /* ---------- SIDEBAR ---------- */

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #081a31 0%, #0d2948 100%);
            border-right: 1px solid #173a60;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 2rem;
            padding-left: 1.45rem;
            padding-right: 1.45rem;
        }

        [data-testid="stSidebar"] .sidebar-brand {
            color: #ffffff !important;
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 3px;
        }

        [data-testid="stSidebar"] .sidebar-subtitle {
            color: #a9d8f5 !important;
            font-size: 13px;
            margin-bottom: 28px;
        }

        [data-testid="stSidebar"] .sidebar-heading {
            color: #7dd3fc !important;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.13em;
            text-transform: uppercase;
            margin-top: 25px;
            margin-bottom: 10px;
        }

        [data-testid="stSidebar"] .sidebar-help {
            color: #c8def0 !important;
            font-size: 13px;
            line-height: 1.8;
        }

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            color: #a9bfd3 !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploader"] {
            background: rgba(255,255,255,0.98);
            border-radius: 14px;
            padding: 8px;
            border: 1px solid #cfe8f7;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploader"] * {
            color: #334155 !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploader"] button {
            background: #e0f2fe !important;
            color: #075985 !important;
            border: 1px solid #7dd3fc !important;
            border-radius: 9px !important;
            font-weight: 700 !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
            background: #bae6fd !important;
            border-color: #38bdf8 !important;
        }

        [data-testid="stSidebar"] [data-testid="stAlert"] {
            border-radius: 12px;
        }

        [data-testid="stSidebar"] .stMarkdown ul {
            padding-left: 1.15rem;
        }

        [data-testid="stSidebar"] .stMarkdown li {
            color: #e4f2fb !important;
            margin-bottom: 7px;
        }

        /* ---------- HERO ---------- */

        .hero {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
            border: 1px solid #cfe5f3;
            border-radius: 24px;
            padding: 38px 44px;
            margin-bottom: 30px;
            box-shadow: 0 16px 45px rgba(11,31,58,0.08);
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 230px;
            height: 230px;
            border-radius: 50%;
            right: -80px;
            top: -110px;
            background: rgba(14,165,233,0.13);
        }

        .hero-label {
            color: #0284c7;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .hero-title {
            color: #0b1f3a;
            font-size: 40px;
            font-weight: 850;
            line-height: 1.1;
            margin-bottom: 12px;
        }

        .hero-text {
            color: #52677d;
            font-size: 16px;
            line-height: 1.75;
            max-width: 820px;
        }

        .ready-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 18px;
            padding: 8px 13px;
            background: #e0f2fe;
            color: #075985;
            border: 1px solid #bae6fd;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
        }

        .ready-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #0ea5e9;
            display: inline-block;
        }

        /* ---------- SECTION HEADINGS ---------- */

        .section-title {
            color: #0b1f3a;
            font-size: 25px;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .section-description {
            color: #64748b;
            font-size: 14px;
            margin-bottom: 16px;
        }

        /* ---------- INFO / START CARD ---------- */

        .start-card {
            background: #ffffff;
            border: 1px solid #d8e7f2;
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: 0 8px 25px rgba(11,31,58,0.05);
        }

        .start-number {
            display: inline-flex;
            width: 30px;
            height: 30px;
            align-items: center;
            justify-content: center;
            background: #e0f2fe;
            color: #0369a1;
            border-radius: 50%;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .start-title {
            color: #0f172a;
            font-weight: 750;
            font-size: 16px;
        }

        .start-text {
            color: #64748b;
            font-size: 13px;
            line-height: 1.6;
        }

        /* ---------- METRICS ---------- */

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #d7e6f1;
            border-radius: 17px;
            padding: 18px 20px;
            box-shadow: 0 7px 24px rgba(11,31,58,0.055);
        }

        div[data-testid="stMetricLabel"] {
            color: #64748b !important;
            font-weight: 600 !important;
        }

        div[data-testid="stMetricValue"] {
            color: #0b1f3a !important;
            font-weight: 800 !important;
        }

        /* ---------- TABS ---------- */

        button[data-baseweb="tab"] {
            color: #64748b !important;
            font-weight: 700 !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #0284c7 !important;
        }

        div[data-baseweb="tab-highlight"] {
            background: #0ea5e9 !important;
        }

        /* ---------- INPUTS ---------- */

        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        div[data-baseweb="select"] > div {
            background: #ffffff !important;
            border: 1px solid #cbddea !important;
            border-radius: 11px !important;
        }

        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {
            color: #0f172a !important;
        }

        div[data-baseweb="input"] input::placeholder,
        div[data-baseweb="textarea"] textarea::placeholder {
            color: #94a3b8 !important;
        }

        /* ---------- BUTTONS ---------- */

        .stButton > button {
            min-height: 42px;
            border-radius: 11px !important;
            border: 1px solid #cbddea !important;
            background: #ffffff !important;
            color: #0f172a !important;
            font-weight: 650 !important;
            transition: 0.15s ease;
        }

        .stButton > button:hover {
            border-color: #38bdf8 !important;
            color: #0369a1 !important;
            background: #f0f9ff !important;
        }

        /* Primary button - support multiple Streamlit versions */
        div.stButton > button[kind="primary"],
        button[data-testid="stBaseButton-primary"] {
            background: linear-gradient(135deg, #0284c7, #0ea5e9) !important;
            border: 1px solid #0284c7 !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            box-shadow: 0 7px 18px rgba(14,165,233,0.25);
        }

        div.stButton > button[kind="primary"] *,
        button[data-testid="stBaseButton-primary"] * {
            color: #ffffff !important;
        }

        div.stButton > button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover {
            background: linear-gradient(135deg, #0369a1, #0284c7) !important;
            color: #ffffff !important;
        }

        /* ---------- DATAFRAME ---------- */

        [data-testid="stDataFrame"] {
            border: 1px solid #d7e6f1;
            border-radius: 14px;
            overflow: hidden;
            background: white;
        }

        /* ---------- ALERTS ---------- */

        [data-testid="stAlert"] {
            border-radius: 13px !important;
        }

        /* ---------- ANALYSIS AREA ---------- */

        .analysis-header {
            background: linear-gradient(135deg, #effaff 0%, #e0f2fe 100%);
            border: 1px solid #bae6fd;
            border-radius: 16px;
            padding: 17px 20px;
            color: #075985;
            font-weight: 750;
            margin-bottom: 12px;
        }

        .question-hint {
            color: #64748b;
            font-size: 13px;
            margin-top: -5px;
            margin-bottom: 10px;
        }

        /* ---------- FOOTER ---------- */

        .footer {
            text-align: center;
            color: #8aa0b5;
            font-size: 12px;
            padding: 34px 0 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "df" not in st.session_state:
    st.session_state.df = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = None


# ============================================================
# DATA LOADING
# ============================================================

def load_uploaded_file(uploaded_file):
    """Load CSV or Excel into a DataFrame."""
    try:
        file_name = uploaded_file.name.lower()

        if file_name.endswith(".csv"):
            return pd.read_csv(uploaded_file)

        if file_name.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)

        st.error("Please upload a CSV or Excel file.")
        return None

    except Exception as exc:
        st.error(f"Could not read the file: {exc}")
        return None


# ============================================================
# HELPERS
# ============================================================

def numeric_columns(df):
    return df.select_dtypes(include="number").columns.tolist()


def missing_count(df):
    return int(df.isna().sum().sum())


def safe_local_analysis(df, question):
    """
    Use deterministic local analysis first.
    If it cannot answer the question, fall back to the AI analyzer.
    """
    try:
        from agent.fallback_analyzer import local_analysis
        return local_analysis(df, question)
    except Exception as local_error:
        try:
            from agent.analyst import analyze_question
            return analyze_question(df, question)
        except Exception as ai_error:
            return (
                "### Analysis unavailable\n\n"
                f"Local analysis error: {local_error}\n\n"
                f"AI analysis error: {ai_error}"
            )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">📊 DataMind AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">Intelligent Data Analyst</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-heading">Dataset</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"],
        help="Upload a dataset to start exploring it.",
    )

    if uploaded_file is not None:
        if st.session_state.file_name != uploaded_file.name:
            loaded_df = load_uploaded_file(uploaded_file)

            if loaded_df is not None:
                st.session_state.df = loaded_df
                st.session_state.file_name = uploaded_file.name
                st.session_state.analysis_result = None
                st.session_state.last_question = None
                st.success("Dataset loaded successfully.")

    st.markdown(
        '<div class="sidebar-heading">What you can do</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-help">
            📋 Explore your data<br>
            📈 View quick statistics<br>
            ⚠️ Check missing values<br>
            💬 Ask questions in plain English<br>
            🧮 Run Pandas-based calculations<br>
            🤖 Get AI-assisted insights
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.df is not None:
        st.markdown(
            '<div class="sidebar-heading">Current dataset</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="sidebar-help">
                <strong style="color:#ffffff;">{st.session_state.file_name}</strong><br>
                {len(st.session_state.df):,} rows ·
                {len(st.session_state.df.columns):,} columns
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# MAIN HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">AI-POWERED DATA ANALYSIS</div>
        <div class="hero-title">Turn your data into insights.</div>
        <div class="hero-text">
            Upload a CSV or Excel dataset, explore its structure,
            and ask analytical questions in natural language.
            DataMind AI combines reliable Pandas calculations
            with AI-assisted analysis.
        </div>
        <div class="ready-pill">
            <span class="ready-dot"></span>
            DataMind AI is ready
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# NO DATA STATE
# ============================================================

df = st.session_state.df

if df is None:
    st.markdown(
        '<div class="section-title">Get started</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-description">Follow these three simple steps to get insights from your dataset.</div>',
        unsafe_allow_html=True,
    )

    st.info("Upload a CSV or Excel file from the sidebar to begin.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="start-card">
                <div class="start-number">1</div>
                <div class="start-title">Upload</div>
                <div class="start-text">
                    Choose a CSV or Excel file from the sidebar.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="start-card">
                <div class="start-number">2</div>
                <div class="start-title">Explore</div>
                <div class="start-text">
                    Review rows, columns, statistics and data quality.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="start-card">
                <div class="start-number">3</div>
                <div class="start-title">Ask</div>
                <div class="start-text">
                    Ask questions about totals, averages, trends and rankings.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="footer">DataMind AI · Python · Pandas · Streamlit</div>',
        unsafe_allow_html=True,
    )
    st.stop()


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">Dataset overview</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">A quick snapshot of the uploaded dataset.</div>',
    unsafe_allow_html=True,
)

rows = len(df)
columns = len(df.columns)
numeric_count = len(numeric_columns(df))
missing = missing_count(df)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Rows", f"{rows:,}")

with m2:
    st.metric("Columns", f"{columns:,}")

with m3:
    st.metric("Numeric columns", f"{numeric_count:,}")

with m4:
    st.metric("Missing values", f"{missing:,}")


# ============================================================
# EXPLORE DATASET
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">Explore your dataset</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">Use the tabs below to inspect your data.</div>',
    unsafe_allow_html=True,
)

tab_preview, tab_stats, tab_quality = st.tabs(
    ["🔎 Data preview", "📊 Statistics", "⚠️ Data quality"]
)

with tab_preview:
    st.dataframe(
        df.head(100),
        use_container_width=True,
        height=430,
    )

with tab_stats:
    try:
        stats = df.describe(include="all").transpose()
        st.dataframe(
            stats,
            use_container_width=True,
            height=430,
        )
    except Exception:
        st.info("Statistics could not be generated for this dataset.")

with tab_quality:
    quality = pd.DataFrame(
        {
            "Column": df.columns,
            "Data type": [str(df[c].dtype) for c in df.columns],
            "Missing": [int(df[c].isna().sum()) for c in df.columns],
            "Missing %": [
                round(float(df[c].isna().mean() * 100), 2)
                for c in df.columns
            ],
            "Unique values": [
                int(df[c].nunique(dropna=True))
                for c in df.columns
            ],
        }
    )

    st.dataframe(
        quality,
        use_container_width=True,
        height=430,
    )


# ============================================================
# QUICK VISUALIZATION
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">Quick visualization</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">Select a numeric column to quickly view its values.</div>',
    unsafe_allow_html=True,
)

num_cols = numeric_columns(df)

if num_cols:
    selected_numeric = st.selectbox(
        "Choose a numeric column",
        num_cols,
    )

    chart_data = df[[selected_numeric]].copy()
    chart_data[selected_numeric] = pd.to_numeric(
        chart_data[selected_numeric],
        errors="coerce",
    )

    st.line_chart(
        chart_data,
        use_container_width=True,
    )
else:
    st.info("No numeric columns are available for visualization.")


# ============================================================
# ASK DATAMIND
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">Ask DataMind</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">Ask questions about your uploaded dataset using natural language.</div>',
    unsafe_allow_html=True,
)

question = st.text_input(
    "Your question",
    placeholder="Example: What is the average revenue by region?",
    label_visibility="collapsed",
)

st.markdown(
    '<div class="question-hint">Tip: You can ask for totals, averages, rankings, comparisons, missing values and more.</div>',
    unsafe_allow_html=True,
)

example_questions = [
    "What is the total revenue?",
    "Which product sold the most?",
    "What are the top 5 products by revenue?",
    "Show revenue by region",
    "What is the average revenue by salesperson?",
]

st.markdown("**Try an example**")

example_cols = st.columns(len(example_questions))

for i, example in enumerate(example_questions):
    with example_cols[i]:
        if st.button(
            example,
            key=f"example_{i}",
            use_container_width=True,
        ):
            st.session_state.last_question = example
            st.rerun()


if st.session_state.last_question:
    question = st.session_state.last_question
    st.markdown(
        f'<div class="analysis-header">Selected question: {question}</div>',
        unsafe_allow_html=True,
    )


if st.button(
    "✨ Analyze dataset",
    type="primary",
    use_container_width=True,
):
    if not question or not question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Analyzing your dataset..."):
            result = safe_local_analysis(
                df,
                question.strip(),
            )

        st.session_state.analysis_result = result
        st.session_state.last_question = question.strip()


# ============================================================
# ANALYSIS RESULT
# ============================================================

if st.session_state.analysis_result:
    st.markdown("---")

    st.markdown(
        '<div class="section-title">Analysis result</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-description">Calculated from your uploaded dataset.</div>',
        unsafe_allow_html=True,
    )

    # Analyzer returns Markdown, so render it normally.
    st.markdown(st.session_state.analysis_result)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">DataMind AI · Python · Pandas · Streamlit · Generative AI</div>',
    unsafe_allow_html=True,
)
