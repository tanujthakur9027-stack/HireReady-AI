import time
import base64
import streamlit as st

# ==============================
# SERVICES
# ==============================

from services import gemini_service
from services.voice_service import text_to_speech
from services.compiler_service import run_python
from services.coding_service import review_code

# Camera (OpenCV)
try:
    from services.camera_service import VideoProcessor
    CAMERA_AVAILABLE = True
except Exception :
    CAMERA_AVAILABLE = False
from streamlit_webrtc import webrtc_streamer

# ==============================
# UTILS
# ==============================

from utils.resume_parser import extract_resume
from utils.resume_analyzer import analyze_resume
from utils.ats_checker import check_resume
from utils.jd_matcher import match_resume
from utils.question_generator import generate_question
from utils.avatar_service import get_avatar
from utils.session_manager import (
    save_session,
    load_session
)

# ==============================
# MEMORY
# ==============================

from memory.memory_adapter import (
    save_memory,
    load_memory
)

from memory.memory_analyzer import (
    build_memory
)

# ==============================
# REPORTS
# ==============================

from dashboard import show_resume_dashboard
from analytics import show_analytics
import reports.report_generator as report_generator

# ==============================
# EXTRAS
# ==============================

from streamlit_mic_recorder import speech_to_text
from streamlit_ace import st_ace

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(

    page_title="InterviewMate AI",

    page_icon="🎯",

    layout="wide"

)

# ==============================
# SESSION STATE
# ==============================

DEFAULTS = {

    "started": False,

    "name": "",

    "role": "",

    "company": "",

    "resume_text": "",

    "messages": [],

    "question_count": 0,

    "start_time": None,

    "generated_question": ""

}

for k, v in DEFAULTS.items():

    if k not in st.session_state:

        st.session_state[k] = v
        # ==========================================
# HOME PAGE
# ==========================================

if not st.session_state.started:

    st.title("🎯HireReady ")

    st.caption(
        "AI Powered Resume Analyzer & Mock Interview Platform"
    )

    st.divider()

    resume_tab, interview_tab = st.tabs(

        [

            " Resume Intelligence",

            " AI Interview"

        ]

    )

# ===========================================================
# RESUME TAB
# ===========================================================

    with resume_tab:

        st.header(" Resume Intelligence")

        resume = st.file_uploader(

            "Upload Resume",

            type=["pdf"]

        )

        analyze = st.button(

            " Analyze Resume",

            use_container_width=True

        )

        if analyze:

            if resume is None:

                st.warning("Upload Resume First")

            else:

                with st.spinner("Analyzing Resume..."):

                    resume_text = extract_resume(

                        resume

                    )

                    st.session_state.resume_text = resume_text

                    analysis = analyze_resume(

                        resume_text

                    )

                    ats = check_resume(

                        resume_text

                    )

                st.success("Resume Analyzed Successfully")

                st.divider()

                show_resume_dashboard(

                    analysis

                )

                st.divider()

                st.header(" ATS Score")

                st.metric(

                    "ATS",

                    f"{ats['ats_score']}%"

                )

                st.progress(

                    ats["ats_score"]/100

                )

                st.subheader(" Suggestions")

                if "suggestions" in analysis:

                    for tip in analysis["suggestions"]:

                        st.info(

                            tip

                        )

