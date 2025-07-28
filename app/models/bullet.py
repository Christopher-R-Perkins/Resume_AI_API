from typing import Optional
from pydantic import BaseModel

class GoogleBulletRequest(BaseModel):
    """
    This is the request body for the Google Bullet API.
    """
    accomplished: str
    measured: str
    task: str
    keyword: Optional[str]

class BulletOptions(BaseModel):
    """
    This is the response body for the Google Bullet API.
    """
    list_of_bullets: list[str]
    keyword: Optional[str]

class BulletRatingList(BaseModel):
    strong_action_verb: bool
    clear_meaning: bool
    has_quantifiable_result: bool
    result_makes_sense: bool
    skill_can_be_deduced: bool
    skill_is_valuable: bool
    is_readable: bool
    is_specific: bool
    keyword_added: bool

class BulletResponseItem(BaseModel):
    bullet: str
    score: float

class BulletResponse(BaseModel):
    bullet_list: list[BulletResponseItem]

class BulletAgentDeps(BaseModel):
    bullet_request: GoogleBulletRequest