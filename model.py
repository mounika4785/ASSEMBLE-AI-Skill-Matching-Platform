from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def match_students(students, opportunity):

    results = []

    # ✅ Normalize required skills ONCE
    required_skills = [skill.lower().strip() for skill in opportunity.get("required_skills", [])]
    required_set = set(required_skills)

    # 🔹 Prepare text data for cosine similarity
    student_profiles = []
    for s in students:
        text = " ".join(s["skills"]) + " " + " ".join(s.get("interests", []))
        student_profiles.append(text)

    opportunity_text = " ".join(opportunity.get("required_skills", [])) + " " + opportunity.get("description", "")

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(student_profiles + [opportunity_text])

    student_vectors = vectors[:-1]
    opportunity_vector = vectors[-1]

    cosine_scores = cosine_similarity(student_vectors, opportunity_vector)

    # 🔹 Process each student
    for i, student in enumerate(students):

        # ✅ Normalize student skills
        student_skills_list = [skill.lower().strip() for skill in student.get("skills", [])]
        student_set = set(student_skills_list)

        # ✅ Matched skills
        matched = required_set.intersection(student_set)

        # ✅ Skill Score
        skill_score = len(matched) / len(required_set) if required_set else 0

        # 🔹 Level Score
        level_map = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3
        }

        level_score = 0
        skill_levels = student.get("skill_levels", {})

        for skill in matched:
            level = skill_levels.get(skill, "beginner").lower()
            level_score += level_map.get(level, 1)

        level_score = (level_score / (len(matched) * 3)) if matched else 0

        # 🔹 Cosine similarity
        cosine_score = float(cosine_scores[i][0])

        # 🔹 Achievement score
        achievements = student.get("achievements", [])
        achievement_score = min(len(achievements) * 0.05, 0.2)

        # 🔹 Final score
        final_score = (
            0.5 * skill_score +
            0.2 * level_score +
            0.2 * cosine_score +
            achievement_score
        )

        # ✅ CORRECT missing skills logic (ONLY here)
        missing = list(required_set - student_set)

        # 🔹 Store result
        results.append({
            "name": student["name"],
            "score": round(final_score, 2),
            "missing_skills": missing,
            "achievements": achievements
        })

    # 🔹 Sort by best match
    results.sort(key=lambda x: x["score"], reverse=True)

    return results