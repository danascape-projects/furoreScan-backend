from fastapi import FastAPI, Depends, HTTPException, Form, Query
from fastapi.responses import JSONResponse
import json

app = FastAPI()

valid_username = "user123"
valid_password = "password123"

attendees = {
    "123": {"name": "John Doe", "day1": False, "day2": False},
    "23": {"name": "John Doe", "day2": False, "day2": False},
    # Add more attendees
}

try:
    with open("attendees.json", "r") as file:
        attendees = json.load(file)
except FileNotFoundError:
    attendees = {}

@app.get("/")
def read_hello():
    content = {"message": "Hello, World!"}
    return JSONResponse(content=content)

@app.post("/login/")
async def login(
    username: str = Query(None, title="User Name"),
    password: str = Query(None, title="Password")
):
    # Check if provided credentials match the valid ones
    if username == valid_username and password == valid_password:
        content = {"response": "1"}
        return JSONResponse(content=content)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.post('/check-in')
async def check_in(attendee_id: str):
    if attendee_id in attendees:
        if attendees[attendee_id].get('day1', False) or attendees[attendee_id].get('day2', False):
            return {'success': False, 'message': 'Attendee has already attended'}

        attendees[attendee_id]['day1'] = True
        attendees[attendee_id]['day2'] = True

        with open("attendees.json", "w") as file:
            json.dump(attendees, file, indent=2)
            
        return {'success': True, 'message': 'Check-in successful for day1 and day2', 'attendee': attendees[attendee_id]}
    else:
        raise HTTPException(status_code=404, detail='Attendee not found') 