from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.admins import router as admins_router
from routers.eventos import router as eventos_router
from routers.logs import router as logs_router
from services.weather import router as clima_router
from services.chat import router as chat_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://igorvictor23.github.io",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(admins_router)
app.include_router(eventos_router)
app.include_router(logs_router)
app.include_router(clima_router)
app.include_router(chat_router)
