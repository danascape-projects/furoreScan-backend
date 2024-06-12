from fastapi import FastAPI, Depends, HTTPException, Form, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

json_list_path = "json_list.json"
try:
    with open("json_list.json", "r") as file:
        json_strings = json.load(file)
except FileNotFoundError:
    json_strings = {}

# Parse each string into a JSON object
json_list = [json.loads(json_str) for json_str in json_strings]

# Create a set of IDs for fast lookup
ids_set = {item["ID"] for item in json_list}

class IDCheckResponse(BaseModel):
    id: str
    found: bool

def save_json_list():
    """Save the json_list back to the json_list.json file"""
    with open(json_list_path, 'w') as json_file:
        json.dump([json.dumps(item) for item in json_list], json_file, indent=4)

@app.get("/")
def read_hello():
    content = {"message": "Hello, World!"}
    return JSONResponse(content=content)
    
@app.post('/check-in')
async def check_in(attendee_id: str):
    for item in json_list:
        if item["ID"] == id:
            # Update day1 to true
            item["day1"] = "true"
            item["day2"] = "true"
            save_json_list()

            return {'detail': False, 'message': 'Attendee has already attended', 'attendee': attendee_id}
    # if attendee_id in ids_set:
    #     if ids_set[attendee_id].get('day1', False) and ids_set[attendee_id].get('day2', False):
    #         return {'detail': False, 'message': 'Attendee has already attended', 'attendee': attendee_id}

    #     if not ids_set[attendee_id].get('day1', False):
    #         ids_set[attendee_id]['day1'] = True
            
    #         with open("attendees.json", "w") as file:
    #             json.dump(ids_set, file, indent=2)

    #         return {'detail': True, 'message': 'day1', 'attendee': attendee_id}


    #     if not ids_set[attendee_id].get('day2', False):
    #         attendees[attendee_id]['day2'] = True

    #         with open("attendees.json", "w") as file:
    #             json.dump(attendees, file, indent=2)

    #         return {'detail': True, 'message': 'day2', 'attendee': attendee_id}


        return {'success': True, 'message': 'Check-in successful for day1', 'attendee': attendee_id}
    else:
        raise HTTPException(status_code=404, detail='Attendee not found') 