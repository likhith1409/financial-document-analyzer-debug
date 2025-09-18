# Importing necessary libraries and modules
import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
from tools import read_financial_document, analyze_investment, assess_risk

# Load environment variables from .env file
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the OpenAI client for NVIDIA models
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

# Define the LLM to be used by the agents
llm = client

import asyncio

async def _get_text_from_tools(tools, file_path: str) -> str:
    """Helper to extract text using the first provided tool. Handles both sync and async tool objects."""
    if not tools:
        return ""
    tool = tools[0]
    # If tool has run, call it
    if hasattr(tool, "run"):
        return await asyncio.to_thread(tool.run, file_path)
    # If tool is a callable function
    if callable(tool):
        try:
            return await asyncio.to_thread(tool, file_path)
        except Exception:
            return ""
    return ""

class FinancialAnalystAgent:
    async def run(self, payload: dict, tools: list):
        file_path = payload.get("file_path")
        query = payload.get("query")
        document_text = await _get_text_from_tools(tools, file_path)
        if not document_text or document_text.startswith("Error"):
            return "Could not read the document."

        analysis = await asyncio.to_thread(analyze_investment.run, document_text)
        return analysis

async def generate_with_fallback(prompt):
    """Generate content with Gemini and fallback to Nvidia."""
    try:
        # Try Gemini first
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text
    except Exception as e:
        print(f"Gemini failed: {e}. Falling back to Nvidia.")
        # Fallback to Nvidia
        completion = llm.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=False
        )
        return completion.choices[0].message.content

class InvestmentAdvisorAgent:
    async def run(self, payload: dict, tools: list):
        previous_task_result = payload.get("previous_task_result")
        if not previous_task_result:
            return "No analysis from the previous agent to provide advice on."

        # Use a prompt to generate advice based on the previous analysis
        prompt = f"Based on the following financial analysis, provide investment advice:\n\n{previous_task_result}"
        
        advice = await generate_with_fallback(prompt)
        return advice

class RiskAssessorAgent:
    async def run(self, payload: dict, tools: list):
        file_path = payload.get("file_path")
        document_text = await _get_text_from_tools(tools, file_path)
        if not document_text or document_text.startswith("Error"):
            return "Could not read the document."

        risk_assessment = await asyncio.to_thread(assess_risk.run, document_text)
        return risk_assessment

# Instances exported for task.py
financial_analyst = FinancialAnalystAgent()
investment_advisor = InvestmentAdvisorAgent()
risk_assessor = RiskAssessorAgent()
