import json
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, ValidationError


origins = [
    "http://localhost:4200"
]


class ClubMember(BaseModel):
    name: str
    age: int


class Club(BaseModel):
    index: Optional[int] = None
    club_members: List[ClubMember]
    club_name: str
    club_address: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def validate_list(list_object):
    print(list_object)
    try:
        for club in list_object:
            Club(**club)
    except ValidationError as e:
        print(e)


def get_response():
    with open('database.json') as fp:
        data = json.load(fp)
    return {
        "list": data
    }


def update_club(index, club: Club):
    with open('database.json', 'r') as fp:
        database = json.load(fp)
    clubs = database['clubs']
    clubs[index] = club.dict()
    database['clubs'] = clubs
    with open('database.json', 'w') as fp:
        fp.write(json.dumps(database, indent=2))


@app.get("/clubs")
async def get_clubs():
    validate_list(get_response()['list']['clubs'])
    return get_response()


@app.post("/clubs")
async def post_clubs(club: Club):
    index = club.index
    del club.index
    update_club(index, club)
    return club
