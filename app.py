import pandas as pd
import streamlit as st

from matcher import classify_college, profile_bonus


st.set_page_config(page_title="College Match Finder", page_icon="🎓")

st.title("🎓 College Match Finder")
st.write(
    "Compare a student profile with historical U.S. college admissions data."
)

st.info(
    "This project is an educational matching tool. "
    "It does not predict or guarantee admission."
)

sat_score = st.slider("SAT score", 400, 1600, 1200, 10)
gpa = st.slider("GPA (4.0 scale)", 0.0, 4.0, 3.5, 0.1)
major = st.selectbox(
    "Intended major",
    ["Computer Science", "Engineering", "Business", "Biology", "Undecided"],
)
extracurriculars = st.selectbox(
    "Extracurricular involvement", ["Low", "Moderate", "Strong"]
)
leadership = st.checkbox("Leadership experience")
volunteering = st.checkbox("Volunteer / community service")

if st.button("Find College Matches"):
    colleges = pd.read_csv("data/colleges.csv")

    bonus = profile_bonus(gpa, extracurriculars, leadership, volunteering)

    colleges["Match"] = colleges.apply(
        lambda row: classify_college(
            sat_score,
            row["sat_25"],
            row["sat_75"],
            row["admission_rate"],
        ),
        axis=1,
    )

    order = {"Likely": 1, "Target": 2, "Reach": 3}
    colleges["sort_order"] = colleges["Match"].map(order)
    colleges = colleges.sort_values(["sort_order", "college_name"])

    st.subheader("Your Profile")
    st.write(f"SAT: **{sat_score}** | GPA: **{gpa:.1f}** | Major: **{major}**")
    st.write(f"Supporting profile score: **{bonus}/6**")

    st.subheader("College Matches")

    for _, college in colleges.iterrows():
        st.markdown(f"### {college['college_name']} — {college['Match']}")
        st.write(
            f"{college['city']}, {college['state']} | "
            f"Historical SAT range: {college['sat_25']}–{college['sat_75']} | "
            f"Admission rate: {college['admission_rate']:.0%}"
        )

    st.caption(
        "SAT ranges and admission rates are historical institutional statistics. "
        "Admissions decisions consider many additional factors."
    )
