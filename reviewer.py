import argparse
import sys
import os
from groq import Groq
from rich.console import Console
from rich.markdown import Markdown

def get_cli_arguments():
    # Setup argparse to take the filename from the terminal
    parser = argparse.ArgumentParser(description="Intelligent AI Code Reviewer & Explainer")
    parser.add_argument("file", help="The path to the code file you want to review")
    return parser.parse_args()

def safely_read_file(file_path):
    # Input & Payload Capture (Safely reading the file)
    print(f"Attempting to ingest file: {file_path}...")
    try:
        # Open the file in read mode ('r') with standard text encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("File successfully loaded into memory.\n")
            return content
            
    # If the user gives a wrong file name or path
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1) # Exit the program safely
        
    # If the user does not have permission to open the file
    except PermissionError:
        print(f"Error: You do not have permission to read '{file_path}'.")
        sys.exit(1)
        
    # If the file is an image or binary file instead of text
    except UnicodeDecodeError:
        print(f"Error: '{file_path}' appears to be a binary file. Only text files are supported.")
        sys.exit(1)

def analyze_code_with_ai(raw_code):
    # Context Orchestration & The LLM Taming Matrix
    # Get the API key from the environment variable
    api_key = os.environ.get("GROQ_API_KEY")
    
    # Check if the API key exists
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not found.")
        print("Please set your API key using: export GROQ_API_KEY='your_key_here' (Mac/Linux) or $env:GROQ_API_KEY='your_key_here' (Windows PowerShell)")
        sys.exit(1)

    # Initialize the Groq client
    client = Groq(api_key=api_key)
    
    print("Connecting to the AI Gatekeeper... Please wait.\n")
    
    # Strict System Prompt to force the AI to behave exactly as required by the PDF
    system_prompt = """
    You are a cold, analytical Senior Code Quality Assurance Engineer.
    You only output valid code blocks and direct bullet points.
    Do not write friendly greetings.
    
    You MUST format your entire response exactly like this:
    
    ## BUG_REPORT
    - [Bullet point 1 detailing a bug]
    - [Bullet point 2 detailing a bug]
    
    ## REFACTORED_CODE
    ```python
    [Your fixed and optimized code here]
    ```
    
    If there are no bugs, still use the ## BUG_REPORT section to state that the code looks good.
    Do NOT add any other text outside these two sections.
    """
    
    try:
        # Call the Groq API using the latest supported model
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Review this code:\n\n{raw_code}"}
            ],
            model="llama-3.1-8b-instant", # Updated model name to avoid decommission error
            temperature=0.1 # Low temperature for more analytical and less creative output
        )
        
        # Return the AI's response
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"An error occurred while communicating with the AI: {e}")
        sys.exit(1)

def validate_and_render_output(ai_response):
    # Output Validation and Rich Rendering
    console = Console()
    
    # Validation Check: Ensure AI gave us the exact headings we asked for
    if "## BUG_REPORT" not in ai_response or "## REFACTORED_CODE" not in ai_response:
        console.print("[bold red]Validation Error:[/bold red] The AI Gatekeeper returned a malformed report.")
        sys.exit(1)
        
    # Convert the raw text into a beautiful Markdown format using Rich
    markdown_output = Markdown(ai_response)
    
    # Print it to the terminal with nice visual separators
    console.rule("[bold blue]AI GATEKEEPER REPORT[/bold blue]")
    console.print(markdown_output)
    console.rule("[bold blue]END OF REPORT[/bold blue]")

def main():
    # Get the file path from the user's command
    args = get_cli_arguments()
    
    # Read the raw code into a string variable
    raw_code = safely_read_file(args.file)
    
    # Send the raw code to the AI for analysis
    ai_response = analyze_code_with_ai(raw_code)
    
    # Validate the AI response and print it beautifully to the terminal
    validate_and_render_output(ai_response)

if __name__ == "__main__":
    main()