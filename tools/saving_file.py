import datetime
from planner_state import PlannerState
from langchain_ollama import ChatOllama
def format_to_file(content: str) -> None:
    llm = ChatOllama(model="llama3.2:3b")
    prompt = f"""
            The below is the content provided, I need to format it into a markdown format file.
            {content}
            Analyze the content and frame the output properly.
            Just return the markdown output, nothing else.
            OUTPUT SHOULD BE IN MARKDOWN FORMAT.

            example:
            # Heading (Can be either Weather data or Flights / Hotels Search based on the content)
            ## Place1: 
             - details
            ## Place2:
             - details

            other details.....
        """
    try:
        result = llm.invoke(prompt)
        content = result.content.strip()
        print(content)
        return content
    except Exception as e:
        print("errorrrr: ", e)


import os

def save_to_file(content: str, filename: str, agent_name: str) -> None:
    output_dir = "output"

    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Combine directory and filename
    filepath = os.path.join(output_dir, filename)

    # Write to file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Data saved by agent '{agent_name}' to: {filepath}")
