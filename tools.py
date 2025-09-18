# Importing necessary libraries and modules
import os
from dotenv import load_dotenv
from crewai.tools import BaseTool, tool
from pypdf import PdfReader
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client for NVIDIA models
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def get_llm_response(prompt):
    """
    This function communicates with the NVIDIA model to get a response.
    """
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        top_p=0.7,
        max_tokens=4096,
        stream=False  # Changed to False for simplicity in this context
    )
    return completion.choices[0].message.content

@tool
def read_financial_document(file_path: str) -> str:
    """
    Reads a financial document from a PDF file and returns its content as a string.
    The file path is passed as an argument.
    """
    try:
        reader = PdfReader(file_path)
        full_report = ""
        for page in reader.pages:
            full_report += page.extract_text() + "\n"
        
        # Clean up the text by removing excessive newlines
        while "\n\n" in full_report:
            full_report = full_report.replace("\n\n", "\n")
            
        return full_report
    except Exception as e:
        return f"Error reading PDF file: {e}"

@tool
def analyze_investment(financial_document_data: str) -> str:
    """
    Analyzes financial data to provide investment insights.
    This tool uses an LLM to generate the analysis.
    
    Args:
        financial_document_data (str): The financial data to be analyzed.
        
    Returns:
        str: Investment analysis and recommendations.
    """
    prompt = f"""
    As a senior financial analyst, your task is to provide a detailed investment analysis based on the provided financial data.

    **Financial Data:**
    {financial_document_data}

    **Analysis Requirements:**
    1.  **Key Metrics:**
        *   Revenue Growth (YoY)
        *   Net Income (GAAP and Non-GAAP, if available)
        *   Earnings Per Share (EPS) (GAAP and Non-GAAP, if available)
        *   Operating Margin
        *   Debt-to-Equity Ratio (calculated as Total Debt / Equity, not Total Liabilities / Equity)
        *   Free Cash Flow (FCF)
    2.  **Growth Areas:**
        *   Identify and elaborate on 2-3 potential growth areas, citing specific data from the document.
    3.  **Market Position:**
        *   Assess the company's market position relative to its key competitors, mentioning strengths and weaknesses.
    4.  **Investment Recommendation:**
        *   Provide a clear "Buy", "Hold", or "Sell" recommendation. The rationale should be framed from a fiduciary perspective, suitable for investors with a specific risk tolerance (e.g., "This investment is suitable for investors with a high-risk tolerance due to...").

    **Important Notes:**
    *   **Precision:** Use precise figures as reported in the financial document. Avoid rounding where possible, especially for EPS and growth percentages.
    *   **Clarity:** Ensure the analysis is clear, concise, and avoids jargon where possible.

    **Output Format:**
    Provide the analysis in a structured format with clear headings for each section.
    """
    return get_llm_response(prompt)

@tool
def assess_risk(financial_document_data: str) -> str:
    """
    Assesses the risks associated with an investment based on financial data.
    This tool uses an LLM to generate the risk assessment.
    
    Args:
        financial_document_data (str): The financial data for risk assessment.
        
    Returns:
        str: A detailed risk assessment.
    """
    prompt = f"""
    As a risk assessment expert, your task is to identify and evaluate potential risks based on the provided financial data.

    **Financial Data:**
    {financial_document_data}

    **Risk Assessment Requirements:**
    1.  **Identify Key Risks:**
        *   List all identifiable risks (e.g., market, operational, financial, regulatory, technological).
    2.  **Categorize Risks:**
        *   Group the risks into logical, non-overlapping categories to avoid redundancy.
    3.  **Assess Severity and Impact:**
        *   Assign a severity level (Low, Medium, High) and potential impact to each risk.
    4.  **Provide Mitigation Strategies:**
        *   For each "High" severity risk, suggest a concrete and actionable mitigation strategy.
    5.  **Quantitative Analysis:**
        *   Where possible, quantify the potential financial impact of the most critical risks.

    **Output Format:**
    Provide the risk assessment as a structured report with clear headings for each section.
    """
    return get_llm_response(prompt)
