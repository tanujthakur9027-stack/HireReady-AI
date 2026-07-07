import time
import base64
import os
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
except Exception:
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
from utils.session_manager import save_session, load_session
from utils.auth_service import register_user, login_user, db_init

# ==============================
# MEMORY
# ==============================
from memory.memory_adapter import save_memory, load_memory
from memory.memory_analyzer import build_memory
from memory import cognee_adapter

# ==============================
# REPORTS & DASHBOARDS
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
    page_title="HireReady-AI",
    page_icon="🎯",
    layout="wide"
)

# Ingest Custom CSS
try:
    with open("ui/style.css", "r") as f:
        custom_css = f.read()
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)
except Exception:
    pass

# Initialize Authentication DB
db_init()

# ==============================
# SESSION STATE DEFAULTS
# ==============================
DEFAULTS = {
    "authenticated": False,
    "user_data": None,
    "started": False,
    "name": "",
    "role": "AI/ML Engineer",
    "company": "Google",
    "resume_text": "",
    "messages": [],
    "question_count": 0,
    "start_time": None,
    "generated_question": "",
    "voice_mode": False,
    "camera_mode": False,
    "coding_round": False,
    "duration": 5,
    "active_step": "setup",        # "setup", "interview", "evaluation"
    "evaluation_result": None,
    "code_review_result": None,
    "resume_analysis": None,
    "ats_result": None,
    "jd_match_result": None
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Reset Helper
def reset_session():
    st.session_state.started = False
    st.session_state.messages = []
    st.session_state.question_count = 0
    st.session_state.start_time = None
    st.session_state.generated_question = ""
    st.session_state.voice_mode = False
    st.session_state.camera_mode = False
    st.session_state.coding_round = False
    st.session_state.duration = 5
    st.session_state.active_step = "setup"
    st.session_state.evaluation_result = None
    st.session_state.code_review_result = None
    st.session_state.resume_analysis = None
    st.session_state.ats_result = None
    st.session_state.jd_match_result = None
    gemini_service.reset_chat()

# ==========================================
# AUTHENTICATION SCREEN
# ==========================================
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-header' style='text-align:center;'>🎯 HireReady-AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header' style='text-align:center;'>Industry-Level AI Career Prep Workspace & Interactive Mock Interview Portal</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_tab1, auth_tab2 = st.tabs(["🔐 Sign In", "📝 Sign Up"])
        
        with auth_tab1:
            st.markdown("<h3>Welcome Back!</h3>", unsafe_allow_html=True)
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            login_btn = st.button("Sign In", use_container_width=True, type="primary")
            
            if login_btn:
                user = login_user(email, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user
                    st.session_state.name = user["name"]
                    st.success(f"Welcome back, {user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
                    
        with auth_tab2:
            st.markdown("<h3>Create Account</h3>", unsafe_allow_html=True)
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_pwd")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            register_btn = st.button("Sign Up", use_container_width=True)
            
            if register_btn:
                if reg_password != reg_confirm:
                    st.error("Passwords do not match.")
                else:
                    success, msg = register_user(reg_name, reg_email, reg_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
    st.stop()

# ==========================================
# SETUP / HOME PAGE (AUTHENTICATED)
# ==========================================
if st.session_state.active_step == "setup":

    st.markdown("<h1 class='main-header'>🎯 HireReady-AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-header'>Logged in as <b>{st.session_state.name}</b> • Personalized AI Graph Memory Enabled</p>", unsafe_allow_html=True)

    # Sidebar Logout & Profile Details
    st.sidebar.markdown("<div class='sidebar-title'>User Profile</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div class="sidebar-profile">
        <strong>👤 {st.session_state.name}</strong><br/>
        <span style="color:#94A3B8; font-size:0.85rem;">✉ {st.session_state.user_data['email']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🔓 Sign Out", use_container_width=True):
        reset_session()
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.rerun()

    resume_tab, interview_tab = st.tabs(
        [
            "📄 Resume Intelligence",
            "🤝 AI Mock Interview"
        ]
    )

    # -----------------------------------------------------------
    # RESUME TAB
    # -----------------------------------------------------------
    with resume_tab:
        st.markdown("<h3 class='section-title'>Analyze Resume ATS & Performance</h3>", unsafe_allow_html=True)
        
        resume = st.file_uploader(
            "Upload Resume (PDF format)",
            type=["pdf"],
            key="resume_uploader"
        )

        analyze = st.button(
            "⚡ Run Resume Intelligence",
            use_container_width=True
        )

        if analyze:
            if resume is None:
                st.warning("Please upload a resume first.")
            else:
                with st.spinner("Analyzing resume formatting, structure, and keywords..."):
                    resume_text = extract_resume(resume)
                    st.session_state.resume_text = resume_text
                    st.session_state.resume_analysis = analyze_resume(resume_text)
                    st.session_state.ats_result = check_resume(resume_text)
                st.success("Analysis complete!")
        
        # Display Dashboard if analysis exists
        if st.session_state.resume_analysis is not None:
            show_resume_dashboard(st.session_state.resume_analysis)
            
            if st.session_state.ats_result:
                ats = st.session_state.ats_result
                st.markdown("<h2 class='section-title'>⚙ ATS Parsing Details</h2>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("<h4>Heading Checklist</h4>", unsafe_allow_html=True)
                    checklist = ats.get("checklist", {})
                    for key, val in checklist.items():
                        if val:
                            st.markdown(f"✔ <span style='color:#10B981;'>{key} Detected</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"❌ <span style='color:#EF4444;'>Missing {key}</span>", unsafe_allow_html=True)
                with col2:
                    st.markdown("<h4>ATS Readability & Layout Feedback</h4>", unsafe_allow_html=True)
                    for feedback in ats.get("formatting_feedback", []):
                        st.info(feedback)
                    
                    st.markdown("<h4>Extracted Keywords</h4>", unsafe_allow_html=True)
                    skills_html = "".join(f"<div class='topic-badge'>{skill}</div>" for skill in ats.get("skills", []))
                    st.markdown(f"<div style='display:flex; flex-wrap:wrap; gap:0.4rem;'>{skills_html}</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------
    # INTERVIEW TAB
    # -----------------------------------------------------------
    with interview_tab:
        st.markdown("<h3 class='section-title'>Configure AI Mock Session</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Candidate Name", value=st.session_state.name, disabled=True)
            role = st.selectbox(
                "Target Role",
                [
                    "AI/ML Engineer",
                    "Frontend Developer",
                    "Backend Developer",
                    "Full Stack Developer",
                    "Data Scientist",
                    "Cyber Security",
                    "DevOps Engineer"
                ],
                index=0
            )
            duration = st.slider(
                "Interview Length (Number of questions)",
                min_value=3,
                max_value=10,
                value=5
            )

        with col2:
            company = st.selectbox(
                "Target Company",
                [
                    "Google",
                    "Microsoft",
                    "Amazon",
                    "Meta",
                    "OpenAI",
                    "Infosys",
                    "TCS",
                    "Startup"
                ],
                index=0
            )
            interview_resume = st.file_uploader(
                "Customize with Resume (Optional)",
                type=["pdf"],
                key="resume_int_uploader"
            )
            jd = st.text_area(
                "Job Description (Optional for JD-alignment questions)",
                height=110
            )

        st.markdown("<h4>Session Integration Features</h4>", unsafe_allow_html=True)
        feat_c1, feat_c2, feat_c3 = st.columns(3)
        with feat_c1:
            voice_mode = st.toggle("🗣 Enable Voice Mode (TTS / Audio output)", value=st.session_state.voice_mode)
        with feat_c2:
            camera_mode = st.toggle("📷 Enable Live Camera Feed", value=st.session_state.camera_mode)
        with feat_c3:
            coding_round = st.toggle("💻 Integrate Coding Round workspace", value=st.session_state.coding_round)

        start = st.button(
            "🚀 Initialize & Start Session",
            use_container_width=True
        )

        if start:
            resume_text = st.session_state.resume_text
            if interview_resume is not None:
                resume_text = extract_resume(interview_resume)

            # -----------------------------------
            # Resume vs JD Match
            # -----------------------------------
            if jd.strip() != "" and resume_text != "":
                with st.spinner("Analyzing resume alignment with Job Description..."):
                    jd_match = match_resume(resume_text, jd)
                    st.session_state.jd_match_result = jd_match
            
            # Setup State Variables
            st.session_state.role = role
            st.session_state.company = company
            st.session_state.resume_text = resume_text
            st.session_state.voice_mode = voice_mode
            st.session_state.camera_mode = camera_mode
            st.session_state.coding_round = coding_round
            st.session_state.duration = duration
            
            # Search Cognee Graph Memory for candidate history
            with st.spinner("Retrieving historical interview memory graph..."):
                search_query = f"What are the weaknesses, mistakes, and strong topics of candidate {st.session_state.name} in mock interviews?"
                graph_history = cognee_adapter.search(search_query)
                st.session_state.graph_history = graph_history

            # Check for previous session
            previous = load_session(st.session_state.name)
            if previous:
                st.session_state.messages = previous.get("messages", [])
                st.session_state.question_count = previous.get("question_count", 0)
                st.session_state.start_time = previous.get("start_time", time.time())
                st.session_state.duration = previous.get("duration", duration)
            else:
                st.session_state.messages = []
                st.session_state.question_count = 0
                st.session_state.start_time = time.time()

            save_memory(
                st.session_state.name,
                {
                    "name": st.session_state.name,
                    "role": role,
                    "company": company,
                    "resume": resume_text
                }
            )

            # Reset chat session in Gemini
            gemini_service.reset_chat()

            st.session_state.started = True
            st.session_state.active_step = "interview"
            st.rerun()

        # Display JD Match if computed
        if st.session_state.jd_match_result:
            result = st.session_state.jd_match_result
            st.markdown("<h2 class='section-title'>🎯 Job Description Match analysis</h2>", unsafe_allow_html=True)
            
            col_left, col_right = st.columns([1, 2])
            with col_left:
                st.markdown(f"""
                <div class="premium-card metric-card" style="border-top-color: #10B981; text-align: center;">
                    <p style="color:#94A3B8; margin-bottom:5px;">Role Compatibility</p>
                    <h1 style="color:#FFFFFF; margin:0;">{result.get('score', 0)}%</h1>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<h4>Missing Required Skills</h4>")
                if result.get("missing"):
                    for skill in result["missing"]:
                        st.markdown(f"<span style='color:#EF4444;'>✘ {skill}</span>", unsafe_allow_html=True)
                else:
                    st.success("Perfect skill matches!")
            
            with col_right:
                st.markdown("<h4>Semantic Fit Assessment</h4>")
                st.info(result.get("alignment_summary", ""))
                
                c_s, c_g = st.columns(2)
                with c_s:
                    st.markdown("<h5>Direct Strengths</h5>")
                    for s in result.get("strengths_for_role", []):
                        st.markdown(f"✔ <span style='font-size:0.9rem;'>{s}</span>", unsafe_allow_html=True)
                with c_g:
                    st.markdown("<h5>Identified Gaps</h5>")
                    for g in result.get("gaps_for_role", []):
                        st.markdown(f"⚠ <span style='font-size:0.9rem; color:#F59E0B;'>{g}</span>", unsafe_allow_html=True)

# ==========================================
# ACTIVE INTERVIEW STAGE
# ==========================================
elif st.session_state.active_step == "interview":

    voice_mode = st.session_state.voice_mode
    camera_mode = st.session_state.camera_mode
    coding_round = st.session_state.coding_round
    duration = st.session_state.duration

    # Sidebar Panel
    st.sidebar.markdown("<div class='sidebar-title'>HireReady-AI Controls</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <div class="sidebar-profile">
        <strong style="color:#6366F1; font-size:1.1rem;">Candidate details</strong><br/>
        <span style="color:#E2E8F0; font-size:0.9rem;">👤 {st.session_state.name}</span><br/>
        <span style="color:#E2E8F0; font-size:0.9rem;">💼 {st.session_state.role}</span><br/>
        <span style="color:#E2E8F0; font-size:0.9rem;">🏢 {st.session_state.company}</span>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🏠 Quit & Exit to Home", use_container_width=True):
        reset_session()
        st.rerun()

    # Time tracking
    elapsed = int(time.time() - st.session_state.start_time)
    min_progress = int((st.session_state.question_count / duration) * 100)
    
    st.sidebar.markdown("<h4>Session Metrics</h4>", unsafe_allow_html=True)
    st.sidebar.write(f"⏱ Time Elapsed: {elapsed//60}:{elapsed%60:02}")
    st.sidebar.write(f"📝 Question Tracker: {st.session_state.question_count} / {duration}")
    st.sidebar.progress(min(min_progress, 100) / 100)

    # Force Completion Button
    if st.session_state.question_count > 0:
        if st.sidebar.button("🛑 Complete & Evaluate Now", type="primary", use_container_width=True):
            with st.spinner("Compiling transcript and generating custom scorecard..."):
                evaluation = build_memory(st.session_state.messages)
                st.session_state.evaluation_result = evaluation
                save_memory(st.session_state.name, evaluation)
                
                # Save to Cognee graph memory
                summary_text = f"""
                Candidate {st.session_state.name} completed a mock interview for {st.session_state.role} at {st.session_state.company}.
                Technical Score was {evaluation.get('technical_score', 0)}%, Communication was {evaluation.get('communication_score', 0)}%.
                Demonstrated strong topics: {', '.join(evaluation.get('strong_topics', []))}.
                Demonstrated weak topics: {', '.join(evaluation.get('weak_topics', []))}.
                Specific mistakes: {', '.join(evaluation.get('mistakes', []))}.
                Recommended study areas: {', '.join(evaluation.get('recommended_topics', []))}.
                """
                cognee_adapter.save(summary_text)

                st.session_state.active_step = "evaluation"
                st.rerun()

    # Top layout banner
    avatar = get_avatar(st.session_state.company)
    st.markdown(f"<h2>{avatar} {st.session_state.company} Interview Session</h2>", unsafe_allow_html=True)
    
    # -----------------------------------------------------------
    # TABS STRUCTURE FOR CHAT & CODING WORKSPACE
    # -----------------------------------------------------------
    if coding_round:
        chat_tab, coding_tab = st.tabs(["💬 Interview Chat Room", "💻 Code Workspace IDE"])
    else:
        chat_tab = st.container()

    # -----------------------------------------------------------
    # CHAT SECTION
    # -----------------------------------------------------------
    with chat_tab:
        col_chat, col_cam = st.columns([3, 1])
        
        with col_cam:
            if camera_mode:
                st.markdown("<h5>📷 Mock Webcam</h5>", unsafe_allow_html=True)
                if CAMERA_AVAILABLE:
                    webrtc_streamer(
                        key="camera",
                        video_processor_factory=VideoProcessor,
                        media_stream_constraints={"video": True, "audio": False},
                        async_processing=True
                    )
                else:
                    st.warning("Webcam integration unavailable in this environment.")

        with col_chat:
            # Init first message
            if len(st.session_state.messages) == 0:
                welcome_text = f"""Welcome **{st.session_state.name}**. I'm your AI interviewer today.
We'll conduct a realistic mock interview for **{st.session_state.role}** at **{st.session_state.company}**.
Please answer naturally. Let's begin.

### Tell me about yourself and your background."""
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": welcome_text
                })

            # Render Chat bubble history
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            # Voice Input
            voice_text = ""
            if voice_mode:
                st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
                voice_text = speech_to_text(
                    language="en",
                    start_prompt="🎙 Start Speaking",
                    stop_prompt="🛑 Stop Speaking",
                    just_once=True,
                    use_container_width=True,
                    key="voice_input"
                )

            # Chat Input
            prompt = st.chat_input("Type your answer here...")
            if voice_text:
                prompt = voice_text

            # Response processing
            if prompt:
                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt
                })
                st.rerun()

    # Outside the chat render loops to avoid state re-render problems
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Interviewer is evaluating and formulating question..."):
            # Gather profile context, including previous Cognee graph history
            profile = {
                "name": st.session_state.name,
                "role": st.session_state.role,
                "company": st.session_state.company,
                "resume": st.session_state.resume_text,
                "memory": load_memory(st.session_state.name),
                "knowledge": st.session_state.get("graph_history", "")
            }
            
            st.session_state.question_count += 1
            
            if st.session_state.question_count >= duration:
                # Conclude
                conclusion_text = f"Thank you, **{st.session_state.name}**. That concludes our mock interview. I've gathered enough details to build your scorecard. Please click the button below to compile and view your performance feedback."
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": conclusion_text
                })
                
                save_session(st.session_state.name, {
                    "messages": st.session_state.messages,
                    "question_count": st.session_state.question_count,
                    "start_time": st.session_state.start_time,
                    "company": st.session_state.company,
                    "role": st.session_state.role,
                    "resume": st.session_state.resume_text,
                    "duration": duration
                })
                st.rerun()
            else:
                reply = gemini_service.ask_ai(st.session_state.messages[-1]["content"], profile)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })
                
                if voice_mode:
                    audio = text_to_speech(reply)
                    if audio:
                        st.audio(base64.b64decode(audio), format="audio/mp3", autoplay=True)

                save_session(st.session_state.name, {
                    "messages": st.session_state.messages,
                    "question_count": st.session_state.question_count,
                    "start_time": st.session_state.start_time,
                    "company": st.session_state.company,
                    "role": st.session_state.role,
                    "resume": st.session_state.resume_text,
                    "duration": duration
                })
                st.rerun()

    # Conclusion Trigger Panel
    if st.session_state.question_count >= duration:
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
        with col_c2:
            if st.button("📊 Compile Performance Evaluation", type="primary", use_container_width=True):
                with st.spinner("Generating deep AI evaluation & scorecard..."):
                    evaluation = build_memory(st.session_state.messages)
                    st.session_state.evaluation_result = evaluation
                    save_memory(st.session_state.name, evaluation)
                    
                    # Save summary to Cognee graph memory
                    summary_text = f"""
                    Candidate {st.session_state.name} completed a mock interview for {st.session_state.role} at {st.session_state.company}.
                    Technical Score was {evaluation.get('technical_score', 0)}%, Communication was {evaluation.get('communication_score', 0)}%.
                    Demonstrated strong topics: {', '.join(evaluation.get('strong_topics', []))}.
                    Demonstrated weak topics: {', '.join(evaluation.get('weak_topics', []))}.
                    Specific mistakes: {', '.join(evaluation.get('mistakes', []))}.
                    Recommended study areas: {', '.join(evaluation.get('recommended_topics', []))}.
                    """
                    cognee_adapter.save(summary_text)

                    st.session_state.active_step = "evaluation"
                    st.rerun()

    # -----------------------------------------------------------
    # CODING IDE WORKSPACE
    # -----------------------------------------------------------
    if coding_round:
        with coding_tab:
            st.markdown("<h3 class='section-title'>Coding Practice Board</h3>", unsafe_allow_html=True)
            
            c_col1, c_col2 = st.columns([2, 3])
            
            with c_col1:
                difficulty = st.selectbox(
                    "Select Problem Difficulty",
                    ["Easy", "Medium", "Hard"]
                )
                
                if st.button("🆕 Generate Coding Question", use_container_width=True):
                    with st.spinner("Generating coding challenges matching your target company & role..."):
                        st.session_state.generated_question = generate_question(
                            st.session_state.role,
                            st.session_state.company,
                            difficulty
                        )
                        st.session_state.code_review_result = None
                
                if st.session_state.generated_question:
                    st.markdown("<div class='premium-card' style='max-height: 480px; overflow-y: auto;'>", unsafe_allow_html=True)
                    st.write(st.session_state.generated_question)
                    st.markdown("</div>", unsafe_allow_html=True)

            with c_col2:
                st.markdown("<h5>Write Code (Python)</h5>", unsafe_allow_html=True)
                code = st_ace(
                    language="python",
                    theme="monokai",
                    height=350,
                    key="editor_ace"
                )

                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    if st.button("▶ Run Python Code", use_container_width=True):
                        success, output = run_python(code)
                        st.markdown("<h5>Console Output</h5>", unsafe_allow_html=True)
                        if success:
                            st.markdown(f"<div class='terminal-console terminal-success'>{output}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='terminal-console terminal-error'>{output}</div>", unsafe_allow_html=True)
                with btn_c2:
                    if st.button("🚀 Submit to AI Reviewer", use_container_width=True):
                        if code.strip() == "":
                            st.warning("Please write some code before submitting.")
                        elif not st.session_state.generated_question:
                            st.warning("Please generate a coding question first.")
                        else:
                            with st.spinner("AI is evaluating your code, checking complexity and bugs..."):
                                review = review_code(st.session_state.generated_question, code)
                                st.session_state.code_review_result = review

                # Display code review if submitted
                if st.session_state.code_review_result:
                    rev = st.session_state.code_review_result
                    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
                    st.markdown("<h3 class='section-title'>AI Code Review</h3>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; background-color:#1E293B; border:1px solid #334155; padding:0.75rem 1.25rem; border-radius:8px; margin-bottom:15px;">
                        <span>Code Correctness & Quality Rating</span>
                        <span class="review-score-badge">Score: {rev.get('score', 0)}/100</span>
                    </div>
                    """, unsafe_allow_html=True)

                    r_tab1, r_tab2, r_tab3, r_tab4 = st.tabs(["💡 Feedback", "📊 Complexity", "❌ Bugs & Mistakes", "🐍 Optimal Code"])
                    
                    with r_tab1:
                        st.info(rev.get("feedback", ""))
                        st.markdown("<h5>Core Strengths</h5>")
                        for s in rev.get("strengths", []):
                            st.markdown(f"✔ {s}")
                            
                    with r_tab2:
                        st.write(f"**Time Complexity:** `{rev.get('time_complexity', 'N/A')}`")
                        st.write(f"**Space Complexity:** `{rev.get('space_complexity', 'N/A')}`")
                        st.markdown("<h5>Correctness Analysis</h5>")
                        st.write(rev.get("correctness", ""))
                        
                    with r_tab3:
                        st.markdown("<h5>Identified Inefficiencies / Mistakes</h5>")
                        if rev.get("mistakes"):
                            for m in rev.get("mistakes", []):
                                st.markdown(f"<span style='color:#EF4444;'>✘ {m}</span>", unsafe_allow_html=True)
                        else:
                            st.success("No issues or syntax errors found in your implementation!")
                            
                    with r_tab4:
                        st.markdown("<h5>Optimal Implementation</h5>")
                        st.code(rev.get("optimized_solution", ""), language="python")

# ==========================================
# EVALUATION & POST-INTERVIEW STAGE
# ==========================================
elif st.session_state.active_step == "evaluation":

    # Sidebar Controls
    st.sidebar.markdown("<div class='sidebar-title'>Evaluation Controls</div>", unsafe_allow_html=True)
    
    if st.sidebar.button("🏠 Start New Session", type="primary", use_container_width=True):
        reset_session()
        st.rerun()

    # PDF Report Generator integration
    st.sidebar.markdown("<h4>Report Downloads</h4>", unsafe_allow_html=True)
    report_btn = st.sidebar.button("📄 Generate PDF Scorecard", use_container_width=True)
    
    if report_btn:
        with st.spinner("Creating beautiful PDF document..."):
            report_generator.generate_report(st.session_state.evaluation_result, "Interview_Report.pdf")
            st.success("PDF Generated Successfully!")
            
    if os.path.exists("Interview_Report.pdf"):
        with open("Interview_Report.pdf", "rb") as f:
            st.sidebar.download_button(
                "⬇ Download PDF Report",
                data=f,
                file_name=f"{st.session_state.name}_Interview_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    # Main dashboard display
    if st.session_state.evaluation_result:
        show_analytics(st.session_state.evaluation_result)
    else:
        st.error("No evaluation scorecard available. Please reset or contact support.")