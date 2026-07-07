# HireReady-AI

> **Commercial-Grade, AI-Powered Career Preparation Workspace & Realistic Mock Interview Portal**

HireReady-AI is an intelligent interview preparation platform designed to help candidates evaluate their resumes, optimize ATS compatibility, practice AI-powered mock interviews with dynamic graph cognitive memory, resolve coding challenges in a built-in IDE, and inspect performance analytics.

---

## 🚀 Core Features

### 🔐 1. Secure User Authentication
- Built-in signup and sign-in interfaces powered by SQLite database migrations.
- Secure credential protection using SHA256 password hashing with unique salts.
- Complete session-state route guards to lock user dashboard data and mock interview panels.

### 📄 2. AI Resume Intelligence
- **Semantic ATS Audit**: Parses and evaluates resume formatting, heading checklist completeness, and technical keyword density.
- **Job Description Matcher**: Runs deep semantic analysis matching candidate profiles with target JDs to identify skills gaps, direct strengths, and role alignment.
- **Scorecard Radar**: Visualizes overall resume ratings, formatting, projects, and communication scores in Plotly gauges and radar charts.

### 🤝 3. Mock Interview Room
- **Structured State-Machine Flow**: Select interview lengths (3, 5, or 8 questions) and monitor progress with real-time timers and progress bar indicators.
- **Webcam & Audio support**: Integrates live webcam feeds (OpenCV/webrtc) and text-to-speech audio playback.
- **Dual-Pane IDE Workspace**: Practice coding questions generated dynamically for your target role and company. Features a Monaco-style editor, local python compilation inside a terminal console, and detailed FAANG AI reviews.

### 🧠 4. Graph Cognitive Memory (Cognee)
- Relocates LanceDB and Ladybug databases to a clean workspace directory.
- Graph cognification stores detailed summaries of previous interview performance.
- Direct memory recall injects candidate history back to the interviewer prompt, enabling personalized follow-up on historical weak topics.

---

## 🛠 Tech Stack

- **Frontend / Portal**: Streamlit, Streamlit Ace, Streamlit WebRTC
- **AI Engine / LLM**: Google Gemini API, Google GenAI SDK (`gemini-2.5-flash`), Cognee Memory Layer
- **Databases**: SQLite (Authentication), LanceDB (Vector indexing), Ladybug / Kuzu (Graph store)
- **Formatting / Reports**: ReportLab PDF, Plotly charts

---

## 🚀 Getting Started

### Local Setup
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd HireReady-AI
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root folder and configure the API Keys:
   ```env
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY
   LLM_API_KEY=YOUR_GEMINI_API_KEY
   GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
   EMBEDDING_API_KEY=YOUR_GEMINI_API_KEY
   
   LL_PROVIDER=gemini
   LLM_MODEL=gemini/gemini-2.5-flash
   EMBEDDING_PROVIDER=gemini
   EMBEDDING_MODEL=gemini/gemini-embedding-001
   EMBEDDING_DIMENSIONS=3072
   
   COGNEE_SKIP_CONNECTION_TEST=true
   SYSTEM_ROOT_DIRECTORY="c:/path/to/project/data/cognee_system"
   DATA_ROOT_DIRECTORY="c:/path/to/project/data/cognee_data"
   ```
5. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

---

## ☁ Production Deployment

This project contains a `render.yaml` blueprint for zero-config production deployment on **Render**:

1. Push your updated code to a private GitHub repository.
2. Link the repository to your Render dashboard.
3. Deploy using the **Blueprint** option to automatically set up the Python web service and map env values.
