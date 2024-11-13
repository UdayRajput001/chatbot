from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama
import pymongo
from pydantic import BaseModel

# FastAPI instance
app = FastAPI()

# Enable CORS for all origins (you can specify your allowed domains here)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Adjust to your needs for security.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# MongoDB configuration
MONGO_URI = "mongodb+srv://udsingh468:Qwerty467@cluster0.5d2yg.mongodb.net/"
client = pymongo.MongoClient(MONGO_URI)
db = client["Ollama"]
collection = db["data"]

# Model to handle user input
class ChatMessage(BaseModel):
    user_message: str  # Only expect user message

# Initialize Ollama model
def generate_response(text: str):
    try:
        model = ChatOllama(
            model='llama3.2:1b',
            base_url='http://localhost:11434/'
        )
        response = model.invoke(text)
        # print("Model Response:", response.content)  # Debugging line
        return response.content
    except Exception as e:
        print(f"Error in model invocation: {e}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Error generating response: {e}")


# Function to store chat history in MongoDB
def store_chat_history(data: dict):
    collection.insert_one(data)


@app.post("/chat/")
async def chat_message(chat: ChatMessage):
    try:
        # Generate response using Ollama model
        response = generate_response(chat.user_message)

        # Store chat history in MongoDB (optional)
        chat_data = {
            "user_message": chat.user_message,
            "bot_response": response,
        }
        store_chat_history(chat_data)

        return {"user_message": chat.user_message, "bot_response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


# Endpoint to fetch chat history
@app.get("/history/")
async def get_chat_history():
    try:
        # Retrieve chat history from MongoDB
        chats = collection.find()
        chat_history = [
            {"user_message": chat["user_message"], "bot_response": chat["bot_response"]}
            for chat in chats
        ]
        return chat_history

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {e}")

