import requests 
import json
from datetime import datetime, timezone
import os.path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def pegar_token():
    creds = Credentials.from_service_account_file("KEY.json",scopes=SCOPES)
    return build("calendar","v3",credentials=creds)

        

def timestamp_to_iso(ts):
    return datetime.fromtimestamp(ts,tz=timezone.utc).isoformat()

def colher_contests():
    urlcf = "https://codeforces.com/api/contest.list"
    response = requests.get(urlcf)

    if response.status_code != 200:
        print("Nao foi acessar a api do codeforces")
        exit()

    data = response.json()

    print("Status da Api: ", data["status"])

    contest = []
    for i in data["result"]:
        if i["phase"] != "BEFORE":
            break
        contest.append({
            "summary": i["name"],
            "start": {
                "dateTime": timestamp_to_iso(i["startTimeSeconds"]),
                "timeZone": "America/Sao_Paulo"
            },
            "end": {
                "dateTime": timestamp_to_iso(i["startTimeSeconds"]+i["durationSeconds"]),
                "timeZone": "America/Sao_Paulo"
            },
            "description": "Contest link: https://codeforces.com/contests/" + str(i["id"]) 
        })

    return contest


def post_contest(contest):
    creds = pegar_token()
    calendarid = "8962961efb508f69ae701db8228e78dc62e8e02227d3ae51850a23a5d8c2bce9@group.calendar.google.com"
    for i in contest: 
        created_event = creds.events().insert(calendarId=calendarid, body=i).execute()
        print("Evento criado: ",created_event["htmlLink"])


contests = colher_contests()

post_contest(contests)


