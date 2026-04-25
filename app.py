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
    
    /* Style the + button */
    .stButton button {
        border-radius: 50%;
        width: 45px;
        height: 45px;
        font-size: 25px;
        background-color: #0083B8;
        color: white;
        border: none;
        cursor: pointer;
    }
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

if "show_options" not in st.session_state:
    st.session_state.show_options = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# + Button Row
col1, col2 = st.columns([0.05, 0.95])

with col1:
    if st.button("➕"):
        st.session_state.show_options = not st.session_state.show_options

with col2:
    user_input = st.chat_input("Type your message here...")

# Show Upload or Camera when + clicked
if st.session_state.show_options:
    st.markdown("### Choose an option:")
    option_col1, option_col2 = st.columns(2)

    with option_col1:
        uploaded_file = st.file_uploader(
            "📎 Upload File",
            type=["txt", "pdf", "png", "jpg", "jpeg"]
        )

    with option_col2:
        camera_photo = st.camera_input("📷 Take Photo")

    # Show uploaded file
    if uploaded_file is not None:
        st.success(f"✅ File: {uploaded_file.name}")
        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file, width=300)

    # Show camera photo
    if camera_photo is not None:
        st.success("✅ Photo taken!")
        st.image(camera_photo, width=300)

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
