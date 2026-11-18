import streamlit as st
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
st.title("AI Resume Analyzer")

st.write(
    "Analyze your resume using Artificial Intelligence"
)
import pymupdf as fitz

from skill_extractor import (
    compare_skills,
    extract_job_requirements
)

from score_calculator import calculate_overall_score

resume = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"]
)
job_description = st.text_area(
    "Paste the Job Description",
    height=200
)
if st.button("Analyze Resume"):

    if resume is not None and job_description.strip():

        try:
            with st.spinner("Extracting resume text..."):

                with fitz.open(
                    stream=resume.getvalue(),
                    filetype="pdf"
                ) as pdf:

                    resume_text = ""

                    for page in pdf:
                        resume_text += page.get_text() + "\n"

        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            st.stop()

        if resume_text.strip():

            st.success("Resume uploaded successfully!")
            resume_skills, job_skills, results = compare_skills(
                resume_text,
                job_description
            )
            must_have, good_to_have = extract_job_requirements(
                job_description
            )
            st.divider()
            st.header("Job Requirement Classification")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Must-Have Skills")
                st.json(must_have)

            with col2:
                st.subheader("Good-to-Have Skills")
                st.json(good_to_have)

            # --------------------------------
            # EXTRACTED SKILLS
            # --------------------------------

            st.divider()
            st.header("Resume Analysis Results")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Extracted Resume Skills")
                st.json(resume_skills)

            with col2:
                st.subheader("Skills Required by Job Description")
                st.json(job_skills)
            st.divider()
            st.header("Keyword Matching Results")

            for category, data in results.items():

                st.subheader(category)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Required Skills",
                        len(data["required"])
                    )

                with col2:
                    st.metric(
                        "Matched Skills",
                        len(data["matched"])
                    )

                with col3:
                    st.metric(
                        "Match Score",
                        f"{data['score']}%"
                    )

                st.write("**Matched Skills**")

                if data["matched"]:
                    st.success(", ".join(data["matched"]))
                else:
                    st.info("No matching skills found.")

                st.write("**Missing Skills**")

                if data["missing"]:
                    st.warning(", ".join(data["missing"]))
                else:
                    st.success("No missing skills!")

                if not data["required"]:
                    st.info(
                        "No recognized skills found in this category."
                    )

           
            st.divider()
            st.header("Semantic Matching Results")

            st.write(
                "Semantic matching compares the meaning of "
                "job requirements with your resume content."
            )

            if not any(job_skills.values()):

                st.warning(
                    "No recognized job skills were found. "
                    "Please provide a more detailed job description."
                )

            else:

                try:

                    with st.spinner(
                        "Loading AI model and performing "
                        "semantic matching... Please wait."
                    ):

                        from semantic_matcher import semantic_match_skills

                        semantic_results = semantic_match_skills(
                            resume_text,
                            job_skills,
                            threshold=0.50
                        )

                except Exception:

                    st.error(
                        "Semantic matching could not be completed."
                    )
                    import logging
                    logging.getLogger(__name__).exception("Semantic matching failed")
                    st.stop()

                # --------------------------------
                # DISPLAY SEMANTIC MATCHING
                # --------------------------------

                for category, data in semantic_results.items():

                    st.subheader(category)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Semantic Matches",
                            len(data["matched"])
                        )

                    with col2:
                        st.metric(
                            "Semantic Missing Skills",
                            len(data["missing"])
                        )

                    st.write("**Semantically Matched Skills**")

                    if data["matched"]:
                        st.success(", ".join(data["matched"]))
                    else:
                        st.info("No semantic matches found.")

                    st.write("**Skills Not Matched Semantically**")

                    if data["missing"]:
                        st.warning(", ".join(data["missing"]))
                    else:
                        st.success("All skills matched!")

                    st.write("**Similarity Details**")

                    for item in data["details"]:

                        st.write(
                            f"**{item['skill']}** — "
                            f"{item['similarity']}%"
                        )

                        st.caption(
                            "Resume evidence: "
                            + item["resume_evidence"]
                        )

                        st.progress(
                            max(
                                0.0,
                                min(item["similarity"] / 100, 1.0)
                            )
                        )

                # --------------------------------
                # OVERALL RESUME MATCH SCORE
                # --------------------------------

                st.divider()

                st.header("Overall Resume Match Score")

                score_data = calculate_overall_score(
                    job_skills,
                    results,
                    semantic_results,
                    must_have,
                    good_to_have
                )

                overall_score = score_data["overall_score"]

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Overall Resume Match",
                        f"{overall_score}%"
                    )

                with col2:

                    if score_data["must_have_score"] is not None:

                        st.metric(
                            "Must-Have Skills Match",
                            f"{score_data['must_have_score']}%"
                        )

                    else:

                        st.metric(
                            "Must-Have Skills Match",
                            "N/A"
                        )
                st.progress(
                    max(0.0, min(overall_score / 100, 1.0))
                )
                st.subheader("Detailed Skill Scoring")

                if score_data["skill_details"]:

                    st.dataframe(
                        score_data["skill_details"],
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No recognized job skills available for scoring."
                    )
                st.subheader("How Your Score Is Calculated")

                st.write(
                    "The overall resume match score uses weighted "
                    "skill matching:"
                )

                st.write(
                    "- Must-Have Skills: 3x weight\n"
                    "- Good-to-Have Skills: 1.5x weight\n"
                    "- Other Job Skills: 1x weight"
                )

                st.write(
                    "Exact keyword matches receive 100 points. "
                    "Otherwise, semantic similarity is used."
                )

                st.info(
                    "This is a project-specific skill compatibility "
                    "score, not an official ATS score or a prediction "
                    "of hiring success. Experience and education "
                    "requirements are not included yet."
                )


            st.divider()

            st.caption(
                "AI similarity scores indicate textual similarity, "
                "not verified skill proficiency."
            )

        else:

            st.error(
                "Could not extract text from the PDF. "
                "The PDF may be scanned or image-based."
            )

    else:

        st.warning(
            "Please upload your resume and enter a job description."
        )