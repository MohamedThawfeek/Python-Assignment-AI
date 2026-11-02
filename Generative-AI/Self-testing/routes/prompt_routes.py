from fastapi import APIRouter, status
from validation.prompt import UserPrompt

from controller.ai_response import (gpt_response, gemini_response, ollama_response )

router = APIRouter()


@router.post("/ask-gpt",status_code=status.HTTP_200_OK)
def ask_gpt(prompt:UserPrompt):
    return gpt_response(prompt)

@router.post("/ask-gemini",status_code=status.HTTP_200_OK)
def ask_ai_gemini(prompt:UserPrompt):
    return gemini_response(prompt)

@router.post("/ask-ollama",status_code=status.HTTP_200_OK)
def ask_ai_ollama(prompt:UserPrompt):
    return ollama_response(prompt)
    