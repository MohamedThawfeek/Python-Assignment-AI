from pydantic import BaseModel, Field, EmailStr



class UserPrompt(BaseModel):
    prompt: str