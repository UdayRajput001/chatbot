from langchain_ollama import ChatOllama

# Initialize the Ollama model
model = ChatOllama(
    model='llama3.2:1b',   # Replace with the desired model
    base_url='http://localhost:11434/'  # URL of the Ollama server
)

def generate_response(text: str) -> str:
    """Generate a response using the Ollama model"""
    try:
        response = model.invoke(text)
        return response.content
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")
