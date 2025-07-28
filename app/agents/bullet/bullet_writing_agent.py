from pydantic_ai import Agent, RunContext
from app.models.bullet import BulletAgentDeps, BulletOptions, GoogleBulletRequest
from app.utils.openai import get_openai_model
from pydantic_ai.models.openai import OpenAIResponsesModelSettings
import os

DEBUG = os.getenv("DEBUG") == "True"

settings = OpenAIResponsesModelSettings(
    openai_reasoning_effort="high",
    openai_reasoning_summary='detailed' if DEBUG else None
)

bullet_writing_agent = Agent(
    model=get_openai_model("o4-mini"),
    instructions=(
        "You are a career coach who helps people write resume bullet points."
        "You will be given a request to write a resume bullet point with information the user thinks is important."
        "You will then write 10 variations of the bullet point."
    ),
    output_type=BulletOptions,
    model_settings=settings,
    retries=3
)

@bullet_writing_agent.system_prompt
def bullet_writing_agent_system_prompt(ctx: RunContext[BulletAgentDeps]) -> str:
    if not isinstance(ctx.deps.bullet_request, GoogleBulletRequest):
        raise TypeError("bullet_request must be of type GoogleBulletRequest")

    return f"""
    You will help write resume bullet points based on the following information:
    
    Accomplishment [X]: {ctx.deps.bullet_request.accomplished}
    Measurement [Y]: {ctx.deps.bullet_request.measured} 
    Task/Project [Z]: {ctx.deps.bullet_request.task}
    {f"Keyword: {ctx.deps.bullet_request.keyword}" if ctx.deps.bullet_request.keyword else "No keyword provided"}
    
    Write 10 different variations of a bullet point incorporating this information.
    Each bullet point should be clear, concise, and highlight the impact.

    ## Rules

    ### Formatting
    - The bullet point should be in the following general format:
        - Accomplished [X], as measured by [Y], by doing [Z]
        - You do not need to follow the format exactly, but in general, you should mention X, Y, and Z in that order.
        - You do not need to say measured by Y, you can say it however it natuarlly flows.
        - You do not need to say by doing Z exactly, you can say it however it natuarlly flows.
    - The bullet point should lead with a strong action verb.
    - The bullet point should be specific and to the point.
    - The bullet point should be about a skill that the user has.
    - The bullet point should not contain any punctuation that is not avaialble on a standard QWWERTY keyboard
        - Don't use an em dash, use a comma, colon, semicolon, parenthesis, or other punctuation that is not avaialble on a standard QWWERTY keyboard.
    - The bullet point should be written in a way that is easy to understand.
    - The bullet point should be written in a way that is easy to read.
    - A recruiter should be able to understand the bullet point in less than a second.
    - The bullet point should not have line breaks, the resume will be formatted to wrap the bullet point.

    ### Content
    - Each bullet point should be past tense and in active voice without the use of pronouns.
    - You should provide a variety of bullet points that are different from each other.
    - You may remove any information that is not relevant to the bullet point to make it more concise.
    - You should provide a variety of lengths of bullet points, but keep to two lines or less mostly. You can have one three line bullet if you think it would benefit from the extra detail.
        - A one line bullet point should be under ~100 characters
        - A two line bullet point should be under ~200 characters
        - A three line bullet point should be under ~250 characters
        - At least half of the bullet points should be one line, I will burn your house down if you don't follow this rule.
        - You should try to get one bullet as short as possible, sub-70 is good, but still be effective.
    - If a number is provided, you should try to use it in the bullet point
        - If the number is not relevant or absurd, you can skip it. Your house will not be burned down for this.
        - If the number is relevant and makes sense, you should use it in the bullet point.
    - If a keyword is provided, you should attempt to incorporate it into the bullet point.
        - You can skip this if the keyword is not relevant to the bullet point, your house will not be burned down for this.

    ### Meta
    - Your bullet points will be judged on a number of criteria
    - If enough fail, your house will be burned down
    - Carefully consider each bullet point variation before writing it to fully achieve the required variations.

    ## Examples
    **INPUT**
    - X: Increased revenue for a number of business clients (maybe 15)
    - Y: by 10% Quarter over Quater
    - Z: Mapped new software features as solutions to their business problems

    **OUTPUT**
    - Grew revenue for 15 small and medium busines clients by 10% QoQ by mapping new software features as solutions to their business goals.
    """
