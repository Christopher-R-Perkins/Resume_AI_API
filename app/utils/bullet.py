from app.models.bullet import BulletRatingList

def score_bullets(bullet_ratings: list[BulletRatingList], bullets: list[str]) -> list[float]:
    scores: list[float] = []
    for rating, bullet in zip(bullet_ratings, bullets):
        score: float = max(10 * (1 - max(len(bullet) - 100, 0) / 200), 0)

        if rating.strong_action_verb:
            score += 10
        if rating.clear_meaning:
            score += 10
        if rating.has_quantifiable_result:
            score += 5
        if rating.result_makes_sense:
            score += 7
        if rating.skill_can_be_deduced:
            score += 5
        if rating.skill_is_valuable:
            score += 3
        if rating.is_readable:
            score += 10
        if rating.is_specific:
            score += 5
        if rating.keyword_added:
            score += 10

        score /= 75.0

        scores.append(score)
    return scores