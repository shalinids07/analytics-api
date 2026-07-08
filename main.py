from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

EMAIL = "23f1000746@ds.study.iitm.ac.in"
API_KEY = "ak_7ov4f0mdahngash01l6jtnoh"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class RequestData(BaseModel):
    events: list[Event]

@app.post("/analytics")
def analytics(
    data: RequestData,
    x_api_key: str = Header(None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total_events = len(data.events)
    unique_users = len(set(e.user for e in data.events))
    revenue = sum(e.amount for e in data.events if e.amount > 0)

    totals = {}
    for e in data.events:
        if e.amount > 0:
            totals[e.user] = totals.get(e.user, 0) + e.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }
