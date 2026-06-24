import streamlit as st
import json
import time
import pandas as pd
 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
from utils import preprocess, load_faqs
 
# Page Config
st.set_page_config(
    page_title="Smart FAQ Assistant",
    page_icon="🤖",
    layout="wide"
)
 
# CSS Styling
st.markdown("""
<style>
 
.stApp {
    background: linear-gradient(
        135deg,
        #020617,
        #0F172A,
        #111827
    );
}
 
.main-title {
    color: #00F5FF;
    text-align: center;
    text-shadow: 0 0 20px #00F5FF;
}
 
[data-testid="stSidebar"] {
    background: rgba(8,17,31,0.95);
    border-right: 2px solid #00F5FF;
}
 
.stButton button {
    background: #141B2D;
    color: white;
    border: 1px solid #00F5FF;
    border-radius: 12px;
    box-shadow: 0 0 10px #00F5FF;
}
 
div[data-testid="stMetric"] {
    background: #141B2D;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #00F5FF;
}
 
</style>
""", unsafe_allow_html=True)
 
# Load FAQs (must happen before use)
faqs = load_faqs()
 
questions = [
    preprocess(faq["question"])
    for faq in faqs
]
 
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(questions)
 
# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
 
if "scores" not in st.session_state:
    st.session_state.scores = []
 
# Title
st.markdown("""
<h1 style='text-align:center;color:#00F5FF;'>
🤖 Smart FAQ Assistant
</h1>
 
<h3 style='text-align:center;color:white;'>
 AI-Powered Knowledge Hub for
Artificial Intelligence, Machine Learning,
Deep Learning & NLP
</h3>
 
<p style='text-align:center;color:#A0AEC0;'>
Ask anything about AI technologies ⚡
</p>
""", unsafe_allow_html=True)
 
# Metrics (after faqs is loaded)
c1, c2 = st.columns(2)
 
with c1:
    st.metric("📚 FAQs", f"{len(faqs)}+")
 
with c2:
    st.metric("🤖 Topics", "AI • ML • NLP • DL")
 
# Sidebar
menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📚 FAQ Browser",
        "💬 Chatbot",
        "📊 Analytics",
        "ℹ️ About"
    ]
)
 
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()
 
st.sidebar.subheader("💡 Example Questions")
st.sidebar.info("What is AI?")
st.sidebar.info("What is NLP?")
st.sidebar.info("What is Deep Learning?")
st.sidebar.info("What is TensorFlow?")
 
# Home
if menu == "🏠 Home":
 
    st.markdown("## 🚀 Features")
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.info("📚 FAQ Browser\n\nBrowse AI FAQs")
 
    with col2:
        st.info("💬 Smart Chatbot\n\nAsk Questions Naturally")
 
    col3, col4 = st.columns(2)
 
    with col3:
        st.info("🧠 NLP Engine\n\nTF-IDF Matching")
 
    with col4:
        st.info("📊 Analytics\n\nTrack Usage")
 
    st.markdown("---")
 
    st.subheader("✨ Recent Features")
 
    st.success("✅ NLP Matching")
    st.success("✅ TF-IDF Vectorization")
    st.success("✅ Cosine Similarity")
    st.success("✅ AI Knowledge Base")
 
# FAQ Browser
elif menu == "📚 FAQ Browser":
 
    st.header("📚 FAQ Browser")
 
    search = st.text_input("Search FAQ")
 
    category = st.radio(
        "Category",
        ["All", "AI", "ML", "NLP", "Deep Learning", "Python"],
        horizontal=True
    )
 
    filtered_faqs = []
    for faq in faqs:
        match_search = search.lower() in faq["question"].lower() if search else True
        match_category = (
            category == "All" or
            faq.get("category", "").upper() == category.upper()
        )
        if match_search and match_category:
            filtered_faqs.append(faq)
 
    st.success(f"📚 {len(filtered_faqs)} FAQs Shown  ({len(faqs)} Total)")
 
    for faq in filtered_faqs:
        with st.expander(faq["question"]):
            st.write(faq["answer"])
 
# Chatbot
elif menu == "💬 Chatbot":
 
    st.success("🟢 AI Assistant Online")
 
    st.info("""Hello 👋
 
I can answer questions about:
 
• Artificial Intelligence
• Machine Learning
• Deep Learning
• NLP
• TensorFlow
• PyTorch
 
Try asking: What is Machine Learning?
""")
 
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
 
    user_input = st.chat_input("Ask AI & ML Question...")
 
    if user_input:
 
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
 
        processed_input = preprocess(user_input)
 
        input_vector = vectorizer.transform([processed_input])
 
        similarity = cosine_similarity(input_vector, faq_vectors)
 
        best_match = similarity.argmax()
        confidence = float(similarity[0][best_match])
 
        st.session_state.scores.append(confidence)
 
        if confidence > 0.20:
            answer = faqs[best_match]["answer"]
        else:
            answer = "Question not found. Please ask AI related questions."
 
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
 
        st.rerun()
 
# Analytics
elif menu == "📊 Analytics":
 
    st.header("📊 Analytics Dashboard")
 
    avg_confidence = (
        f"{sum(st.session_state.scores) / len(st.session_state.scores) * 100:.0f}%"
        if st.session_state.scores else "N/A"
    )
 
    c1, c2, c3 = st.columns(3)
 
    with c1:
        st.metric("Questions Asked", len(st.session_state.messages))
 
    with c2:
        st.metric("FAQs Available", len(faqs))
 
    with c3:
        st.metric("Average Confidence", avg_confidence)
 
    data = pd.DataFrame({
        "Topics": ["AI", "ML", "NLP", "DL"],
        "Usage":  [25, 40, 15, 20]
    })
 
    st.bar_chart(data.set_index("Topics"))
 
# About
elif menu == "ℹ️ About":
 
    st.title("ℹ️ About")
 
    st.markdown("""
 
### Smart FAQ Assistant
 
Built Using
 
✅ Python
 
✅ Streamlit
 
✅ NLP
 
✅ TF-IDF
 
✅ Cosine Similarity
 
### Developer
 
👨‍💻 Sreenadh Gajjala
 
CSE (AI & ML)
 
NBKRIST
 
""")
 
    st.markdown("---")
 
st.markdown(
    """
    <center>
    Developed by Sreenadh Gajjala<br>
    Powered by Python • NLP • Streamlit
    </center>
    """,
    unsafe_allow_html=True
)