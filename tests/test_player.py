from tests.client import create_client
from fastapi import Response

client = create_client()

def test_get_trending_players():
    response = client.get("/players")
    assert response.status_code == 200
    assert len(response.json()) == 60

def test_get_player_positions():
    response: Response = client.get("players/position-abilities/252371")
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 27
    assert json["CAM"] == 85

def test_get_player_positions_invalid_id():
    response = client.get("player/position-abilities/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"
