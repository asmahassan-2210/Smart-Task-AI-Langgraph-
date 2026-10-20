import os
from dotenv import load_dotenv
from graph import build_graph

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Build the compiled workflow graph
    app = build_graph()

    # Sample user input
    user_message = "I need to finish my assignment tomorrow, buy groceries today, and prepare for my meeting next week."
    
    initial_state = {
        "user_input": user_message,
        "extracted_tasks": [],
        "prioritized_tasks": [],
        "final_output": ""
    }

    print(f"Processing input: '{user_message}'\n" + "-" * 50 + "\n")
    
    # Run the workflow
    final_state = app.invoke(initial_state)
    
    print(final_state["final_output"])