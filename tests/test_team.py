from tests.client import create_client
from fastapi import Response

client = create_client()

def test_get_trending_teams():
    response = client.get("/teams")
    assert response.status_code == 200
    assert len(response.json()) == 60

def test_get_club_teams():
    response = client.get("/teams?type=club")
    assert response.status_code == 200
    assert len(response.json()) == 60
    first_team = response.json()[0]
    assert first_team["name"] == "Manchester City"
    assert first_team["crest"] == 'https://cdn.sofifa.net/meta/team/9/60.png'
    assert first_team["country"] == "England"
    assert first_team["league"] == "Premier League"
    assert first_team["squad_size"] == 26

def test_get_national_teams():
    response = client.get("/teams?type=national")
    assert response.status_code == 200
    first_team = response.json()[0]
    assert len(response.json()) == 35
    assert first_team["name"] == "England"
    assert first_team["crest"] == 'https://cdn.sofifa.net/meta/team/18645/60.png'
    assert first_team["country"] == "Rest of World"
    assert first_team["league"] == "Friendly International"
    assert first_team["squad_size"] == 23
