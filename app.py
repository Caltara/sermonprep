import streamlit as st
from generators.sermon_generator import generate_sermon
from generators.study_generator import generate_bible_study
from generators.outline_generator import generate_teaching_outline

st.set_page_config(page_title="AI Sermon Assistant", layout="centered")

# ✅ Check for logged-in user
if not st.experimental_user:
    st.warning("🔒 Please log in to use the AI Sermon Assistant.")
    st.stop()

user_email = st.experimental_user["email"]  # capture email for future saved sermons

st.title("📖✍️ AI Sermon Assistant for Pastors")
st.caption(f"👤 Logged in as: {user_email}")

tab1, tab2, tab3 = st.tabs(["Sermon Generator", "Bible Study", "Teaching Outline"])

with tab1:
    st.header("✝️ Sermon Generator")
    title = st.text_input("Sermon Title")
    summary = st.text_area("Sermon Summary or Theme")
    if st.button("Generate Sermon"):
        if title and summary:
            with st.spinner("Preparing sermon..."):
                sermon = generate_sermon(title, summary)
                st.markdown(sermon)
        else:
            st.warning("Please enter a title and summary.")

with tab2:
    st.header("📖 Bible Study Creator")
    topic = st.text_input("Study Topic")
    notes = st.text_area("Short Description or Summary")
    if st.button("Generate Bible Study"):
        if topic and notes:
            with st.spinner("Creating study..."):
                study = generate_bible_study(topic, notes)
                st.markdown(study)
        else:
            st.warning("Please enter a topic and summary.")

with tab3:
    st.header("🧠 Teaching Outline Builder")
    subject = st.text_input("Outline Subject")
    idea = st.text_area("Brief Concept or Theme")
    if st.button("Generate Outline"):
        if subject and idea:
            with st.spinner("Building outline..."):
                outline = generate_teaching_outline(subject, idea)
                st.markdown(outline)
        else:
            st.warning("Please enter a subject and idea.")
