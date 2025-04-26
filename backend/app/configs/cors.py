from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def add_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",  # React dev server
            "http://localhost:8173", # BE
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )