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

from formats import Input, Setting, Option

@app.get("/api/messages")
def get_messages(title: str):
    print(title)

    # load messages and send to client

    return {"Title": title, "Messages": ["message 1", "message 2", "message 3"]}

@app.post("/api/setting")
def post_setting(setting: Setting):
    setting_dict = setting.dict()
    print(setting_dict)

    # Send setting to lc_package
    
    return {"Setting": setting_dict, "Titles": ["Chat 1", "Chat 2", "Chat 3"]}

@app.post("/api/option")
def post_input(option: Option):
    option_dict = option.dict()
    print(option_dict)

    # Send option to lc_package

    return {"Option": option_dict}

@app.post("/api/input")
def post_input(input: Input):
    input_dict = input.dict()
    print(input_dict)

    # Send and receive message

    return {"Input": input_dict["text"], "Output": "<<Sample>>"}