### **Intelligent Code Reviewer \& Explainer**



This project is part of the DecodeLabs Internship (Project 4 - Optional Mastery Phase). It is an automated developer utility tool that ingests raw code files, acts as an AI gatekeeper to identify bugs, and renders optimized, syntax-highlighted code directly in the terminal.



### **Key Features**



Safe File Ingestion: Uses robust try-except blocks to handle file reading errors gracefully (e.g., FileNotFoundError, PermissionError, binary file detection).



Strict AI Persona (The LLM Taming Matrix): Enforces strict system instructions using the Groq API (llama-3.1-8b-instant model) to output only a distinct bug report and refactored code without conversational filler.



Output Validation: Automatically rejects malformed AI responses if the required ## BUG\_REPORT and ## REFACTORED\_CODE headings are missing.



Rich Terminal Rendering: Utilizes the Python rich library to convert standard markdown into color-coded, IDE-quality syntax highlighting directly within the console.



### **Technologies Used**



Python 3.x



Groq API (LLM Orchestration)



Rich (Terminal Output Formatting)



Argparse (CLI Interface)



#### **How to Run**



Clone this repository to your local machine.



Install the required dependencies:



pip install groq rich





Set your Groq API key in your terminal environment:



Windows (PowerShell): $env:GROQ\_API\_KEY="your\_api\_key\_here"



Mac/Linux: export GROQ\_API\_KEY="your\_api\_key\_here"



Run the code reviewer on any target file:



**python reviewer.py buggy\_script.py**

