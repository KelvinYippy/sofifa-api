from fastapi import FastAPI
from utils import fetch
from models.player import Player
from models.team import Team

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the sofifa-api!"}


@app.get("/players")
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


@app.get("/teams")
async def get_teams():
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
                else:
                    league += c
        return country, league.lstrip()
    soup = fetch("https://sofifa.com/teams")
    team_table = soup.find("table").find("tbody")
    teams = team_table.find_all("tr")
    result = []
    for team in teams:
        basic_info = team.find("td", class_="col-name-wide").find_all("div", class_="ellipsis")
        name = basic_info[0].text
        crest = team.find("td", class_="col-avatar").find("img")["data-src"]
        squad_size=team.find("td", class_="col col-ps").text
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