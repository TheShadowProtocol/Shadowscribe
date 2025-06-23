import streamlit as st
from summarizer import get_summary
from utils import extract_text_from_file, extract_text_from_url, is_url
import base64

def inject_custom_css(logo_path, bg_path):
    with open(logo_path, "rb") as logo_file:
        logo_data = base64.b64encode(logo_file.read()).decode()

    with open(bg_path, "rb") as bg_file:
        bg_data = base64.b64encode(bg_file.read()).decode()

    css = f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{bg_data}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            header {{
                visibility: hidden;
            }}
            .shadow-logo {{
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
            }}
            .shadow-logo img {{
                max-height: 120px;
            }}
        </style>
        <div class="shadow-logo">
            <img src="data:image/png;base64,{logo_data}" alt="Shadow Scribe Logo" />
        </div>
    """
    st.markdown(css, unsafe_allow_html=True)

# ────────────────────────────── UI INIT ────────────────────────────── #
st.set_page_config(page_title="Shadow Scribe", page_icon="🌒 📝", layout="centered")
inject_custom_css("logo.png", "dark-bg.jpg")

st.title("📝🌒Shadow Scribe")
st.caption("Where silence meets syntax. Summarized by Shadow’s mind.")

# ────────────────────────────── TABS ────────────────────────────── #
tab1, tab2, tab3 = st.tabs(["📄 Paste Text", "📂 Upload File", "🌐 From URL"])

text_input = ""
file_type = None  # To route PDF internally

# 🔹 Tab 1: Paste Text
with tab1:
    text_input = st.text_area("Paste your content here:", height=300)

# 🔹 Tab 2: Upload File
with tab2:
    uploaded_file = st.file_uploader("Upload a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])
    if uploaded_file:
        text_input = extract_text_from_file(uploaded_file)
        if text_input:
            st.success("File content loaded successfully!")
            if uploaded_file.name.endswith(".pdf"):
                file_type = "pdf"
        else:
            st.error("Could not extract text from the uploaded file.")

# 🔹 Tab 3: URL Input
with tab3:
    url_input = st.text_input("Paste a web article URL (starts with http:// or https://):")
    if url_input:
        text_input = url_input  # Let backend decide it's a URL

# ────────────────────────────── Options & Generate ────────────────────────────── #
tone = st.selectbox("🗣️ Tone", ["Formal", "Casual", "Detailed" ])
length = st.selectbox("📏 Length", ["Short", "Medium", "Detailed"])

if st.button("⚡ Summarize Now"):
    if not text_input or not text_input.strip():
        st.warning("Give me something to work with, Shadow.")
    else:
        with st.spinner("Summoning the summary magic..."):
            summary = get_summary(text_input, tone=tone.lower(), length=length.lower(), file_type=file_type)
            st.success("Here’s your shiny new summary:")

            st.text_area("🔥 Output:", summary, height=200)

            st.download_button(
                label="💾 Download Summary",
                data=summary,
                file_name="shadow_summary.txt",
                mime="text/plain"
            )
