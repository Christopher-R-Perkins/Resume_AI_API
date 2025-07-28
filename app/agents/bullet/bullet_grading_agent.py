from pydantic_ai import Agent, RunContext
from app.models.bullet import BulletOptions, BulletRatingList
from app.utils.openai import get_openai_model
from pydantic_ai.models.openai import OpenAIResponsesModelSettings
import os

DEBUG = os.getenv("DEBUG") == "True"

settings = OpenAIResponsesModelSettings(
    openai_reasoning_effort="low",
    openai_reasoning_summary='detailed' if DEBUG else None
)

bullet_grading_agent = Agent(
    model=get_openai_model("o4-mini"),
    instructions=(
        "You are a career coach who helps people write resume bullet points."
        "You will be given a list of bullet points and a request to grade them."
        "You will then grade the bullet points on a number of criteria."
        "You will grade the bullets by answering a series of questions with True or False."
    ),
    output_type=list[BulletRatingList],
    model_settings=settings
)

@bullet_grading_agent.system_prompt
def bullet_grading_agent_system_prompt(ctx: RunContext[BulletOptions]) -> str:
    return f"""
    ## Input
    - Bullet Points:
      {"\n      ".join(f"{i+1}. {bullet}" for i, bullet in enumerate(ctx.deps.list_of_bullets))}
    - {f"Keyword: {ctx.deps.keyword}" if ctx.deps.keyword else "No keyword provided"}

    ## Grading Criteria
    - Strong Action Verb: Does the bullet point lead with a strong action verb?
    - Clear Meaning: Does the bullet point have a clear meaning? 
    - Has Quantifiable Result: Does the bullet point have a quantifiable result? If there is no quantification, it is not quantifiable.
    - Result Makes Sense: Does the result make sense? If the result seems to be out of proportion to the accomplishment, it doesnt make sense.
    - Skill Can Be Deducted: Can the skill be deduced from the bullet point? If you cannot deduce the skill, it is also not valuable.
    - Skill is Valuable: Is the skill deduced from the bullet point valuable to a potential employer? If it is not, it is not valuable.
    - Is Readable: Is the bullet point easily digestible at a quick glance? Could a recruiter understand it in less than a second? If you feel it is too complex to be understood at a glance, it is not readable.
    - Is Specific: Is the bullet point specific about what it is describing? If anything feels ambiguous, it is not specific.
    - Keyword Added: Is the keyword part of the bullet point? 

    ## Rules
    - You should provide a rating list for each bullet point
    - Grade each bullet point based on the grading criteria
    - You should grade each bullet point individually and not as a whole. You should evaluate each one separately.
    - Does the action verb make sense? If it does not, it is not a strong action verb.
    """