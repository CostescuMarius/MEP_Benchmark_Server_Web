from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class NumePayload(BaseModel):
    nume: str

@app.get("/salut")
def salut():
    return {"mesaj": "Salut!"}

@app.post("/salut")
def salut_post(payload: NumePayload):
    return {"mesaj": f"Salut, {payload.nume}!"}
