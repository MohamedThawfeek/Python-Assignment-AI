from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.prompt_routes import router as prompt_router


app = FastAPI(
    title="Chat conversation",
    description="Python FastAPI Backend",
    version="1.0.0"

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    prompt_router,
    prefix="/api/v1",
    tags=["prompt"]
)

@app.get("/")
def root():
    return{
        "success": True,
        "message": "FastAPI server is running"
    }

@app.get("/health")
def health_check():
    return{
        "status": "OK"
    }