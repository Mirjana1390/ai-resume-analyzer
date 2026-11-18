
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st

@st.cache_resource(show_spinner="Loading AI model...")
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def split_resume_into_chunks(resume_text):

    chunks = re.split(
        r"\n|(?<=[.!?])\s+",
        resume_text
    )

    chunks = [
        chunk.strip()
        for chunk in chunks
        if len(chunk.strip().split()) >= 2
    ]

    return chunks


def semantic_match_skills(
    resume_text,
    job_skills,
    threshold=0.50
):

    model = load_model()
    resume_chunks = split_resume_into_chunks(resume_text)

    results = {}

    if not resume_chunks:
        return results

    # Convert resume chunks into embeddings
    resume_embeddings = model.encode(resume_chunks)

    for category, skills in job_skills.items():

        results[category] = {
            "matched": [],
            "missing": [],
            "details": []
        }

        for skill in skills:

            # Convert job skill into an embedding
            skill_embedding = model.encode([skill])

            # Compare with resume chunks
            similarities = cosine_similarity(
                skill_embedding,
                resume_embeddings
            )[0]

            best_index = similarities.argmax()
            best_score = float(similarities[best_index])

            best_chunk = resume_chunks[best_index]

            if best_score >= threshold:

                results[category]["matched"].append(skill)

            else:

                results[category]["missing"].append(skill)

            results[category]["details"].append({
                "skill": skill,
                "similarity": round(best_score * 100, 2),
                "resume_evidence": best_chunk,
                "matched": best_score >= threshold
            })

    return results