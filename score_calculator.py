
def calculate_overall_score(
    job_skills,
    keyword_results,
    semantic_results,
    must_have,
    good_to_have
):

    # Convert skill dictionaries into sets
    must_set = set()
    good_set = set()

    for skills in must_have.values():
        must_set.update(skills)

    for skills in good_to_have.values():
        good_set.update(skills)

    # Store exact keyword matches
    keyword_matched = set()

    for category, data in keyword_results.items():
        keyword_matched.update(data["matched"])

    total_weighted_score = 0
    total_weight = 0

    must_score = 0
    must_weight = 0

    skill_details = []

    for category, skills in job_skills.items():

        # Get semantic similarity details
        semantic_details = {}

        if category in semantic_results:
            for item in semantic_results[category]["details"]:
                semantic_details[item["skill"]] = (
                    item["similarity"]
                )

        for skill in skills:

            # Determine skill importance
            if skill in must_set:
                weight = 3.0
                priority = "Must-Have"

            elif skill in good_set:
                weight = 1.5
                priority = "Good-to-Have"

            else:
                weight = 1.0
                priority = "Other Requirement"

            # Get semantic similarity
            similarity = semantic_details.get(skill, 0)

            # Exact keyword match receives 100 points
            if skill in keyword_matched:
                skill_score = 100

            else:
                skill_score = max(0, similarity)

            # Calculate weighted score
            total_weighted_score += skill_score * weight
            total_weight += weight

            if priority == "Must-Have":
                must_score += skill_score * weight
                must_weight += weight

            skill_details.append({
                "Skill": skill,
                "Priority": priority,
                "Keyword Match": (
                    "Yes" if skill in keyword_matched else "No"
                ),
                "Semantic Similarity": similarity,
                "Final Skill Score": round(skill_score, 2)
            })

    # Calculate overall score
    if total_weight > 0:
        overall_score = total_weighted_score / total_weight
    else:
        overall_score = 0

    # Calculate must-have score
    if must_weight > 0:
        must_have_score = must_score / must_weight
    else:
        must_have_score = None

    return {
        "overall_score": round(overall_score, 2),
        "must_have_score": (
            round(must_have_score, 2)
            if must_have_score is not None
            else None
        ),
        "skill_details": skill_details
    }