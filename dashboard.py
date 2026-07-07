import streamlit as st
import plotly.graph_objects as go

def gauge(title, value, color="#6366F1"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#FFFFFF", "family": "Outfit", "size": 18}},
        number={"font": {"color": "#FFFFFF", "family": "Outfit"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
            "bar": {"color": color},
            "bgcolor": "#1E293B",
            "borderwidth": 1,
            "bordercolor": "#334155",
            "steps": [
                {"range": [0, 40], "color": "rgba(239, 68, 68, 0.1)"},
                {"range": [40, 70], "color": "rgba(245, 158, 11, 0.1)"},
                {"range": [70, 100], "color": "rgba(16, 185, 129, 0.1)"},
            ]
        }
    ))
    fig.update_layout(
        height=220, 
        margin=dict(l=30, r=30, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def radar_chart(analysis):
    categories = [
        "ATS Score",
        "Technical Depth",
        "Communication",
        "Formatting",
        "Projects Strength"
    ]
    values = [
        analysis.get("ats_score", 0),
        analysis.get("technical_score", 0),
        analysis.get("communication_score", 0),
        analysis.get("formatting_score", 0),
        analysis.get("project_score", 0)
    ]
    
    values.append(values[0])
    categories.append(categories[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(99, 102, 241, 0.2)",
        line=dict(color="#6366F1", width=2),
        name="Resume Metrics"
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,100], gridcolor="#334155", tickfont=dict(color="#94A3B8")),
            angularaxis=dict(gridcolor="#334155", tickfont=dict(color="#E2E8F0", size=11))
        ),
        showlegend=False,
        height=380,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def show_resume_dashboard(analysis):
    st.markdown("<h2 class='section-title'>📄 Resume Scorecard</h2>", unsafe_allow_html=True)
    
    # Metics Gauge Columns
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(
            gauge("Overall Quality", analysis.get("overall_score", 0), "#6366F1"),
            use_container_width=True
        )
    with c2:
        st.plotly_chart(
            gauge("ATS Readability", analysis.get("ats_score", 0), "#10B981"),
            use_container_width=True
        )
    with c3:
        st.plotly_chart(
            gauge("Technical Depth", analysis.get("technical_score", 0), "#3B82F6"),
            use_container_width=True
        )

    # Secondary scores layout in columns
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""
        <div class="premium-card metric-card" style="border-top-color: #6366F1;">
            <p style="color: #94A3B8; margin-bottom: 5px; font-size: 0.9rem;">Written Communication</p>
            <h2 style="margin: 0; color: #FFFFFF;">{analysis.get("communication_score", 0)}%</h2>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="premium-card metric-card" style="border-top-color: #EC4899;">
            <p style="color: #94A3B8; margin-bottom: 5px; font-size: 0.9rem;">Formatting & Layout</p>
            <h2 style="margin: 0; color: #FFFFFF;">{analysis.get("formatting_score", 0)}%</h2>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div class="premium-card metric-card" style="border-top-color: #F59E0B;">
            <p style="color: #94A3B8; margin-bottom: 5px; font-size: 0.9rem;">Projects Impact</p>
            <h2 style="margin: 0; color: #FFFFFF;">{analysis.get("project_score", 0)}%</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='section-title'>📊 Resume Radar Analysis</h2>", unsafe_allow_html=True)
    st.plotly_chart(radar_chart(analysis), use_container_width=True)

    # Strengths & Weaknesses custom card design
    left, right = st.columns(2)
    with left:
        strengths_html = "".join(f"<div class='topic-badge' style='background-color: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.3); color: #34D399;'>✔ {s}</div>" for s in analysis.get("strengths", []))
        st.markdown(f"""
        <div class="premium-card" style="min-height: 250px;">
            <h3 style="margin-top: 0; color: #10B981 !important;">✅ Core Strengths</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
                {strengths_html if strengths_html else '<p style="color:#94A3B8;">None identified</p>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        weaknesses_html = "".join(f"<div class='topic-badge' style='background-color: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.3); color: #F87171;'>⚠ {w}</div>" for w in analysis.get("weaknesses", []))
        st.markdown(f"""
        <div class="premium-card" style="min-height: 250px;">
            <h3 style="margin-top: 0; color: #EF4444 !important;">⚠ Key Weaknesses</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
                {weaknesses_html if weaknesses_html else '<p style="color:#94A3B8;">None identified</p>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='section-title'>💡 Actionable AI Suggestions</h2>", unsafe_allow_html=True)
    for suggestion in analysis.get("suggestions", []):
        st.markdown(f"""
        <div class="premium-card" style="padding: 1rem; border-left: 4px solid #6366F1; background-color: #1E293B;">
            <p style="margin: 0; color: #E2E8F0; font-size: 0.95rem;">{suggestion}</p>
        </div>
        """, unsafe_allow_html=True)