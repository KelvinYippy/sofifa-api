from fastapi import APIRouter, Depends
from dependencies import valid_team
from models.player import Player
from models.team import Team, TeamType
from utils import fetch
from bs4 import BeautifulSoup

router = APIRouter()


@router.get("/", response_model=list[Team])
async def get_teams(type: TeamType = TeamType.TRENDING):
    type_hash_map = {
        TeamType.CLUB: "?type=club",
        TeamType.NATIONAL: "?type=national",
        TeamType.TRENDING: ""
    }
    team_type = type_hash_map[type]
    soup = fetch(f"https://sofifa.com/teams{team_type}")
    team_table = soup.find("table").find("tbody")
    teams = team_table.find_all("tr")
    result = []
    for team in teams:
        basic_info = team.find("td", class_="s20").find_all("a")
        name = basic_info[0].text
        crest = team.find("td", class_="a1").find("img")["data-src"]
        squad_size = team.find("td", attrs={"data-col": "ps"}).text
        if len(basic_info) > 1:
            country = basic_info[1].find("img")["title"]
            league = basic_info[1].text[1:]
        else:
            country = basic_info[0].text
            league = "Friendly International"
        result.append(Team(
            name=name,
            crest=crest,
            country=country,
            league=league,
            squad_size=squad_size
        ))
    return result

@router.get("/{id}", response_model=Team)
async def get_team_by_id(soup: BeautifulSoup = Depends(valid_team)):
    team_info = soup.find("div", class_="profile clearfix")
    name = team_info.find("h1").text
    crest = team_info.find("img")["data-src"]
    location_info = team_info.find("p")
    country = location_info.find("a")["title"]
    league = location_info.text
    squad_size = len(soup.find("tbody").find_all("tr"))
    return Team(
        name=name,
        crest=crest,
        country=country,
        league=league,
        squad_size=squad_size
    )

def get_players(soup: BeautifulSoup, class_name: str):
    players = soup.find("tbody").find_all("tr", class_=class_name)
    players = [Player(
        name=player.find("td", class_="col-name").find("a", role="tooltip").get_text(),
        age=player.find("td", class_="col col-ae").get_text(),
        overall=player.find("td", class_="col col-oa").get_text(),
        potential=player.find("td", class_="col col-pt").get_text(),
        positions=[position.get_text() for position in player.find("td", class_="col-name").find_all("a", rel="nofollow")]
    ) for player in players]
    return players

@router.get("/{id}/starting_lineup", response_model=list[Player])
async def get_team_starting_lineup_by_id(soup: BeautifulSoup = Depends(valid_team)):
    return get_players(soup, "starting")

@router.get("/{id}/substitutes", response_model=list[Player])
async def get_team_substitutes_by_id(soup: BeautifulSoup = Depends(valid_team)):
    return get_players(soup, "sub")

@router.get("/{id}/reserves", response_model=list[Player])
async def get_team_reserves_by_id(soup: BeautifulSoup = Depends(valid_team)):
    return get_players(soup, "res")
