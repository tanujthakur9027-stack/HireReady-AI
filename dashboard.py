import streamlit as st
import plotly.graph_objects as go


def gauge(title, value):

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=value,

        title={"text": title},

        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#00C853"},
            "steps": [
                {"range": [0, 40], "color": "#ffebee"},
                {"range": [40, 70], "color": "#fff8e1"},
                {"range": [70, 100], "color": "#e8f5e9"},
            ]
        }

    ))

    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))

    return fig


def radar_chart(analysis):

    categories = [
        "ATS",
        "Technical",
        "Communication",
        "Formatting",
        "Projects"
    ]

    values = [
        analysis["ats_score"],
        analysis["technical_score"],
        analysis["communication_score"],
        analysis["formatting_score"],
        analysis["project_score"]
    ]

    values.append(values[0])
    categories.append(categories[0])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(

        r=values,

        theta=categories,

        fill="toself",

        name="Resume"

    ))

    fig.update_layout(

        polar=dict(radialaxis=dict(visible=True, range=[0,100])),

        showlegend=False,

        height=450

    )

    return fig


def show_resume_dashboard(analysis):

    st.header("📄 Resume Intelligence")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.plotly_chart(
            gauge("Overall", analysis["overall_score"]),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            gauge("ATS", analysis["ats_score"]),
            use_container_width=True
        )

    with c3:
        st.plotly_chart(
            gauge("Technical", analysis["technical_score"]),
            use_container_width=True
        )

    st.divider()

    st.subheader("📊 Resume Radar")

    st.plotly_chart(
        radar_chart(analysis),
        use_container_width=True
    )

    st.divider()

    left,right = st.columns(2)

    with left:

        st.subheader("✅ Strengths")

        for s in analysis["strengths"]:
            st.success(s)

    with right:

        st.subheader("⚠ Weaknesses")

        for w in analysis["weaknesses"]:
            st.warning(w)

    st.divider()

    st.subheader("💡 AI Suggestions")

    for s in analysis["suggestions"]:
        st.info(s)