import os

from dotenv import load_dotenv
import google.generativeai as genai

# Loads environment variables from .env (including GEMINI_API_KEY).
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    # Fail fast if the key is missing, so you notice immediately.
    raise RuntimeError("GEMINI_API_KEY is not set in the environment/.env file.")

# Configure the Gemini client with your API key.
genai.configure(api_key=API_KEY)

# Creates a reusable Gemini model instance.
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_insight(
    filename: str,
    rows: int,
    columns: int,
    column_types: dict,
    missing: dict,
    summary: str,
    correlations: str,
):
    """
    Generates a natural-language insight for a CSV dataset using Gemini.
    """

    prompt = f"""
You are a senior data analyst and product strategist.

Dataset name: {filename}
Rows: {rows}
Columns: {columns}

Column types:
{column_types}

Missing values:
{missing}

Summary statistics:
{summary}

Correlation matrix:
{correlations}

Instructions:
- Briefly explain what this dataset likely represents.
- Highlight 3–5 interesting or business-relevant insights.
- Mention any data quality issues.
- Suggest next analysis steps.
- Keep it under 200 words.
"""

    try:
        response = model.generate_content(prompt)
        return (response.text or "").strip()
    except Exception as e:
        return f"AI insight generation failed: {e}"

