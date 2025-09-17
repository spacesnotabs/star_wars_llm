from llm_service import LLMService
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    # Initialize the LLM service
    llm_service = LLMService()

    # Load environment variables
    load_dotenv()

    api_key = os.getenv('GEMINI_API_KEY')
    llm_service.initialize_model(model_name='gemini-2.5-flash',
                                 api_key=api_key)
    
    while True:
        user_prompt = input('User: ').strip()

        if user_prompt.lower() in ['quit', 'exit']:
            break

        response = llm_service.chat_message(message=user_prompt)
        print(f'AI: {response}')

