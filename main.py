from fastapi import FastAPI, Depends
from dependencies import valid_scrape
from utils import fetch
from models.player import Player
from models.team import Team, TeamType
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the sofifa-api!"}


@app.get("/players", response_model=list[Player])
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


def split_country_league(text: str):
    is_country = False
    country = ""
    league = ""
    for c in text:
        if c == "[":
            is_country = True
        elif c == "]":
            is_country = False
        else:
            if is_country:
                country += c
            elif not (c == " " and len(league) == 0):
                league += c
    return country, league


@app.get("/teams", response_model=list[Team])
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
        basic_info = team.find("td", class_="col-name-wide").find_all("div", class_="ellipsis")
        name = basic_info[0].text
        crest = team.find("td", class_="col-avatar").find("img")["data-src"]
        squad_size = team.find("td", class_="col col-ps").text
        country_league_text = basic_info[1].text
        country, league = split_country_league(country_league_text)
        result.append(Team(
            name=name,
            crest=crest,
            country=country,
            league=league,
            squad_size=squad_size
        ))
    return result

@app.get("/teams/{id}", response_model=Team)
async def get_team_by_id(soup: BeautifulSoup = Depends(valid_scrape)):
    team_info = soup.find("div", class_="bp3-card player")
    name = team_info.find("div", class_="info").find("h1").text
    crest = team_info.find_all("img")[0]["data-src"]
    country, league = split_country_league(team_info.find("div", class_="info").find("div", class_="meta ellipsis").text)
    squad_size = len(soup.find_all("tbody")[0].find_all("tr"))
    return Team(
        name=name,
        crest=crest,
        country=country,
        league=league,
        squad_size=squad_size
    )

@app.get("/teams/{id}/starting_lineup", response_model=list[Player])
async def get_team_starting_lineup_by_id(soup: BeautifulSoup = Depends(valid_scrape)):
    starting_players = soup.find_all("tbody")[0].find_all("tr", class_="starting")
    starting_players = [Player(
        name=player.find("td", class_="col-name").find("a", role="tooltip").get_text(),
        age=player.find("td", class_="col col-ae").get_text(),
        overall=player.find("td", class_="col col-oa").get_text(),
        potential=player.find("td", class_="col col-pt").get_text(),
        positions=[position.get_text() for position in player.find("td", class_="col-name").find_all("a", rel="nofollow")]
    ) for player in starting_players]
    return starting_players

@app.get("/teams/{id}/substitutes", response_model=list[Player])
async def get_team_substitutes_by_id(soup: BeautifulSoup = Depends(valid_scrape)):
    substitutes = soup.find_all("tbody")[0].find_all("tr", class_="sub")
    substitutes = [Player(
        name=player.find("td", class_="col-name").find("a", role="tooltip").get_text(),
        age=player.find("td", class_="col col-ae").get_text(),
        overall=player.find("td", class_="col col-oa").get_text(),
        potential=player.find("td", class_="col col-pt").get_text(),
        positions=[position.get_text() for position in player.find("td", class_="col-name").find_all("a", rel="nofollow")]
    ) for player in substitutes]
    return substitutes

@app.get("/teams/{id}/reserves", response_model=list[Player])
async def get_team_reserves_by_id(soup: BeautifulSoup = Depends(valid_scrape)):
    reserves = soup.find_all("tbody")[0].find_all("tr", class_="res")
    reserves = [Player(
        name=player.find("td", class_="col-name").find("a", role="tooltip").get_text(),
        age=player.find("td", class_="col col-ae").get_text(),
        overall=player.find("td", class_="col col-oa").get_text(),
        potential=player.find("td", class_="col col-pt").get_text(),
        positions=[position.get_text() for position in player.find("td", class_="col-name").find_all("a", rel="nofollow")]
    ) for player in reserves]
    return reserves
