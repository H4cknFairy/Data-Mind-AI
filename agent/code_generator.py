import os

from dotenv import load_dotenv
from google import genai

from agent.prompt import build_analysis_prompt


load_dotenv()


# ============================================================
# GEMINI CLIENT
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    try:
        client = genai.Client(
            api_key=API_KEY
        )
    except Exception:
        client = None


# ============================================================
# GENERATE PANDAS CODE
# ============================================================

def generate_analysis_code(
    question,
    dataset_profile,
):
    """
    Ask Gemini to generate Pandas analysis code
    based on the uploaded dataset.
    """

    if client is None:
        raise RuntimeError(
            "Gemini API key is not configured."
        )

    prompt = build_analysis_prompt(
        question=question,
        dataset_profile=dataset_profile,
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    if not response or not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    code = response.text.strip()

    # Remove Markdown code fences
    if code.startswith("```python"):
        code = code[len("```python"):].strip()

    elif code.startswith("```"):
        code = code[3:].strip()

    if code.endswith("```"):
        code = code[:-3].strip()

    return code