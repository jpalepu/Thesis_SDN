from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_openai():
    try:
        # Initialize ChatOpenAI with recommended configuration
        chat = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0
        )
        
        # Simple test message
        messages = [
            HumanMessage(content="Write a simple Python hello world program")
        ]
        
        # Get response
        response = chat.invoke(messages)
        print("Response from OpenAI:")
        print(response.content)
        
    except Exception as e:
        print(f"Error: {str(e)}")

def test_anthropic():
    try:
        # Initialize ChatAnthropic
        chat = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            temperature=0,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        # Simple test message
        messages = [
            HumanMessage(content="Write a simple Python hello world program")
        ]
        
        # Get response
        response = chat.invoke(messages)
        print("\nResponse from Anthropic:")
        print(response.content)
        
    except Exception as e:
        print(f"Error with Anthropic: {str(e)}")

if __name__ == "__main__":
    print("Testing OpenAI...")
    test_openai()
    
    print("\nTesting Anthropic...")
    test_anthropic() 