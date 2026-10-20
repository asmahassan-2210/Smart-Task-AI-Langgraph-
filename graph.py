from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END
from tools import extract_tasks_tool, prioritize_tasks_tool


class TaskState(TypedDict, total=False):
    user_input: str
    extracted_tasks: List[dict]
    prioritized_tasks: List[dict]
    final_output: str


def extract_tasks_node(state: TaskState):
    extracted = extract_tasks_tool.invoke({"user_input": state["user_input"]})
    return {"extracted_tasks": extracted}


def prioritize_tasks_node(state: TaskState):
    prioritized = prioritize_tasks_tool.invoke({"tasks": state["extracted_tasks"]})
    return {"prioritized_tasks": prioritized}


def format_results_node(state: TaskState):
    tasks = state["prioritized_tasks"]
    
    grouped = {"High": [], "Medium": [], "Low": []}
    for t in tasks:
        grouped[t["priority"]].append(f"- **{t['task']}** (Due: {t['due_hint']})")
        
    output = "## 📋 Organized Task List\n\n"
    for priority in ["High", "Medium", "Low"]:
        if grouped[priority]:
            output += f"### {priority} Priority\n"
            output += "\n".join(grouped[priority]) + "\n\n"
            
    return {"final_output": output.strip()}


def build_graph(checkpointer=None):
    builder = StateGraph(TaskState)
    
    # Add Nodes
    builder.add_node("extract_tasks", extract_tasks_node)
    builder.add_node("prioritize_tasks", prioritize_tasks_node)
    builder.add_node("format_results", format_results_node)
    
    # Define Edges
    builder.add_edge(START, "extract_tasks")
    builder.add_edge("extract_tasks", "prioritize_tasks")
    builder.add_edge("prioritize_tasks", "format_results")
    builder.add_edge("format_results", END)
    
    return builder.compile(checkpointer=checkpointer)