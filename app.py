import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import streamlit as st
import pandas as pd
import plotly.express as px
from googletrans import Translator
import json
from langdetect import detect

# ---------------------- Utility Functions ----------------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def translate_text(text, target_lang="en"):
    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except:
        return text  # Return original if translation fails

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="Emotion Analysis", layout="wide")

st.title("Customer Feedback Analysis")
st.write("Analyze customer emotions, topics, and sentiment scoring.")

# ------ User Input ------
feedback = st.text_area("Enter Customer Feedback(any language):",
                        "The delivery was incredibly fast and the quality was amazing! However, one of the clothing items didn't fit well.")

if st.button("Analyze Feedback"):
    from emotion import EmotionAnalyzer
    from topic import TopicAnalyzer
    from adorescore import AdorescoreCalculator
    
    detected_lang = detect_language(feedback)
    translated_feedback = feedback if detected_lang == "en" else translate_text(feedback)
    
    if detected_lang != "en":
        st.write(f"🔄 Translated Feedback: **{translated_feedback}**")
    
    # Step 1: Emotion Analysis
    emotion_analyzer = EmotionAnalyzer()
    emotion_result = emotion_analyzer.analyze_feedback(translated_feedback)
    
    try:
        emotion_result = json.loads(emotion_result) if isinstance(emotion_result, str) else emotion_result
    except json.JSONDecodeError:
        st.error("Error processing emotion analysis.")
        st.stop()
    
    categorized_emotions = emotion_result.get("categorized_emotions", {"High Activation": [], "Medium Activation": [], "Low Activation": []})
    
    # Step 2: Topic Analysis
    topic_analyzer = TopicAnalyzer()
    topic_result = topic_analyzer.analyze_feedback(translated_feedback)
    
    try:
        topic_result = json.loads(topic_result) if isinstance(topic_result, str) else topic_result
    except json.JSONDecodeError:
        st.error("Error processing topic analysis.")
        st.stop()
    
    topics = topic_result.get("topics", {"main": [], "subtopics": {}})
    
    # Step 3: Adorescore Calculation
    adore_analyzer = AdorescoreCalculator()
    adorescore_result = adore_analyzer.calculate_adorescore(translated_feedback)
    
    try:
        adorescore_result = json.loads(adorescore_result) if isinstance(adorescore_result, str) else adorescore_result
    except json.JSONDecodeError:
        st.error("Error processing Adorescore calculation.")
        st.stop()
    
    adorescore = adorescore_result.get("adorescore", {"overall": 0})
    # ------ Mapping Emotions to Topics ------
    emotion_topic_map = {}
    for theme in topics["main"]:
        emotion_topic_map[theme] = {
            "dominant_emotions": [],
            "subtopics": topics["subtopics"].get(theme, [])
        }

        for emotion_category in ["High Activation", "Medium Activation", "Low Activation"]:
            for emotion in categorized_emotions[emotion_category]:
                emotion_topic_map[theme]["dominant_emotions"].append(emotion["emotion"])

    # ------ UI Layout ------
    col1, col2, col3, col4 = st.columns(4)

    # Function to create radar chart
    def create_radar_chart(emotion_list, title):
        if not emotion_list:
            return None
        df = pd.DataFrame(emotion_list)
        fig = px.line_polar(df, r="intensity", theta="emotion", line_close=True, title=title)
        fig.update_traces(fill="toself")
        return fig

    if categorized_emotions["High Activation"]:
        col1.plotly_chart(create_radar_chart(categorized_emotions["High Activation"], "High Activation Emotions"), use_container_width=True)
    if categorized_emotions["Medium Activation"]:
        col2.plotly_chart(create_radar_chart(categorized_emotions["Medium Activation"], "Medium Activation Emotions"), use_container_width=True)
    if categorized_emotions["Low Activation"]:
        col3.plotly_chart(create_radar_chart(categorized_emotions["Low Activation"], "Low Activation Emotions"), use_container_width=True)

    with col4:
        st.metric(label="🚀 Adorescore", value=f"{adorescore.get('overall', 0):.2f}")
        st.subheader("Top Themes in Dataset")
        if topics["main"]:
            for theme in topics["main"]:
                st.write(f"🔹 **{theme}**")
        else:
            st.write("No themes detected.")
            
    # ------ Display Themes & Subtopics ------
    st.subheader("Themes & Customer Feedback")
    if topics["main"]:
        num_themes = len(topics["main"])
        cols = st.columns(num_themes if num_themes <= 4 else 4)  # Max 4 themes per row

        for i, theme in enumerate(topics["main"]):
            with cols[i % 4]:  # Distribute themes across columns
                st.markdown(f"### 🏷️ {theme}")
                subtopics = topics["subtopics"].get(theme, [])

                if subtopics:
                    st.markdown("📌 **Subtopics:**")
                    for subtopic in subtopics:
                        st.write(f"🔹 {subtopic}")
                else:
                    st.write("No subtopics available.")

    else:
        st.write("No topics detected.")

    
    # ------ Detailed Adorescore Breakdown ------
    with st.expander("📌 Detailed Adorescore Breakdown", expanded=True):
        st.subheader("🔹 Emotions Contributing to Adorescore")

        col1, col2 = st.columns(2)
        with col1:
            primary_emotion = adorescore_result.get("emotions", {}).get("primary", {})
            if primary_emotion:
                st.markdown(f"💡 **Primary Emotion:** {primary_emotion.get('emotion', 'N/A').title()}")
                st.write(f"-  Activation: {primary_emotion.get('activation', 'N/A')}")
                st.write(f"-  Intensity: {primary_emotion.get('intensity', 0):.4f}")

        with col2:
            secondary_emotion = adorescore_result.get("emotions", {}).get("secondary", {})
            if secondary_emotion:
                st.markdown(f"🧐 **Secondary Emotion:** {secondary_emotion.get('emotion', 'N/A').title()}")
                st.write(f" -  Activation: {secondary_emotion.get('activation', 'N/A')}")
                st.write(f" -  Intensity: {secondary_emotion.get('intensity', 0):.4f}")

        st.subheader("🚀 Topic Breakdown")

        topics = adorescore_result.get("topics", {}).get("main", [])
        subtopics = adorescore_result.get("topics", {}).get("subtopics", {})
        breakdown = adorescore_result.get("adorescore", {}).get("breakdown", {})

        if topics:
            for topic in topics:
                st.markdown(f"🔹 **{topic}:**") #Main Topic
                if subtopics.get(topic):
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;**Subtopics:**", unsafe_allow_html=True) #Subtopics label
                    for subtopic in subtopics.get(topic, []):
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- 📊 {subtopic}", unsafe_allow_html=True) #Actual Subtopics

                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp; 📈**Contribution:** {breakdown.get(topic, 0):.4f}", unsafe_allow_html=True) #Contribution Value
                st.write("---")

        else:
            st.write("No topics found.")   
    # ------ Summary ------
    st.subheader("🚀 Emotion & Sentiment Summary")
    primary_emotion = emotion_result.get("emotion_analysis", {}).get("emotions", {}).get("primary", {})
    secondary_emotion = emotion_result.get("emotion_analysis", {}).get("emotions", {}).get("secondary", {})

    if primary_emotion:
        st.write(f"💡 **Primary Emotion:** {primary_emotion.get('emotion', 'N/A').title()} "
                 f"(Activation: {primary_emotion.get('activation', 'N/A')}, "
                 f"Intensity: {primary_emotion.get('intensity', 0):.4f})")

    if secondary_emotion:
        st.write(f"🧐 **Secondary Emotion:** {secondary_emotion.get('emotion', 'N/A').title()} "
                 f"(Activation: {secondary_emotion.get('activation', 'N/A')}, "
                 f"Intensity: {secondary_emotion.get('intensity', 0):.4f})")

    # Footer
    st.markdown("---")
    st.caption("📊 Built with Streamlit | © 2025")