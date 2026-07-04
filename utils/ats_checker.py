import re

TECH_SKILLS = [
    "python","java","c++","c","javascript","typescript",
    "react","next","node","express","django","flask",
    "fastapi","sql","mysql","postgresql","mongodb",
    "pandas","numpy","scikit","tensorflow","keras",
    "pytorch","docker","kubernetes","git","github",
    "aws","azure","gcp","linux","html","css"
]


def check_resume(text):

    text_lower = text.lower()

    score = 0

    report = {}

    # Contact

    email = bool(re.search(r'[\w\.-]+@[\w\.-]+', text))
    phone = bool(re.search(r'\+?\d[\d\s-]{8,}', text))

    report["Email"] = email
    report["Phone"] = phone

    if email:
        score += 10

    if phone:
        score += 10

    # LinkedIn

    linkedin = "linkedin" in text_lower
    github = "github" in text_lower

    report["LinkedIn"] = linkedin
    report["GitHub"] = github

    if linkedin:
        score += 10

    if github:
        score += 10

    # Education

    education = any(word in text_lower for word in [
        "b.tech","btech","bachelor","master","m.tech","degree"
    ])

    report["Education"] = education

    if education:
        score += 10

    # Projects

    projects = "project" in text_lower

    report["Projects"] = projects

    if projects:
        score += 15

    # Experience

    experience = any(word in text_lower for word in [
        "experience","internship","worked"
    ])

    report["Experience"] = experience

    if experience:
        score += 15

    # Skills

    found = []

    for skill in TECH_SKILLS:

        if skill in text_lower:

            found.append(skill)

    score += min(len(found),10)

    return {

        "ats_score": min(score,100),

        "skills": found,

        "checklist": report

    }