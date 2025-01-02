from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.callbacks import get_openai_callback
import difflib
import os
from dotenv import load_dotenv
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# Define the system prompt
SYSTEM_PROMPT = """You are a Trained Network Automation Engine Expert. Do not provide any text/summary before or after response. Only Provide code for mininet with ryu controller setup using Langchain. Not Ryu application and Provide code and debug issues related to all network engineering tasks. Do not provide any text/description only provide code."""

# Define the user prompt
USER_PROMPT = """create a program to 10 hosts and 5 switches and 2 controllers for tree topology"""

# Create prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", USER_PROMPT)
])

# Initialize LLMs with specific configurations
llms = {
    "gpt-4": ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4",
        temperature=0
    ),
    "gpt-3.5": ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
        temperature=0
    ),
    "claude": ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-sonnet-20240229",
        temperature=0
    )
}

# Create output directory
output_dir = Path("llm_generated_code")
output_dir.mkdir(exist_ok=True)

def get_code_from_llm(llm, prompt):
    """Get code from LLM and save to file"""
    response = prompt_template.invoke({"messages": []}).content
    return response

def save_code_to_file(code, filename):
    """Save generated code to file"""
    with open(output_dir / filename, 'w') as f:
        f.write(code)

def calculate_similarity(code1, code2):
    """Calculate similarity between two code snippets"""
    similarity = difflib.SequenceMatcher(None, code1, code2).ratio()
    return similarity * 100

def analyze_code(code):
    """Basic code analysis for potential issues"""
    issues = []
    
    # Check for common issues
    if "sudo mn" in code and not "from mininet.cli import CLI" in code:
        issues.append("Missing Mininet CLI import")
    
    if "Ryu" in code and not "from mininet.node import RemoteController" in code:
        issues.append("Missing RemoteController import")
        
    if "net.addController" in code and not "RemoteController" in code:
        issues.append("Controller setup might be incorrect")
        
    return issues

def main():
    generated_codes = {}
    
    # Generate code from each LLM
    for llm_name, llm in llms.items():
        print(f"Generating code using {llm_name}...")
        
        try:
            with get_openai_callback() as cb:
                code = get_code_from_llm(llm, prompt_template)
                generated_codes[llm_name] = code
                
                # Save to file
                filename = f"sdn_code_{llm_name}.py"
                save_code_to_file(code, filename)
                
                print(f"Code saved to {filename}")
                print(f"Tokens used: {cb.total_tokens}")
                
        except Exception as e:
            print(f"Error with {llm_name}: {str(e)}")
    
    # Calculate similarities
    similarities = {}
    for llm1 in generated_codes:
        for llm2 in generated_codes:
            if llm1 < llm2:
                sim = calculate_similarity(generated_codes[llm1], generated_codes[llm2])
                similarities[f"{llm1} vs {llm2}"] = f"{sim:.2f}%"
    
    # Analyze potential issues
    issues = {}
    for llm_name, code in generated_codes.items():
        issues[llm_name] = analyze_code(code)
    
    # Save analysis results
    analysis = {
        "similarities": similarities,
        "potential_issues": issues
    }
    
    with open(output_dir / "analysis_results.json", 'w') as f:
        json.dump(analysis, f, indent=4)
    
    # Print results
    print("\nSimilarity Analysis:")
    for comparison, similarity in similarities.items():
        print(f"{comparison}: {similarity}")
    
    print("\nPotential Issues:")
    for llm_name, llm_issues in issues.items():
        print(f"\n{llm_name}:")
        if llm_issues:
            for issue in llm_issues:
                print(f"- {issue}")
        else:
            print("No major issues detected")

if __name__ == "__main__":
    main() 