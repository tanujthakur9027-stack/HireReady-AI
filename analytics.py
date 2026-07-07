import streamlit as st
import plotly.graph_objects as go
from dashboard import gauge

def show_analytics(memory):
    st.markdown("<h2 class='section-title'>📊 Interview Performance Scorecard</h2>", unsafe_allow_html=True)
    
    technical = memory.get("technical_score", 70)
    communication = memory.get("communication_score", 70)
    confidence = memory.get("confidence_score", 70)

    # 3 Gauge Indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(
            gauge("Technical Skills", technical, "#3B82F6"),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            gauge("Communication", communication, "#10B981"),
            use_container_width=True
        )
    with col3:
        st.plotly_chart(
            gauge("Confidence & Delivery", confidence, "#F59E0B"),
            use_container_width=True
        )

    # High level overall feedback
    overall_feedback = memory.get("overall_feedback", "")
    if overall_feedback:
        st.markdown(f"""
        <div class="premium-card" style="border-left: 4px solid #6366F1;">
            <h4 style="margin:0 0 8px 0; color: #6366F1 !important;">General Evaluation Summary</h4>
            <p style="margin:0; color: #E2E8F0; font-size: 0.95rem; line-height: 1.6;">{overall_feedback}</p>
        </div>
        """, unsafe_allow_html=True)

    # Columns for Strong vs Weak topics
    left, right = st.columns(2)
    with left:
        strong_html = "".join(f"<div class='topic-badge' style='background-color: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.3); color: #34D399;'>✔ {topic}</div>" for topic in memory.get("strong_topics", []))
        st.markdown(f"""
        <div class="premium-card" style="min-height: 220px;">
            <h3 style="margin-top:0; color:#10B981 !important;">🔥 Demonstrated Strong Topics</h3>
            <div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:1rem;">
                {strong_html if strong_html else '<p style="color:#94A3B8;">None recorded</p>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        weak_html = "".join(f"<div class='topic-badge' style='background-color: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.3); color: #F87171;'>⚠ {topic}</div>" for topic in memory.get("weak_topics", []))
        st.markdown(f"""
        <div class="premium-card" style="min-height: 220px;">
            <h3 style="margin-top:0; color:#EF4444 !important;">⚠ Areas for Improvement</h3>
            <div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:1rem;">
                {weak_html if weak_html else '<p style="color:#94A3B8;">None recorded</p>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Specific Mistakes and Study Recommendations
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown(f"""
        <div class="premium-card" style="min-height: 250px; border-top: 4px solid #EF4444;">
            <h4 style="margin-top: 0; color: #EF4444 !important;">❌ Key Errors & Mistakes</h4>
            <ul style="color: #CBD5E1; padding-left: 20px; font-size: 0.95rem; line-height: 1.5;">
                {"".join(f"<li style='margin-bottom: 8px;'>{m}</li>" for m in memory.get("mistakes", [])) if memory.get("mistakes") else "<li style='color:#94A3B8; list-style-type:none;'>No critical mistakes noted! Keep it up.</li>"}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with c_b:
        st.markdown(f"""
        <div class="premium-card" style="min-height: 250px; border-top: 4px solid #F59E0B;">
            <h4 style="margin-top: 0; color: #F59E0B !important;">📖 Study Plan Recommendations</h4>
            <ul style="color: #CBD5E1; padding-left: 20px; font-size: 0.95rem; line-height: 1.5;">
                {"".join(f"<li style='margin-bottom: 8px;'>{rec}</li>" for rec in memory.get("recommended_topics", [])) if memory.get("recommended_topics") else "<li style='color:#94A3B8; list-style-type:none;'>No specific study topics suggested yet.</li>"}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Question-by-Question review breakdown
    qa_review = memory.get("qa_review", [])
    if qa_review:
        st.markdown("<h2 class='section-title'>📝 Question-by-Question Evaluation</h2>", unsafe_allow_html=True)
        for i, review in enumerate(qa_review):
            q_num = i + 1
            score = review.get("score", 0)
            
            # Choose color based on score
            score_color = "#10B981" if score >= 75 else ("#F59E0B" if score >= 50 else "#EF4444")
            
            expander_title = f"Question {q_num}: {review.get('question', '')[:65]}... (Score: {score}/100)"
            
            with st.expander(expander_title):
                st.markdown(f"**Interviewer Question:**")
                st.info(review.get("question", ""))
                
                st.markdown(f"**Your Answer:**")
                st.markdown(f"""
                <div style="background-color: #0F172A; border: 1px solid #334155; padding: 1rem; border-radius: 8px; color: #E2E8F0; font-style: italic; margin-bottom: 12px;">
                    "{review.get('answer', '')}"
                </div>
                """, unsafe_allow_html=True)
                
                col_score, col_blank = st.columns([1, 3])
                with col_score:
                    st.markdown(f"""
                    <div style="text-align: center; background-color: {score_color}; color: #FFFFFF; border-radius: 20px; padding: 0.25rem 0.75rem; font-weight: 700; font-size: 0.9rem;">
                        Answer Score: {score}/100
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
                
                # Strengths and gaps inside the expander
                col_str, col_gap = st.columns(2)
                with col_str:
                    st.markdown(f"""
                    <div style="background-color: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); padding: 0.75rem; border-radius: 6px; min-height: 100px;">
                        <span style="color:#10B981; font-weight:600; display:block; margin-bottom:4px;">✔ Key Strengths</span>
                        <span style="font-size:0.9rem; color:#CBD5E1;">{review.get('strengths', 'No specific strengths highlighted.')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_gap:
                    st.markdown(f"""
                    <div style="background-color: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); padding: 0.75rem; border-radius: 6px; min-height: 100px;">
                        <span style="color:#EF4444; font-weight:600; display:block; margin-bottom:4px;">⚠ Gaps / Areas to Improve</span>
                        <span style="font-size:0.9rem; color:#CBD5E1;">{review.get('gaps', 'No critical gaps identified.')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
                st.markdown("**Ideal Answer Guidance:**")
                st.success(review.get("ideal_answer", ""))