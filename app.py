import csv

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
    colleges = []

    with open("data/colleges.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["sat_25"] = int(row["sat_25"])
            row["sat_75"] = int(row["sat_75"])
            row["admission_rate"] = float(row["admission_rate"])

            row["Match"] = classify_college(
                sat_score,
                row["sat_25"],
                row["sat_75"],
                row["admission_rate"],
            )
            colleges.append(row)

    bonus = profile_bonus(gpa, extracurriculars, leadership, volunteering)

    order = {"Likely": 1, "Target": 2, "Reach": 3}
    colleges.sort(key=lambda college: (order[college["Match"]], college["college_name"]))

    st.subheader("Your Profile")
    st.write(f"SAT: **{sat_score}** | GPA: **{gpa:.1f}** | Major: **{major}**")
    st.write(f"Supporting profile score: **{bonus}/6**")

    st.subheader("College Matches")

    likely_count = sum(1 for college in colleges if college["Match"] == "Likely")
    target_count = sum(1 for college in colleges if college["Match"] == "Target")
    reach_count = sum(1 for college in colleges if college["Match"] == "Reach")

    total_col, likely_col, target_col, reach_col = st.columns(4)
    total_col.metric("Total Colleges", len(colleges))
    likely_col.metric("Likely", likely_count)
    target_col.metric("Target", target_count)
    reach_col.metric("Reach", reach_count)

    table_data = []

    for college in colleges:
        table_data.append(
            {
                "College": college["college_name"],
                "State": college["state"],
                "SAT Range": f"{college['sat_25']}–{college['sat_75']}",
                "Admission Rate": f"{college['admission_rate']:.0%}",
                "Match": college["Match"],
            }
        )

    st.dataframe(table_data, use_container_width=True, hide_index=True)

    st.caption(
        "SAT ranges and admission rates are historical institutional statistics. "
        "Admissions decisions consider many additional factors."
    )
