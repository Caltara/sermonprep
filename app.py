import streamlit as st
from generators.sermon_generator import generate_sermon
from generators.study_generator import generate_bible_study
from generators.outline_generator import generate_teaching_outline
from generators.series_generator import generate_sermon_series
from utils.export import export_to_pdf, export_to_docx

# ---------------- LOGIN ----------------

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.set_page_config(page_title="AI Sermon Assistant Login", layout="centered")
    st.title("🔐 AI Sermon Assistant Login")
    st.write("Please log in to access the sermon tools.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email == st.secrets["USER_EMAIL"] and password == st.secrets["USER_PASSWORD"]:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.success("✅ Login successful! Please rerun the app using the 🔁 button.")
        else:
            st.error("❌ Invalid email or password.")
        st.stop()

    st.stop()

if not check_password():
    st.stop()

# ---------------- MAIN APP ----------------

st.set_page_config(page_title="AI Sermon Assistant", layout="centered")
st.title("📖✍️ AI Sermon Assistant for Pastors")
st.caption("Generate sermons, outlines, Bible studies, and sermon series with AI ✝️")

tab1, tab2, tab3, tab4 = st.tabs([
    "Sermon Generator",
    "Bible Study",
    "Teaching Outline",
    "Sermon Series Planner"
])

# ----------- TAB 1: SERMON GENERATOR -----------

with tab1:
    st.header("✝️ Sermon Generator")
    title = st.text_input("Sermon Title")
    summary = st.text_area("Sermon Summary or Theme")
    if st.button("Generate Sermon"):
        if title and summary:
            with st.spinner("Preparing sermon..."):
                sermon = generate_sermon(title, summary)
                st.markdown(sermon)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("⬇️ Export as PDF", export_to_pdf(title, sermon), file_name=f"{title}.pdf")
                with col2:
                    st.download_button("⬇️ Export as Word (.docx)", export_to_docx(title, sermon), file_name=f"{title}.docx")
        else:
            st.warning("Please enter a title and summary.")

# ----------- TAB 2: BIBLE STUDY -----------

with tab2:
    st.header("📖 Bible Study Creator")
    topic = st.text_input("Study Topic")
    notes = st.text_area("Short Description or Summary")
    if st.button("Generate Bible Study"):
        if topic and notes:
            with st.spinner("Creating study..."):
                study = generate_bible_study(topic, notes)
                st.markdown(study)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("⬇️ Export as PDF", export_to_pdf(topic, study), file_name=f"{topic}.pdf")
                with col2:
                    st.download_button("⬇️ Export as Word (.docx)", export_to_docx(topic, study), file_name=f"{topic}.docx")
        else:
            st.warning("Please enter a topic and summary.")

# ----------- TAB 3: TEACHING OUTLINE -----------

with tab3:
    st.header("🧠 Teaching Outline Builder")
    subject = st.text_input("Outline Subject")
    idea = st.text_area("Brief Concept or Theme")
    if st.button("Generate Outline"):
        if subject and idea:
            with st.spinner("Building outline..."):
                outline = generate_teaching_outline(subject, idea)
                st.markdown(outline)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("⬇️ Export as PDF", export_to_pdf(subject, outline), file_name=f"{subject}.pdf")
                with col2:
                    st.download_button("⬇️ Export as Word (.docx)", export_to_docx(subject, outline), file_name=f"{subject}.docx")
        else:
            st.warning("Please enter a subject and idea.")

# ----------- TAB 4: SERMON SERIES PLANNER -----------

with tab4:
    st.header("📅 Sermon Series Planner")
    series_theme = st.text_input("Enter Series Theme or Title")
    weeks = st.slider("Number of Weeks", min_value=3, max_value=8, value=5)
    if st.button("Generate Series"):
        if series_theme:
            with st.spinner("Creating sermon series..."):
                series_plan = generate_sermon_series(series_theme, weeks)

                for sermon in series_plan:
                    week_num = sermon.get("week", "?")
                    title = sermon.get("title", "No Title")
                    summary = sermon.get("summary", "No Summary")
                    verses = sermon.get("verses", [])

                    st.markdown(f"### ✅ Week {week_num}: {title}")
                    st.markdown(f"**Summary:** {summary}")

                    if verses:
                        st.markdown("**Bible Verses:**")
                        for verse in verses:
                            st.markdown(f"- {verse}")

                    st.markdown("---")
        else:
            st.warning("Please enter a series theme.")
