
import re

SKILL_CATEGORIES = {

    "Technical Skills": {
        "Python": ["python"],
        "Java": ["java"],
        "C++": ["c++"],
        "Machine Learning": ["machine learning", "ml"],
        "Deep Learning": ["deep learning"],
        "Artificial Intelligence": ["artificial intelligence"],
        "NLP": ["nlp", "natural language processing"],
        "TensorFlow": ["tensorflow"],
        "PyTorch": ["pytorch"],
        "SQL": ["sql"],
        "MySQL": ["mysql"],
        "MongoDB": ["mongodb"],
        "Flask": ["flask"],
        "Django": ["django"],
        "FastAPI": ["fastapi"],
        "HTML": ["html"],
        "CSS": ["css"],
        "JavaScript": ["javascript", "js"],
        "React": ["react"],
        "Node.js": ["node.js", "nodejs"],
        "REST API": ["rest api", "restful api"],
        "AWS": ["aws", "amazon web services"],
        "Azure": ["azure"],
        "Docker": ["docker"],
        "Git": ["git"],
        "Power BI": ["power bi"],
        "Data Analysis": ["data analysis", "data analytics"],
        "Generative AI": ["generative ai", "gen ai", "genai"],
"LLM": ["llm", "llms", "large language model"],
"RAG": ["rag", "retrieval augmented generation"],
"Neural Networks": ["neural networks", "neural network"],
"Chatbots": ["chatbot", "chatbots"],
"Computer Vision": ["computer vision", "image processing"],
"Cloud Computing": ["cloud computing", "cloud services"],
"OpenAI": ["openai"],
"Transformers": ["transformer", "transformers"],
"Prompt Engineering": ["prompt engineering"]
    },

    "Soft Skills": {
        "Communication": ["communication", "verbal communication", "written communication"],
        "Leadership": ["leadership", "team leadership"],
        "Teamwork": ["teamwork", "team player", "collaboration"],
        "Problem Solving": ["problem solving", "problem-solving"],
        "Critical Thinking": ["critical thinking"],
        "Adaptability": ["adaptability", "flexibility"],
        "Time Management": ["time management"],
        "Creativity": ["creativity", "creative thinking"],
        "Decision Making": ["decision making", "decision-making"],
        "Analytical Thinking": ["analytical thinking", "analytical skills"]
    }
}


def preprocess_text(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):

    cleaned_text = preprocess_text(text)

    extracted = {
        "Technical Skills": [],
        "Soft Skills": []
    }

    for category, skills in SKILL_CATEGORIES.items():

        for skill, aliases in skills.items():

            for alias in aliases:

                pattern = (
                    r"(?<!\w)" +
                    re.escape(alias) +
                    r"(?!\w)"
                )

                if re.search(pattern, cleaned_text):

                    extracted[category].append(skill)
                    break

    return extracted


def compare_skills(resume_text, job_description):

    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_description)

    results = {}

    for category in SKILL_CATEGORIES:

        resume_set = set(resume_skills[category])
        job_set = set(job_skills[category])

        matched = sorted(resume_set & job_set)
        missing = sorted(job_set - resume_set)

        if job_set:
            score = (len(matched) / len(job_set)) * 100
        else:
            score = 0

        results[category] = {
            "required": sorted(job_set),
            "matched": matched,
            "missing": missing,
            "score": round(score, 2)
        }

    return resume_skills, job_skills, results
def extract_job_requirements(job_description):

    must_have = {}
    good_to_have = {}

    must_match = re.search(
        r"Must have skills\s*:\s*(.*?)(?=Good to have skills|Minimum|Educational|$)",
        job_description,
        re.IGNORECASE | re.DOTALL
    )

    good_match = re.search(
        r"Good to have skills\s*:\s*(.*?)(?=Minimum|Educational|$)",
        job_description,
        re.IGNORECASE | re.DOTALL
    )

    if must_match:
        must_have = extract_skills(must_match.group(1))

    if good_match:
        good_to_have = extract_skills(good_match.group(1))

    return must_have, good_to_have