# ===========================================================
# INTERVIEW TAB
# ===========================================================

    with interview_tab:

        st.header(" AI Mock Interview")

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(

                "Your Name"

            )

            role = st.selectbox(

                "Role",

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

                "Company",

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

        interview_resume = st.file_uploader(

            "Resume (Optional)",

            type=["pdf"],

            key="resume2"

        )

        jd = st.text_area(

            "Job Description (Optional)",

            height=180

        )

        voice_mode = st.toggle(

            " Enable Voice"

        )

        camera_mode = st.toggle(

            " Enable Camera"

        )

        coding_round = st.toggle(

            " Coding Round"

        )

        start = st.button(

            " Start Interview",

            use_container_width=True

        )
        # ===========================================================
        # START INTERVIEW
        # ===========================================================

        if start:

            if name.strip() == "":

                st.warning("Please Enter Your Name")

                st.stop()

            resume_text = ""

    if interview_resume is not None:

        resume_text = extract_resume(interview_resume)

    # -----------------------------------
    # Resume vs JD Match
    # -----------------------------------

    if jd.strip() != "" and resume_text != "":

        result = match_resume(
            resume_text,
            jd
        )

        st.divider()

        st.subheader(" Resume vs JD Match")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Match Score",
                f"{result['score']}%"
            )

            st.progress(result["score"] / 100)

        with c2:

            st.write("### Missing Skills")

            if result["missing"]:

                for skill in result["missing"]:

                    st.error(skill)

            else:

                st.success("No Missing Skills")

    # -----------------------------------
    # Load Previous Interview
    # -----------------------------------

    previous = load_session(name)

    memory = load_memory(name)

    if previous:

        st.success(" Previous Interview Found!")

        interview_mode = st.radio(

            "Choose Interview Mode",

            [

                " Continue Previous Interview",

                " Start New Interview"

            ],

            horizontal=True,

            key="interview_mode"

        )

        if st.button("Continue"):

            st.session_state.name = name

            st.session_state.role = role

            st.session_state.company = company

            if interview_resume is not None:
                st.session_state.resume_text = extract_resume(interview_resume)
            else:
                st.session_state.resume_text = ""

            st.session_state.voice_mode = voice_mode

            st.session_state.camera_mode = camera_mode

            st.session_state.coding_round = coding_round

            if interview_mode == " Continue Previous Interview":

                st.session_state.messages = previous.get(

                    "messages",

                    []

                )

                st.session_state.question_count = previous.get(

                    "question_count",

                    0

                )

                st.session_state.start_time = previous.get(

                    "start_time",

                    time.time()

                )

            else:

                st.session_state.messages = []

                st.session_state.question_count = 0

                st.session_state.start_time = time.time()

            save_memory(

                name,

                {

                    "name": name,

                    "role": role,

                    "company": company,

                    "resume": st.session_state.resume_text

                }

            )

            st.session_state.started = True

            st.rerun()

    else:

        st.session_state.name = name

        st.session_state.role = role

        st.session_state.company = company

        if interview_resume is not None:
            st.session_state.resume_text = extract_resume(interview_resume)
        else:
            st.session_state.resume_text = ""

        st.session_state.messages = []

        st.session_state.question_count = 0

        st.session_state.start_time = time.time()

        st.session_state.voice_mode = voice_mode

        st.session_state.camera_mode = camera_mode

        st.session_state.coding_round = coding_round

        save_memory(
            name,
            {
                "name": name,
                "role": role,
                "company": company,
                "resume": st.session_state.resume_text
            }
        )

        st.session_state.started = True

        st.rerun()   

# ===========================================================
# INTERVIEW PAGE
# ===========================================================

