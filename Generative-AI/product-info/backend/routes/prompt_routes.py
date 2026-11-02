from fastapi import APIRouter, status
from validation.prompt import UserPrompt

from controller.ai_response import (ollama_response )

router = APIRouter()

@router.post("/ask-ollama",status_code=status.HTTP_200_OK)
def ask_ai_ollama(prompt:UserPrompt):
    return ollama_response(prompt)
    