from tests.client import create_client

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

def test_get_starting_lineup():
    response = client.get("/teams/1/starting_lineup")
    assert response.status_code == 200
    assert len(response.json()) == 11
    json = response.json()[1]
    assert json["name"] == "B. White"
    assert json["age"] == 24
    assert json["overall"] == 80
    assert json["potential"] == 84
    assert json["positions"] == ["RB", "CB"]

def test_get_subs():
    response = client.get("/teams/1/substitutes")
    assert response.status_code == 200
    assert len(response.json()) == 7
    json = response.json()[0]
    assert json["age"] == 27
    assert json["name"] == "L. Trossard"
    assert json["overall"] == 80
    assert json["positions"] == ["CF", "LM"]
    assert json["potential"] == 80

def test_get_reserves():
    response = client.get("/teams/1/reserves")
    assert response.status_code == 200
    assert len(response.json()) == 14
    json = response.json()[1]
    assert json["age"] == 21
    assert json["name"] == "E. Smith Rowe"
    assert json["overall"] == 79
    assert json["potential"] == 86
    assert json["positions"] == ["LW", "CAM"]