else:

    voice_mode = st.session_state.voice_mode

    camera_mode = st.session_state.camera_mode

    coding_round = st.session_state.coding_round

    st.sidebar.title("Interview Controls")

    if st.sidebar.button(" Home"):

        st.session_state.started = False

        st.rerun()

    st.sidebar.write(

        f" {st.session_state.name}"

    )

    st.sidebar.write(

        f" {st.session_state.role}"

    )

    st.sidebar.write(

        f" {st.session_state.company}"

    )

    avatar = get_avatar(

        st.session_state.company

    )

    st.title(

        f"{avatar} {st.session_state.company} Interview"

    )

    elapsed = int(

        time.time()

        -

        st.session_state.start_time

    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Time",

            f"{elapsed//60}:{elapsed%60:02}"

        )

    with c2:

        st.metric(

            "Questions",

            st.session_state.question_count

        )

    with c3:

        st.metric(

            "Progress",

            f"{min(st.session_state.question_count*10,100)}%"

        )

    st.progress(

        min(st.session_state.question_count*10,100)/100

    )

    if camera_mode:

        st.subheader(" Live Camera")

        if CAMERA_AVAILABLE:

            webrtc_streamer(
                key="camera",
                video_processor_factory=VideoProcessor,
                media_stream_constraints={
                    "video": True,
                    "audio": False
                },
                async_processing=True
            )

        else:

            st.warning(" Camera feature is unavailable on this deployment.")

    if len(st.session_state.messages) == 0:

        st.session_state.messages.append(

           {

                "role":"assistant",

                "content":f"""

 Welcome **{st.session_state.name}**

I'm your AI interviewer today.

We'll conduct a realistic interview for

**{st.session_state.role}**

at

**{st.session_state.company}**

Please answer naturally.

Let's begin.

### Tell me about yourself.

"""

           }

        )

    for msg in st.session_state.messages:

        with st.chat_message(

            msg["role"]

        ):

            st.markdown(

                msg["content"]

            )

  # ===========================================================
    # VOICE INPUT
    # ===========================================================

    voice_text = ""

    if voice_mode:

        st.subheader(" Speak")
        st.info(" Click Start Speaking and allow microphone permission.")
        voice_text = speech_to_text(
            language="en",
            start_prompt=" Start Speaking",
            stop_prompt=" Stop",
            just_once=True,
            use_container_width=True,
            key="voice"
        )

    # ===========================================================
    # CHAT INPUT
    # ===========================================================

    prompt = st.chat_input(

        "Type your answer..."

    )

    if voice_text:

        prompt = voice_text

    # ===========================================================
    # AI RESPONSE
    # ===========================================================

    if prompt:

        st.session_state.messages.append(

            {

                "role":"user",

                "content":prompt

            }

        )

        with st.chat_message("user"):

            st.markdown(prompt)

        profile = {

            "name":st.session_state.name,

            "role":st.session_state.role,

            "company":st.session_state.company,

            "resume":st.session_state.resume_text,

            "memory":load_memory(

                st.session_state.name

            )

        }

        with st.spinner(

            " Thinking..."

        ):

            reply = gemini_service.ask_ai(
                prompt,
                profile
            )

        st.session_state.question_count += 1

        st.session_state.messages.append(

            {

                "role":"assistant",

                "content":reply

            }

        )

        with st.chat_message("assistant"):

            st.markdown(reply)

        # =====================================
        # Voice Output
        # =====================================

        if voice_mode:

            audio = text_to_speech(reply)

            if audio:

                st.audio(

                    base64.b64decode(audio),

                    format="audio/mp3",

                    autoplay=True

                )   
                

        # =====================================
        # Save Session
        # =====================================

        save_session(
            st.session_state.name,
            {
                "messages": st.session_state.messages,
                "question_count": st.session_state.question_count,
                "start_time": st.session_state.start_time,
                "company": st.session_state.company,
                "role": st.session_state.role,
                "resume": st.session_state.resume_text
            }
        )

        memory = build_memory(
            st.session_state.messages
        )

        save_memory(
            st.session_state.name,
            memory
        )

    # ===========================================================
    # CODING ROUND
    # ===========================================================

    if coding_round:

        st.divider()

        st.header(" Coding Round")

        difficulty = st.selectbox(

            "Difficulty",

            [

                "Easy",

                "Medium",

                "Hard"

            ]

        )

        if st.button(

            " Generate Question",

            use_container_width=True

        ):

            st.session_state.generated_question = generate_question(

                st.session_state.role,

                st.session_state.company,

                difficulty

            )

        if st.session_state.generated_question != "":

            st.subheader(

                "Coding Question"

            )

            st.info(

                st.session_state.generated_question

            )

            code = st_ace(

                language="python",

                theme="monokai",

                height=400,

                key="editor"

            )

            c1, c2 = st.columns(2)

            with c1:

                if st.button(

                    " Run",

                    use_container_width=True

                ):

                    success, output = run_python(

                        code

                    )

                    if success:

                        st.success(

                            "Executed Successfully"

                        )

                        st.code(

                            output

                        )

                    else:

                        st.error(

                            output

                        )

            with c2:

                if st.button(

                    " Submit",

                    use_container_width=True

                ):

                    if code.strip() == "":

                        st.warning(

                            "Write some code first."

                        )

                    else:

                        review = review_code(

                            st.session_state.generated_question,

                            code

                        )

                        st.success(

                            "AI Review"

                        )

                        st.markdown(

                            review

                        )

    # ===========================================================
    # ANALYTICS
    # ===========================================================

    st.divider()

    st.header(

        " Interview Analytics"

    )

    memory = load_memory(

        st.session_state.name

    )

    if memory:

        show_analytics(

            memory

        )

    else:

        st.info(

            "No Analytics Available Yet"

        )

    # ===========================================================
    # REPORT
    # ===========================================================

    st.divider()

    if st.button(

        " Generate Interview Report",

        use_container_width=True

    ):

        report_generator.generate_report(

            memory,

            "Interview_Report.pdf"

        )

        with open(

            "Interview_Report.pdf",

            "rb"

        ) as f:

            st.download_button(

                "⬇ Download Report",

                data=f,

                file_name="Interview_Report.pdf",

                mime="application/pdf",

                use_container_width=True

            )

    st.divider()

    st.caption(

        " InterviewMate AI | Powered by Gemini + Streamlit"

    )