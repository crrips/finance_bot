from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

from models.expense import Expense
from database import engine, Base
from endpoints import get_router
from models.user import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_router())
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

