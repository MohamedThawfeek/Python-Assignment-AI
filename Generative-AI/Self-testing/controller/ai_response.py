from fastapi import HTTPException
from validation.prompt import UserPrompt

# AI Models
from openai import OpenAI
from google import genai
# pyrefly: ignore[missing-import]
from ollama import Client
from dotenv import load_dotenv
import os

load_dotenv()

gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Gemini client
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Ollama Cloud client
ollama_client = Client(host="https://ollama.com",headers={"Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"})

messages= [{"role": "system", "content": "you are a financial experts that specializes in real estate invertement and negotiation"}]

def gpt_response(user_prompt: UserPrompt):
    try:
        messages.append({"role": "user", "content":user_prompt.prompt})

        response = gpt_client.chat.completions.create(
            model = "gpt-4o-mini",
            messages =messages
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def gemini_response(user_prompt: UserPrompt):
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt.prompt
        )

        reply = response.text
        return reply

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def ollama_response(user_prompt: UserPrompt):
    try:
        response = ollama_client.chat(
            model="gpt-oss:120b",
            messages=[{"role": "user","content": user_prompt.prompt}]
        )
        reply = response.message.content
        return reply
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))