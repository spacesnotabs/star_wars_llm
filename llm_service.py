import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

class LLMService:
    def __init__(self):
        self.model_name: str | None = None
        self.api_key: str | None = None
        self._model = None
        self.chat = None
        self.previous_challenges: list[str] = []  # Track previous challenge titles/descriptions
        
    @property
    def model(self):
        """Lazily initialize and return the model"""
        if not self._model and self.api_key:
            self._model = genai.GenerativeModel(model_name=self.model_name)
        return self._model
    
    def initialize_model(self, model_name: str, api_key: str | None=None):
        """Initialize the model with the provided API key and model name"""
        if api_key:
            self.api_key = api_key
            genai.configure(api_key=self.api_key)
        else:
            return "API key not configured."
        
        if model_name:
            self.model_name = model_name
        else:
            return "Model name not provided."
        
        try:
            self._model = genai.GenerativeModel(model_name=self.model_name)
            return "Model initialized successfully."
        except Exception as e:
            print(f"Error initializing model: {e}")
            return f"Error initializing model. Please check your API key and model name. Error details: {str(e)}"
            
    def start_new_chat(self, history=None):
        """Start a new chat session with the model"""
        try:
            self.chat = self.model.start_chat(history=history)
            return "New chat session started successfully."
        except Exception as e:
            print(f"Error starting chat session: {e}")
            return f"Error starting chat session. Error details: {str(e)}"
    
    def chat_message(self, message: str):
        """Send a message to the active chat session and get a response"""
        if not self.chat:
            self.start_new_chat()
        
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            print(f"Error in chat conversation: {e}")
            return f"Error in chat conversation. Please try again later. Error details: {str(e)}"
