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
        name=player.find("a", attrs={"data-tippy-content": True}).get_text(),
        age=player.find("td", attrs={"data-col": "ae"}).get_text(),
        overall=player.find("td", attrs={"data-col": "oa"}).find("em").get_text(),
        potential=player.find("td", attrs={"data-col": "pt"}).find("em").get_text(),
        positions=[position.get_text() for position in player.find_all("td")[1].find_all("a", rel="nofollow")]
    ) for player in players]
    return players

@router.get("/position-abilities/{id}", response_model=dict[str, int])
async def get_player_position_abilities(soup= Depends(valid_player)):
    lineup = soup.find("div", class_="lineup")
    positions = lineup.find_all("div", class_="grid text-center")
    position_map = {}
    for row in positions:
        row_positions = row.find_all("div", class_="col col-1-5")
        for row_position in row_positions:
            position = row_position.find("div", class_="pos")
            if position != None:
                position_text: str = position.text
                position = position_text[:-4]
                rating = int(position_text[-4:-2]) + int(position_text[-1:])
                position_map[position] = rating
    return position_map