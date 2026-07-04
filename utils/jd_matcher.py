import re

COMMON_SKILLS = [

    "python","java","c++","javascript","react","node",

    "express","django","flask","fastapi",

    "sql","mysql","mongodb","postgresql",

    "aws","azure","gcp",

    "docker","kubernetes",

    "tensorflow","pytorch",

    "machine learning","deep learning",

    "git","github",

    "html","css"

]


def extract_skills(text):

    text = text.lower()

    found = []

    for skill in COMMON_SKILLS:

        if skill in text:

            found.append(skill)

    return found


def match_resume(resume, jd):

    resume_skills = extract_skills(resume)

    jd_skills = extract_skills(jd)

    matched = list(set(resume_skills) & set(jd_skills))

    missing = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) == 0:

        score = 0

    else:

        score = int(

            len(matched)

            /

            len(jd_skills)

            *

            100

        )

    return {

        "score": score,

        "matched": matched,

        "missing": missing

    }