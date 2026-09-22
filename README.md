# DataMind AI

DataMind AI is a Streamlit application for exploring tabular data with natural-language analysis. Upload a CSV or Excel workbook, inspect the dataset profile and quality signals, generate visualizations, and ask questions about the data.

## Features

- Upload CSV, XLS, and XLSX files
- Inspect rows, columns, data types, missing values, and summary statistics
- Review data-quality findings
- Ask analysis questions in plain language
- Generate charts and tabular results
- Use deterministic local analysis when AI analysis is unavailable

## Requirements

- Python 3.10 or newer
- An optional Gemini API key for AI-assisted analysis

## Setup

1. Clone the repository and open the project directory:

   ```powershell
   git clone https://github.com/H4cknFairy/Data-Mind-AI.git
   cd Data-Mind-AI
   ```

2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your own Gemini API key:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

   Keep `.env` private. It is excluded from Git by `.gitignore`.

## Run the app

```powershell
streamlit run app.py
```

Streamlit will print a local URL, normally `http://localhost:8501`.

## Deploy on Streamlit Community Cloud

1. Open [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2. Select **Create app** and choose the `H4cknFairy/Data-Mind-AI` repository.
3. Set the branch to `main` and the main file to `app.py`.
4. Open **Advanced settings**, add this secret, and replace the placeholder with your own key:

   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

5. Select **Deploy**. Streamlit will provide a live URL for the app.

Keep the live URL in the repository description or add it here after deployment:

```text
Live app: https://your-app-name.streamlit.app
```

Do not commit `.env` or API keys to GitHub. Configure secrets through Streamlit Community Cloud instead.

## Project structure

```text
.
├── agent/       Analysis, chart, code-generation, and execution agents
├── ui/          Streamlit UI components
├── utils/       Data loading, profiling, quality, and visualization helpers
├── app.py       Streamlit application entry point
└── requirements.txt
```

## Security

Never commit API keys, uploaded datasets containing sensitive information, or other secrets. Rotate any key that has been exposed and replace it only in your local `.env` file.
