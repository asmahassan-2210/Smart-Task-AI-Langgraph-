# Smart Task AI Assistant

An intelligent multi-node workflow built with **LangGraph** and **Google Gemini** that takes unstructured, natural-language task descriptions, extracts individual action items, assigns priorities based on due dates, and outputs a clean, categorized task list.

## Project Structure

```text
Smart Task AI/
│
├── tools.py          # Pydantic schemas and LangChain tools for extraction & prioritization
├── graph.py          # LangGraph state definition, node logic, and compiled workflow graph
├── main.py           # Entry point to execute the workflow
├── requirements.txt  # Project dependencies
├── .env              # API keys and environment variables (ignored in Git)
└── .gitignore        # Files to ignore in version control

Setup & Installation
1. Clone the repository or navigate to your project directory.

2. Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. Install dependencies:

Bash
pip install -r requirements.txt

4. Set up your environment variables:
Create a .env file in the root directory and add your Google Gemini API key
GOOGLE_API_KEY=your_gemini_api_key_here

Author: ASMA HASSAN