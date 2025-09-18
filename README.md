# Financial Document Analyzer

A full-stack AI application that analyzes financial documents using a team of specialized agents. Users can register, upload a PDF report, and receive a comprehensive analysis covering financial health, investment advice, and risk assessment. All analyses are saved to a user-specific history.

**Live Demo**: https://likhithreddy.redirectme.net
<img width="1910" height="1042" alt="image" src="https://github.com/user-attachments/assets/87a8083d-0648-4265-87f8-5b3ac1c52d34" />


## Technology Stack

- **Backend**: FastAPI
- **Database**: MongoDB
- **AI Agents**:
  - **Primary LLM**: Google's `Gemini 2.5 Flash`
  - **Fallback LLM**: DeepSeek's `deepseek-ai/deepseek-r1` (via NVIDIA API)
- **Core Libraries**: `asyncio`, `pydantic`, `python-jose`
- **Python Version**: `3.12.8`

## Key Improvements: From Prototype to Product

This project was completely rebuilt from a non-functional prototype. The following key issues were addressed:

1.  **Broken AI Integration (File Path Bug)**:
    - **Bug**: The original code saved the uploaded document but failed to pass the file path to the AI crew. The agents were analyzing a hardcoded sample file, ignoring the user's upload.
    - **Fix**: The application logic was corrected to ensure the `file_path` of the user's document is dynamically passed into the `kickoff` payload, allowing the agents to analyze the correct file.

2.  **Unreliable Agents & Tasks**:
    - **Bug**: The original agents were satirical placeholders with no real functionality.
    - **Fix**: Redesigned agents (`FinancialAnalyst`, `InvestmentAdvisor`, `RiskAssessor`) with professional goals. Implemented a custom asynchronous `CustomCrew` to manage a sequential workflow.

3.  **Poor Quality Analysis**:
    - **Bug**: Generic prompts led to vague and unhelpful results.
    - **Fix**: Engineered highly detailed and structured prompts for the `analyze_investment` and `assess_risk` tools, guiding the LLMs to produce precise, high-quality analysis.

4.  **Stateless and Insecure**:
    - **Bug**: The app was a single endpoint with no user management or data persistence.
    - **Fix**: Introduced a full authentication system (`auth.py`) with JWT tokens and integrated a MongoDB database (`database.py`) to store user data and analysis history.

## Setup and Usage

### 1. Prerequisites
- Python 3.12.8
- MongoDB instance (local or cloud)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/likhith1409/financial-document-analyzer-debug.git
cd financial-document-analyzer-debug

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory and add your credentials:
```env
NVIDIA_API_KEY="your_nvidia_api_key"
GEMINI_API_KEY="your_gemini_api_key"
MONGO_URI="your_mongodb_connection_string"
```

### 4. Running the Application
Start the FastAPI server with the following command:
```bash
python main.py
```
The application will be running at `http://localhost:8000`. A default user (`testuser` / `testpassword`) is created automatically for easy testing.

## API Documentation

### `GET /`
- **Description**: Serves the main `index.html` page.
- **Response (200)**: An HTML page.

---

### `POST /register`
- **Description**: Registers a new user in the database.
- **Request Body**: `application/json`
  ```json
  {
    "username": "string",
    "hashed_password": "string",
    "email": "string",
    "full_name": "string",
    "disabled": false
  }
  ```
- **Response (200)**: The created user object without the hashed password.

---

### `POST /token`
- **Description**: Authenticates a user and returns an access token.
- **Request Body**: `application/x-www-form-urlencoded`
  - `username`: The user's username.
  - `password`: The user's password.
- **Response (200)**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

---

### `POST /analyze`
- **Description**: Analyzes a financial document. Requires authentication.
- **Authentication**: `Bearer <token>` in the request header.
- **Request Body**: `multipart/form-data`
  - `file`: The financial document (PDF) to be analyzed. (Required)
  - `query`: A specific query for the analysis. (Optional)
