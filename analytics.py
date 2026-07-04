import streamlit as st
import plotly.graph_objects as go


def show_analytics(memory):

    st.header("📊 Interview Analytics")

    technical = memory.get("technical_score", 70)
    communication = memory.get("communication_score", 70)
    confidence = memory.get("confidence_score", 70)

    c1, c2, c3 = st.columns(3)

    c1.metric("💻 Technical", f"{technical}%")
    c2.metric("🗣 Communication", f"{communication}%")
    c3.metric("🎯 Confidence", f"{confidence}%")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[
                "Technical",
                "Communication",
                "Confidence"
            ],
            y=[
                technical,
                communication,
                confidence
            ]
        )
    )

    fig.update_layout(
        height=350,
        title="Interview Performance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("🔥 Strong Topics")

    for topic in memory.get("strong_topics", []):

        st.success(topic)

    st.subheader("⚠ Weak Topics")

    for topic in memory.get("weak_topics", []):

        st.error(topic)