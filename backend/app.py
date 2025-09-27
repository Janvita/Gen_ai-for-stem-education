from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import detect, llm,auth, regions_detect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect.router, prefix="/detect", tags=["Detection"])
app.include_router(llm.router, prefix="/llm", tags=["LLM"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(regions_detect.router, prefix="/detect", tags=["Region Detection"])