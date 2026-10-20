from langchain_core.tools import tool
from typing import List, Literal
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini model with an active model name
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)

# Pydantic Schemas for Structured Outputs
class TaskItem(BaseModel):
    task: str = Field(description="The actionable task description")
    due_hint: str = Field(description="Timeframe mentioned, e.g., 'today', 'tomorrow', 'next week'")

class TaskListResponse(BaseModel):
    tasks: List[TaskItem]

class PrioritizedTaskItem(BaseModel):
    task: str = Field(description="The actionable task description")
    due_hint: str = Field(description="Timeframe mentioned")
    priority: Literal["High", "Medium", "Low"] = Field(description="Priority level based on urgency")

class PrioritizedTaskListResponse(BaseModel):
    tasks: List[PrioritizedTaskItem]

@tool
def extract_tasks_tool(user_input: str) -> List[dict]:
    """Extract all individual tasks and their due date/time hints from unstructured text."""
    prompt = f"""
    Extract all individual tasks and their due date/time hints from the following text:
    "{user_input}"
    """
    structured_llm = llm.with_structured_output(TaskListResponse)
    result = structured_llm.invoke(prompt)
    return [{"task": t.task, "due_hint": t.due_hint} for t in result.tasks]

@tool
def prioritize_tasks_tool(tasks: List[dict]) -> List[dict]:
    """Assign a priority level (High, Medium, or Low) to each task based on urgency and timeframe hints."""
    tasks_input = "\n".join([f"- {t['task']} (Due: {t['due_hint']})" for t in tasks])
    prompt = f"""
    Assign a priority level (High, Medium, or Low) to each of the following tasks based on urgency and timeframe hints:
    {tasks_input}
    
    Criteria:
    - High: Due today, immediately, or urgent.
    - Medium: Due tomorrow or within a few days.
    - Low: Due next week or later / flexible.
    """
    structured_llm = llm.with_structured_output(PrioritizedTaskListResponse)
    result = structured_llm.invoke(prompt)
    return [{"task": t.task, "due_hint": t.due_hint, "priority": t.priority} for t in result.tasks]