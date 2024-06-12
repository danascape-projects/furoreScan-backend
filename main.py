from fastapi import FastAPI, Depends, HTTPException, Form, Query
from fastapi.responses import JSONResponse
import json

app = FastAPI()

try:
    with open("attendees1.json", "r") as file:
        attendees = json.load(file)
except FileNotFoundError:
    attendees = {}

@app.get("/")
def read_hello():
    content = {"message": "Hello, World!"}
    return JSONResponse(content=content)
    
@app.post('/check-in')
async def check_in(attendee_id: str):
    if attendee_id in attendees:
        if attendees[attendee_id].get('day1', False) and attendees[attendee_id].get('day2', False):
            return {'detail': False, 'message': 'Attendee has already attended', 'attendee': attendee_id}

        if not attendees[attendee_id].get('day1', False):
            attendees[attendee_id]['day1'] = True
            
            with open("attendees.json", "w") as file:
                json.dump(attendees, file, indent=2)

            return {'detail': True, 'message': 'day1', 'attendee': attendee_id}


        if not attendees[attendee_id].get('day2', False):
            attendees[attendee_id]['day2'] = True

            with open("attendees.json", "w") as file:
                json.dump(attendees, file, indent=2)

            return {'detail': True, 'message': 'day2', 'attendee': attendee_id}


        # return {'success': True, 'message': 'Check-in successful for day1 and day2', 'attendee': attendees[attendee_id]}
    else:
        raise HTTPException(status_code=404, detail='Attendee not found') 
