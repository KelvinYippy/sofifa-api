from fastapi import APIRouter
from routes.player import router as player_router
from routes.team import router as team_router

router = APIRouter()
router.include_router(player_router, prefix="/players")
router.include_router(team_router, prefix="/teams")