- **Response (200)**: A JSON object containing the status, query, analysis results, and the name of the processed file.
  ```json
  {
      "status": "success",
      "query": "Analyze this financial document for investment insights",
      "analysis": {
          "financial_analysis": "\n\n# Tesla Q2 2025 Investment Analysis  \n\n---\n\n## 1. Key Metrics  \n\n### **Revenue Growth (YoY):**  \n- **Total Revenues:** $22.496B (-12% YoY)  \n- **Automotive Revenues:** $16.661B (-16% YoY)  \n- **Energy & Storage Revenues:** $2.789B (-7% YoY)  \n- **Services & Other Revenues:** $3.046B (+17% YoY)  \n\n### **Net Income:**  \n- **GAAP Net Income:** $1.172B (-16% YoY)  \n- **Non-GAAP Net Income:** $1.393B (-23% YoY)  \n\n### **Earnings Per Share (EPS):**  \n- **GAAP EPS (Diluted):** $0.33 (-18% YoY)  \n- **Non-GAAP EPS (Diluted):** $0.40 (-23% YoY)  \n\n### **Operating Margin:**  \n- **GAAP Operating Margin:** 4.1% (-219 basis points YoY)  \n\n### **Debt-to-Equity Ratio:**  \n- **Total Debt:** $7.220B (Current + Non-Current Debt)  \n- **Equity:** $77.314B  \n- **Debt-to-Equity:** **0.093** (9.3%)  \n\n### **Free Cash Flow (FCF):**  \n- **FCF:** $146M (-89% YoY)  \n\n---\n\n## 2. Growth Areas  \n\n### **1. Autonomy & Robotics (Robotaxis):**  \n- **Robotaxi Service Launch:** First autonomous ride-hailing service launched in Austin (June 2025).  \n- **AI Training Capacity:** Expanded AI compute to 67k H100-equivalent GPUs (+16k H200 GPUs added in Q2).  \n- **Autonomous Delivery:** Achieved first fully autonomous vehicle delivery (30-minute drive in Austin).  \n\n### **2. Affordable Vehicle Expansion:**  \n- **New Model Ramp:** First builds of a more affordable model completed in June 2025; volume production planned for H2 2025.  \n- **Market Entry:** Launched Model Y in India (July 2025), targeting the world’s third-largest auto market.  \n\n### **3. Energy Storage Growth:**  \n- **Record Deployments:** Trailing 12-month Energy storage deployments hit 12th consecutive quarterly record.  \n- **Megafactory Shanghai:** Began Megapack deployments from Shanghai facility, improving regionalized production efficiency.  \n\n---\n\n## 3. Market Position  \n\n### **Strengths:**  \n- **Leadership in EV & Energy Storage:** Dominant position in EV production (8M+ cumulative vehicles) and energy storage (record Megapack deployments).  \n- **AI/FSD Advancements:** Cumulative FSD (Supervised) miles driven reached 5B+, with rapid improvements in autonomy software.  \n- **Global Manufacturing Footprint:** Regionalized production (e.g., Shanghai, Berlin) mitigates tariff risks and supports demand.  \n\n### **Weaknesses:**  \n- **Declining Automotive Margins:** Automotive gross margin fell to 17.2% (-71 bps YoY) due to lower ASPs, tariffs, and fixed-cost absorption challenges.  \n- **Regulatory Uncertainty:** Delays in FSD (Supervised) approvals in Europe and China limit near-term monetization.  \n- **Macro Risks:** Trade policy shifts and political sentiment threaten supply chains and demand for durable goods.  \n\n---\n\n## 4. Investment Recommendation  \n\n### **Recommendation:** **Hold**  \n\n### **Rationale:**  \n- **High-Risk Tolerance Suitability:** Tesla’s transition into AI/robotics and autonomy introduces significant execution risks (e.g., regulatory approvals, scalability of Robotaxi).  \n- **Mixed Financial Performance:** While Energy/Services segments show growth (+17% YoY), automotive revenue declines (-16% YoY) and compressed margins (4.1% operating margin) raise near-term concerns.  \n- **Long-Term Potential:** Leadership in autonomy, energy storage, and affordable EV models positions Tesla for future growth, but current valuation (~$36.8B cash reserves) already reflects optimism.  \n\n**Key Risks:** Regulatory delays for autonomy, macroeconomic volatility, and competition in affordable EV segments (e.g., Chinese OEMs).  \n\n--- \n\n**Final Note:** Monitor progress on Robotaxi scalability, FSD regulatory approvals, and margin recovery in H2 2025.",
          "investment_advising": "The provided analysis suggests a \"Hold\" recommendation for Tesla stock, and I largely agree with that assessment, but with some important caveats.\n\n**Reasons to agree with the \"Hold\":**\n\n* **Mixed Financial Performance:**  The significant year-over-year decline in automotive revenue (-16%) and net income (-16%) is a major concern. While the energy and services segments show growth, they aren't large enough to offset the weakness in the core automotive business.  The plummeting free cash flow (-89%) is particularly alarming.\n* **Execution Risks:** The \"Growth Areas\" highlight ambitious projects (robotaxis, affordable models, expanded energy storage).  Success is far from guaranteed, and significant execution risks exist. Regulatory hurdles for autonomous driving are a major uncertainty.\n* **Valuation:** The analysis mentions a significant cash reserve, but the current valuation likely already incorporates considerable optimism about the future.  This leaves less room for upside and increases the risk of a significant price drop if the company fails to meet expectations.\n* **Macroeconomic Risks:** The global economic climate introduces substantial uncertainty.  A downturn could severely impact demand for high-priced vehicles like Tesla's.\n\n**Reasons for Cautious Optimism (and potential adjustments to the \"Hold\"):**\n\n* **Long-Term Potential:** Tesla's leadership in EVs and energy storage, coupled with its advancements in AI and autonomous driving, does offer substantial long-term potential.  The expansion into new markets (India) and the development of more affordable models could drive future growth.\n* **Energy and Services Growth:** The positive growth in the Energy & Storage and Services & Other segments demonstrates diversification and the potential for these areas to become increasingly important revenue streams.\n* **Low Debt-to-Equity Ratio:**  The relatively low debt-to-equity ratio suggests a healthy financial foundation, providing some cushion against potential setbacks.\n\n**Recommendation Refinement:**\n\nInstead of a simple \"Hold,\" I'd recommend a **\"Hold with a watchful eye\"**.  Investors should closely monitor the following:\n\n* **H2 2025 Performance:**  The final note correctly emphasizes the importance of monitoring progress in the second half of 2025.  Strong performance in these areas would justify a more positive outlook.\n* **Robotaxi Scalability:**  The success of the robotaxi service is crucial.  Positive developments here could significantly boost the stock price.\n* **FSD Regulatory Approvals:**  Securing approvals in key markets (Europe, China) is critical for unlocking the potential revenue from autonomous driving features.\n* **Margin Recovery:**  Improving automotive margins is essential for long-term profitability.\n\n\nIn conclusion, while Tesla's long-term prospects remain intriguing, the current financial performance and execution risks warrant a cautious approach.  A \"Hold with a watchful eye\" strategy allows investors to stay invested while actively monitoring key performance indicators and adjusting their position based on future developments.  The current situation isn't necessarily bearish, but neither does it present compelling reasons for adding to a position at this time.\n",
          "risk_assessment": "\n\n# Tesla Q2 2025 Risk Assessment Report  \n\n---\n\n## **1. Key Risks Identified**  \n\n### **Market Risks**  \n- Declining automotive revenue (-16% YoY) due to lower vehicle deliveries and reduced ASPs.  \n- Reduced regulatory credit revenue.  \n- Geopolitical risks from shifting tariffs and trade policies (e.g., entry into India, China/EU regulatory approvals).  \n\n### **Operational Risks**  \n- Production scalability challenges for new models (e.g., Cybercab, Semi) and affordable vehicle ramp-up.  \n- Dependence on AI/autonomy development timelines (Robotaxi expansion, FSD regulatory approvals).  \n- Inventory management inefficiencies (33% YoY increase in global vehicle inventory days).  \n\n### **Financial Risks**  \n- Declining free cash flow (-89% YoY to $0.1B).  \n- Reduced operating margin (-219 bps YoY to 4.1%).  \n- Currency exchange volatility impacting international revenue.  \n\n### **Regulatory Risks**  \n- Uncertain impacts of fiscal policy changes and political sentiment.  \n- Delays in FSD/autonomy approvals in Europe and China.  \n- Compliance risks with evolving crypto/digital asset accounting standards.  \n\n### **Technological Risks**  \n- Execution risks in AI training compute expansion (67k H100 equivalents).  \n- Battery material supply chain bottlenecks (lithium refining, LFP cell production).  \n\n---\n\n## **2. Risk Categorization**  \n\n| **Category**       | **Risks**                                                                 |  \n|---------------------|---------------------------------------------------------------------------|  \n| **Market**          | Declining deliveries, ASP pressure, tariff volatility                    |  \n| **Operational**     | Production scalability, inventory management, autonomy delays            |  \n| **Financial**       | Cash flow erosion, margin compression, currency risks                    |  \n| **Regulatory**      | Policy uncertainty, FSD approval delays, crypto accounting changes       |  \n| **Technological**   | AI compute scaling, battery material bottlenecks                         |  \n\n---\n\n## **3. Severity and Impact Assessment**  \n\n| **Risk**                               | **Severity** | **Potential Impact**                                                                 |  \n|----------------------------------------|--------------|-------------------------------------------------------------------------------------|  \n| Declining automotive revenue           | High         | Threatens core business sustainability; $16.7B automotive revenue (-16% YoY).       |  \n| Free cash flow erosion                 | High         | Limits R&D/AI investment capacity; $0.1B free cash flow vs. $2.5B operating cash flow.|  \n| Production scalability challenges      | High         | Delays in Cybercab/Semi production could derail 2026 growth targets.                |  \n| FSD regulatory delays                  | Medium       | Limits Robotaxi expansion and FSD monetization in key markets (EU/China).           |  \n| Battery material bottlenecks           | Medium       | Risks energy storage growth (9.6 GWh deployed, -7% YoY revenue).                    |  \n\n---\n\n## **4. Mitigation Strategies for High-Severity Risks**  \n\n### **Declining Automotive Revenue**  \n- **Mitigation:** Accelerate affordable model production (target: H2 2025) and expand into emerging markets (e.g., India).  \n- **Action:** Leverage Gigafactory Shanghai as an export hub to offset tariff impacts.  \n\n### **Free Cash Flow Erosion**  \n- **Mitigation:** Prioritize capex efficiency ($2.4B Q2 capex) and optimize working capital (reduce inventory days from 24).  \n- **Action:** Monetize Supercharger network growth (+14% stations YoY) through partnerships.  \n\n### **Production Scalability Challenges**  \n- **Mitigation:** Implement “unboxed” manufacturing for Cybercab and replicate Berlin/Texas factory tooling.  \n- **Action:** Pre-order agreements for Semi to secure demand ahead of 2026 production.  \n\n---\n\n## **5. Quantitative Analysis**  \n\n| **Risk**                               | **Estimated Financial Impact**                                  |  \n|----------------------------------------|-----------------------------------------------------------------|  \n| Declining automotive revenue           | $3.2B YoY revenue loss (16% of $19.8B Q2 2024 automotive revenue). |  \n| Free cash flow erosion                 | $1.3B annualized cash flow gap (vs. $6.8B TTM free cash flow).   |  \n| FSD regulatory delays                  | $500M–$1B lost Robotaxi revenue opportunity in 2026.             |  \n| Battery material bottlenecks           | $200M–$400M energy storage revenue risk (10–20% of $2.8B segment revenue). |  \n\n---\n\n## **6. Conclusion**  \nTesla faces significant risks from declining automotive revenue and cash flow compression, exacerbated by macroeconomic and regulatory uncertainties. High-severity risks require immediate action to stabilize core operations, while medium risks (e.g., FSD approvals, battery supply) demand strategic partnerships and regulatory engagement. Proactive cost management and accelerated AI/autonomy commercialization are critical to offsetting near-term pressures."
      },
      "file_processed": "TSLA-Q2-2025-Update.pdf"
  }
  ```

---

### `GET /history`
- **Description**: Fetches the analysis history for the authenticated user.
- **Authentication**: `Bearer <token>` in the request header.
- **Response (200)**: A JSON array where each object represents a past analysis.
