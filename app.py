import csv

import streamlit as st

from matcher import classify_college, profile_bonus


st.set_page_config(
    page_title="College Match Finder",
    page_icon="🎓",
    layout="wide",
)

# Keep the page compact while leaving Streamlit controls native and easy to understand.
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.4rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1400px;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.4rem;
        }

        h1 {
            margin-top: 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎓 College Match Finder")
st.write("Compare a student profile with historical U.S. college admissions data.")

st.info(
    "This project is an educational matching tool. "
    "It does not predict or guarantee admission."
)

with st.sidebar:
    st.header("Student Profile")
    st.write("Enter your academic and activity details.")

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

    find_matches = st.button("Find College Matches", use_container_width=True)

if find_matches:
    colleges = []

    with open("data/colleges.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if major != "Undecided":
                offered_majors = row["majors"].split(";")
                if major not in offered_majors:
                    continue

            row["sat_25"] = int(row["sat_25"])
            row["sat_75"] = int(row["sat_75"])
            row["admission_rate"] = float(row["admission_rate"])

            row["Match"] = classify_college(
                sat_score,
                gpa,
                row["sat_25"],
                row["sat_75"],
                row["admission_rate"],
            )
            colleges.append(row)

    bonus = profile_bonus(gpa, extracurriculars, leadership, volunteering)

    order = {"Likely": 1, "Target": 2, "Reach": 3}
    colleges.sort(key=lambda college: (order[college["Match"]], college["college_name"]))

    recommended = [
        college for college in colleges if college["Match"] in ("Likely", "Target")
    ]
    reach_schools = [college for college in colleges if college["Match"] == "Reach"]

    likely_count = sum(1 for college in recommended if college["Match"] == "Likely")
    target_count = sum(1 for college in recommended if college["Match"] == "Target")

    st.subheader("Your Profile")
    st.write(f"SAT: **{sat_score}** | GPA: **{gpa:.1f}** | Major: **{major}**")
    st.write(f"Supporting profile score: **{bonus}/6**")

    st.subheader("Recommended Matches")
    total_col, likely_col, target_col = st.columns(3)
    total_col.metric("Total Matches", len(recommended))
    likely_col.metric("Likely", likely_count)
    target_col.metric("Target", target_count)

    if recommended:
        table_data = []

        for college in recommended:
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
    else:
        st.warning(
            "No Likely or Target matches were found for this profile in the starter dataset."
        )

    if recommended:
        with st.expander(f"Reach Schools ({len(reach_schools)})"):
            if reach_schools:
                reach_data = []

                for college in reach_schools:
                    reach_data.append(
                        {
                            "College": college["college_name"],
                            "State": college["state"],
                            "SAT Range": f"{college['sat_25']}–{college['sat_75']}",
                            "Admission Rate": f"{college['admission_rate']:.0%}",
                        }
                    )

                st.dataframe(reach_data, use_container_width=True, hide_index=True)

    st.caption(
        "These are educational profile matches based on simplified rules and "
        "historical institutional statistics, not admission predictions."
    )
