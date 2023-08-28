from fastapi import APIRouter, Depends
from dependencies import valid_player
from models.player import Player
from utils import fetch

router = APIRouter()

@router.get("/", response_model=list[Player])
async def get_players():
    soup = fetch("https://sofifa.com/players")
    player_table = soup.find("tbody")
    players = player_table.find_all("tr")
    players = [Player(
        name=player.find("td", class_="col-name").find("a", role="tooltip").get_text(),
        age=player.find("td", class_="col col-ae").get_text(),
        overall=player.find("td", class_="col col-oa").get_text(),
        potential=player.find("td", class_="col col-pt").get_text(),
        positions=[position.get_text() for position in player.find("td", class_="col-name").find_all("a", rel="nofollow")]
    ) for player in players]
    return players

@router.get("/position-abilities/{id}", response_model=dict[str, int])
async def get_player_position_abilities(soup= Depends(valid_player)):
    lineup = soup.find("div", class_="lineup")
    positions = lineup.find_all("div", class_="grid half-spacing")
    position_map = {}
    for row in positions:
        row_positions = row.find_all("div", class_="col col-2")
        for row_position in row_positions:
            position = row_position.find("div", class_="bp3-tag")
            if position != None:
                position_text: str = position.text
                position = position_text[:-4]
                rating = int(position_text[-4:-2]) + int(position_text[-1:])
                position_map[position] = rating
    return position_map