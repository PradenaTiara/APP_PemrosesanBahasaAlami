import streamlit as st
import joblib
import re
from base64 import b64encode

# Load model dan vectorizer
model = joblib.load("svm_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Preprocessing
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|@\w+|#\w+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Konversi gambar logo ke base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("poem.png")

# Set konfigurasi halaman
st.set_page_config(
    page_title="Poem Style Classifier",
    page_icon="poem.png",
    layout="centered"
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="stApp"] {{
    font-family: 'Poppins', sans-serif;
    background-color: #f4f4f4 !important;
    color: #1a1a1a !important;
}}

[data-testid="stHeader"] {{
    z-index: 0 !important;
}}

.navbar {{
    background-color: #ffffff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    display: flex;
    align-items: center;
    padding: 1.2rem 2rem;
    gap: 12px;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;
}}

.navbar-title {{
    font-size: 18px;
    font-weight: 600;
    color: #1c1c1c;
}}

.logo {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
}}

textarea {{
    border-radius: 8px !important;
    font-size: 1rem !important;
    padding: 1rem !important;
    background-color: #fefefe !important;
    color: #1a1a1a !important;
    border: 1px solid #ccc !important;
    resize: vertical;
    /* width: 100% !important; <-- HAPUS INI */
    box-sizing: border-box;
    display: block;
    margin: 0 auto;
}}


textarea:focus {{
    outline: none !important;
    border: 3px solid #ff6b6b !important;
    box-shadow: 0 0 0 4px rgba(127, 90, 240, 0.3) !important;
}}

.container {{
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    max-width: 700px;
    margin: 6rem auto 2rem auto;
}}

.output-box {{
    background-color: #ffffff;
    color: #1a1a1a;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-top: 3rem;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
    font-size: 1.1rem;
}}

.container, .output-box {{
    position: relative;
    z-index: 1;
}}

.background-box {{
    background-color: #ffffff;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 700px;
    min-height: 430px;
    border-radius: 16px;
    z-index: 0;
    transition: all 0.3s ease-in-out;
}}

h3.custom-heading {{
    margin-top: -1rem;
    font-weight: 700;
    text-align: center;
}}

div.stButton {{
    display: flex;
    justify-content: center;
    width: 100%;
    padding: 0 1rem;
}}

div.stButton > button {{
    background: linear-gradient(to right, #7f5af0, #ff6b6b);
    color: white !important;
    border: none;
    border-radius: 50px;
    padding: 0.60rem 3rem;
    font-size: 1rem;
    font-weight: 600;
    margin-top: 1.2rem;
    cursor: pointer;
    transition: 0.2s ease-in-out;
}}

div.stButton > button:hover {{
    opacity: 0.85;
}}

div.stButton > button:active {{
    transform: scale(0.97);
}}


.footer {{
    max-width: 700px;
    margin: 2rem auto -50rem auto;
    text-align: center;
    opacity: 0.6;
    font-size: 0.8rem;
}}

/* === DARK MODE === */
@media (prefers-color-scheme: dark) {{
    html, body, [class*="stApp"] {{
        background-color: #121212 !important;
        color: #f2f2f2 !important;
    }}

    .navbar {{
        background-color: #1e1e1e;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }}

    .navbar-title {{
        color: #ffffff;
    }}

    textarea {{
        background-color: #1e1e1e !important;
        color: #eeeeee !important;
        border: 1px solid #7A7A7A !important;
    }}

    .container, .output-box {{
        background-color: #1e1e1e;
        color: #f2f2f2;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}

    .background-box {{
        background-color: #1e1e1e;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}
}}

/* === RESPONSIVE UNTUK MOBILE === */
@media screen and (max-width: 768px) {{
    .navbar {{
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
        padding: 0.8rem 1.2rem;
    }}

    .navbar-title {{
        font-size: 1rem;
    }}

    .logo {{
        width: 32px;
        height: 32px;
    }}

    .container {{
        padding: 1rem;
        margin: 4rem auto 2rem auto;
    }}

    .background-box {{
        padding: 1rem;
    }}

    .output-box {{
        padding: 1rem;
        font-size: 1rem;
    }}

    textarea {{
        width: 100% !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1.2rem !important;
        margin: 0 auto !important;
        box-sizing: border-box;
    }}

    div.stButton > button {{
        width: 50%;
        max-width: 300px;
        padding: 0.30rem 1rem;
        font-size: 1rem;
        margin-top: -1px;
    }}

    .footer {{
        font-size: 0.7rem;
        margin: 2rem auto -30rem auto;
    }}
}}
</style>
""", unsafe_allow_html=True)


# === NAVBAR ===
st.markdown(f"""
<div class="navbar">
    <div style="display: flex; align-items: center; gap: 12px;">
        <img src="data:image/png;base64,{logo_base64}" class="logo" />
        <span class="navbar-title">Poem Style Classifier</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="background-box"></div>', unsafe_allow_html=True)

# === FORM INPUT===
st.markdown("<h3 class='custom-heading'>Poem Style Classifier</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,24,1])  

with col2:
    poem = st.text_area(
        label="",
        placeholder="Paste or type your poem here...",
        height=200,
    )

submit = st.button("Classify Poem")

if submit:
    if poem.strip():
        cleaned = clean_text(poem)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]

        st.markdown(f"""
        <div class="output-box">
            <p><strong>Classification Results</strong></p>
            <p>{prediction}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
        st.warning("Please enter a poem before classifying.")

# Footer
st.markdown("""
<br><br>
<div class='footer'>
    Made with ❤️ using Streamlit · © 2025 Poem Classifier
</div>
""", unsafe_allow_html=True)

