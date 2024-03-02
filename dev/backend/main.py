from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Server": "Open"}

@app.get("/api/titles")
def get_titles():
    return {"Title": "OK"}

@app.get("/api/messages")
def get_messages(title):
    return {}

@app.post("/api/setting")
def post_setting():
    return {"Setting": "Applied"}

@app.post("/api/input")
def post_input(input):
    return {"Input": "Sended"}