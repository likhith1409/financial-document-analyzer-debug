# Importing necessary libraries and modules
from agents import financial_analyst, investment_advisor, risk_assessor
from tools import read_financial_document, analyze_investment, assess_risk

class CustomTask:
    def __init__(self, description, expected_output, agent, tools, async_execution):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.tools = tools
        self.async_execution = async_execution

# Task 1: Financial Analysis
analyze_financial_document = CustomTask(
    description=(
        "Analyze the financial document at {file_path} to identify key financial metrics, "
        "performance indicators, and overall market positioning. Your analysis will serve as the "
        "foundation for subsequent investment and risk assessments."
    ),
    expected_output=(
        "A comprehensive report detailing the financial health of the entity, including "
        "an analysis of its revenue, profitability, cash flow, and balance sheet. "
        "Highlight any significant trends or anomalies."
    ),
    agent=financial_analyst,
    tools=[read_financial_document, analyze_investment],
    async_execution=False,
)

# Task 2: Investment Advising
investment_analysis = CustomTask(
    description=(
        "Based on the financial analysis, develop a strategic investment plan. "
        "Your recommendations should be tailored to the user's query and take into "
        "account long-term growth potential and market opportunities."
    ),
    expected_output=(
        "A detailed investment strategy that includes specific recommendations, "
        "potential returns, and a clear rationale. The strategy should be aligned with "
        "the findings of the financial analysis and risk assessment."
    ),
    agent=investment_advisor,
    tools=[analyze_investment, assess_risk],
    async_execution=False,
)

# Task 3: Risk Assessment
risk_assessment = CustomTask(
    description=(
        "Conduct a thorough risk assessment of the investment opportunities identified "
        "in the financial analysis of the document at {file_path}. Your evaluation should cover market risks, operational risks, "
        "and any other potential threats to the investment."
    ),
    expected_output=(
        "A comprehensive risk report that outlines all identified risks, their potential impact, "
        "and recommended mitigation strategies. This report will help in making a well-informed "
        "investment decision."
    ),
    agent=risk_assessor,
    tools=[read_financial_document, assess_risk],
    async_execution=False,
)
