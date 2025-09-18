# Financial Document Analyzer

A full-stack AI application that analyzes financial documents using a team of specialized agents. Users can register, upload a PDF report, and receive a comprehensive analysis covering financial health, investment advice, and risk assessment. All analyses are saved to a user-specific history.

**Live Demo**: `[Link to be added]`

## Technology Stack

- **Backend**: FastAPI
- **Database**: MongoDB
- **AI Agents**:
  - **Primary LLM**: Google's `Gemini 1.5 Flash`
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
git clone https://github.com/your-username/financial-document-analyzer-debug.git
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

---

### `GET /history`
- **Description**: Fetches the analysis history for the authenticated user.
- **Authentication**: `Bearer <token>` in the request header.
- **Response (200)**: A JSON array where each object represents a past analysis.
