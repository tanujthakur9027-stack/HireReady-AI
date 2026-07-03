import streamlit as st
from gemini_service import ask_ai
from resume_parser import extract_resume
from session_manager import load_session, save_session

# ---------------- Page ---------------- #

st.set_page_config(
    page_title="InterviewMate AI",
    page_icon="🎯",
    layout="wide"
)

# ---------------- Session Defaults ---------------- #

defaults = {
    "started": False,
    "name": "",
    "role": "",
    "company": "",
    "resume": None,
    "resume_text": "",
    "messages": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ===================================================
# HOME PAGE
# ===================================================

if not st.session_state.started:

    st.title("🎯 InterviewMate AI")
    st.subheader("The AI Interview Coach That Never Forgets")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("👤 Your Name")

        role = st.selectbox(
            "💼 Target Role",
            [
                "AI/ML Engineer",
                "Frontend Developer",
                "Backend Developer",
                "Full Stack Developer",
                "Data Scientist",
                "Cyber Security",
                "DevOps Engineer"
            ]
        )

    with col2:

        company = st.selectbox(
            "🏢 Target Company",
            [
                "Google",
                "Microsoft",
                "Amazon",
                "Meta",
                "OpenAI",
                "Infosys",
                "TCS",
                "Startup"
            ]
        )

        resume = st.file_uploader(
            "📄 Upload Resume",
            type=["pdf"]
        )

    resume_text = ""

    if resume is not None:

        resume_text = extract_resume(resume)

        st.success("✅ Resume Uploaded Successfully")

    st.divider()

    if st.button("🚀 Start Interview", use_container_width=True):

        if name.strip() == "":
            st.warning("Please enter your name.")
            st.stop()

        previous_session = load_session(name)

        st.session_state.name = name
        st.session_state.role = role
        st.session_state.company = company
        st.session_state.resume = resume

        if previous_session:

            st.info("✅ Previous interview found. Restoring session...")

            st.session_state.messages = previous_session.get("messages", [])

            st.session_state.resume_text = previous_session.get(
                "resume",
                resume_text
            )

        else:

            st.session_state.messages = []

            st.session_state.resume_text = resume_text

        st.session_state.started = True

        st.rerun()

# ===================================================
# INTERVIEW PAGE
# ===================================================

else:

    st.sidebar.title("👤 Candidate")

    st.sidebar.write(f"**Name:** {st.session_state.name}")
    st.sidebar.write(f"**Role:** {st.session_state.role}")
    st.sidebar.write(f"**Company:** {st.session_state.company}")

    if st.sidebar.button("🏠 Home"):

        st.session_state.started = False

        st.rerun()

    st.title("🎤 AI Mock Interview")

    # First Question

    if len(st.session_state.messages) == 0:

        intro = f"""
Welcome **{st.session_state.name}** 👋

Today we'll conduct a mock interview for the position of

**{st.session_state.role}**

at

**{st.session_state.company}**

Let's begin.

### Tell me about yourself.
"""

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": intro
            }
        )

    # Display Chat

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

    # User Input

    prompt = st.chat_input("Type your answer...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        profile = {

            "name": st.session_state.name,

            "role": st.session_state.role,

            "company": st.session_state.company,

            "resume": st.session_state.resume_text

        }

        with st.spinner("Interviewer is thinking..."):

            reply = ask_ai(prompt, profile)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        with st.chat_message("assistant"):

            st.markdown(reply)

        # Save Session

        save_session(

            st.session_state.name,

            {

                "name": st.session_state.name,

                "role": st.session_state.role,

                "company": st.session_state.company,

                "resume": st.session_state.resume_text,

                "messages": st.session_state.messages

            }

        )