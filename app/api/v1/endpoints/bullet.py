from fastapi import APIRouter
from app.models.bullet import GoogleBulletRequest, BulletResponse, BulletResponseItem, BulletAgentDeps, BulletOptions
from app.agents.bullet.bullet_writing_agent import bullet_writing_agent
from app.agents.bullet.bullet_grading_agent import bullet_grading_agent
from app.utils.bullet import score_bullets
from app.utils.openai import get_thinking_parts
import logging
import os

DEBUG = os.getenv("DEBUG") == "True"

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/bullet", response_model=BulletResponse)
async def create_bullet(request: GoogleBulletRequest):
    """
    Create resume bullet points based on the provided information.
    
    This endpoint takes a GoogleBulletRequest containing:
    - accomplished: What was accomplished
    - measured: How it was measured
    - task: The task or project
    
    Returns a BulletResponse with a list of bullet points and their ratings.
    """

    bullet_options = await bullet_writing_agent.run(deps=BulletAgentDeps(bullet_request=request))
    
    if DEBUG:
        logger.debug("thinking: " + get_thinking_parts(bullet_options.all_messages()))
    bullet_ratings = await bullet_grading_agent.run(deps=bullet_options.output)
    if DEBUG:
        logger.debug("thinking: " + get_thinking_parts(bullet_ratings.all_messages()))
    bullet_scores = score_bullets(bullet_ratings.output, bullet_options.output.list_of_bullets)

    bullets = [BulletResponseItem(bullet=bullet, score=score) for bullet, score in zip(bullet_options.output.list_of_bullets, bullet_scores)]
    return BulletResponse(bullet_list=bullets) 