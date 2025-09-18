# Financial Document Analyzer

This project is a FastAPI application that uses a team of AI agents to analyze financial documents. You can upload a PDF of a financial report, and the AI agents will provide a detailed analysis, investment advice, and a risk assessment.

## Bugs Found and Fixes

During the development of this project, several bugs were encountered and fixed. Here is a summary of the issues and their resolutions:

### 1. `NameError: name 'tool' is not defined`

*   **Bug:** The `@tool` decorator was used in `tools.py` without being imported.
*   **Fix:** The `tool` decorator was imported from `crewai.tools` by changing the import statement from `from crewai.tools import BaseTool` to `from crewai.tools import BaseTool, tool`.

### 2. `'function' object has no attribute 'get'`

*   **Bug:** This error was caused by a misconfiguration in how the `crewai` agents were being used. The `kickoff` method of the `Crew` class was not receiving the `file_path` of the document to be analyzed.
*   **Fix:** The `main.py` file was updated to pass the `file_path` to the `kickoff` method. The agent goals and task descriptions in `agents.py` and `task.py` were also updated to include the `{file_path}` placeholder, ensuring the agents were aware of the file they needed to process.

### 3. `'function' object has no attribute 'agent'`

*   **Bug:** After refactoring the project to use a custom `Crew` class, this error occurred because the `CustomCrew` was receiving a function instead of a `CustomTask` object.
*   **Fix:** This was a complex issue that required a major refactoring of the project. The `crewai.Crew` and `crewai.Task` classes were replaced with custom `CustomCrew` and `CustomTask` classes to provide more control over the agent and task execution flow.

### 4. `'Tool' object is not callable`

*   **Bug:** This error occurred because the code was attempting to call a `crewai` `Tool` object as a function.
*   **Fix:** The `agents.py` file was modified to call the `run` method of the tool object (e.g., `analyze_investment.run(document_text)`) instead of calling the object directly.

### 5. Inefficient Prompts

*   **Bug:** The prompts used to generate the financial analysis and risk assessment were too generic, leading to suboptimal results.
*   **Fix:** The prompts in `tools.py` were significantly improved to be more specific and structured. They now request specific metrics, a structured output format, and provide more context to the LLM, resulting in higher quality analysis.

## Setup and Usage

### Prerequisites

*   Python 3.8+
*   An NVIDIA API key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/likhith1409/financial-document-analyzer-debug.git
    cd financial-document-analyzer-debug
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up the environment variables:**
    *   Create a `.env` file in the root of the project.
    *   Add your NVIDIA API key to the `.env` file:
        ```
        NVIDIA_API_KEY="your_api_key_here"
        ```

### Running the Application

To run the application, you only need to start the FastAPI server, which now includes the Gradio UI.

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The Gradio web interface will be available at `http://localhost:8000/gradio`.

## API Documentation

### `/analyze`

This endpoint analyzes a financial document and provides a comprehensive report.

*   **Method:** `POST`
*   **Content-Type:** `multipart/form-data`

#### Request

| Parameter | Type   | Description                                         |
| :-------- | :----- | :-------------------------------------------------- |
| `file`    | `file` | The financial document to be analyzed (PDF format). |
| `query`   | `str`  | (Optional) A specific query for the analysis.       |

#### Response

A successful response will return a JSON object with the following structure:

```json
{
  "status": "success",
  "query": "Analyze this financial document for investment insights",
  "analysis": "[...]",
  "file_processed": "your_document.pdf"
}
```

*   `status`: The status of the request.
*   `query`: The query used for the analysis.
*   `analysis`: A string containing the detailed analysis from the AI agents.
*   `file_processed`: The name of the file that was processed.
