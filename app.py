import streamlit as st
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="Zee AI - Your Smart Assistant", page_icon="🔬")

# Hide Streamlit Menu Footer and Header
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# Round Picture Style
st.sidebar.markdown("""
    <style>
    [data-testid="stSidebar"] img {
        border-radius: 50%;
        border: 3px solid #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Your Profile Section
st.sidebar.image("https://avatars.githubusercontent.com/zee5969", width=100)
st.sidebar.title("Zeeshan Ali")
st.sidebar.write("🏥 Medical Lab Technology Student")
st.sidebar.write("🎓 Riphah International University")
st.sidebar.write("📍 Islamabad, Pakistan")
st.sidebar.write("🤖 AI Chatbot Developer")
st.sidebar.markdown("---")
st.sidebar.write("💬 Ask me anything!")

# Chatbot Section
st.title("🔬 MedGenius")
st.write("Ask me anything!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Upload and Camera ABOVE chat input
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader(
        "📎 Upload File",
        type=["txt", "pdf", "png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

with col2:
    camera_photo = st.camera_input(
        "📷 Camera",
        label_visibility="collapsed"
    )

# Show uploaded file
if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    if uploaded_file.type.startswith("image"):
        st.image(uploaded_file, width=300)
    # Tell AI about file
    file_message = f"User uploaded a file named: {uploaded_file.name}"
    st.session_state.messages.append({
        "role": "user",
        "content": file_message
    })

# Show camera photo
if camera_photo is not None:
    st.success("✅ Photo taken!")
    st.image(camera_photo, width=300)

# Chat Input at Bottom
user_input = st.chat_input("Type your message here...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages
    )

    ai_reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })
