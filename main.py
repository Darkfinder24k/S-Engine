import streamlit as st
from googleapiclient.discovery import build
import base64  # For background image

# --- API Configuration ---
API_KEY = "AIzaSyCZ-1xA0qHy7p3l5VdZYCrvoaQhpMZLjig"  # Your API key
SEARCH_ENGINE_ID = "c38572640fa0441bc"  # Your Search Engine ID

# --- Your Website URL (for redirection) ---
YOUR_WEBSITE_URL = "https://yourwebsite.com/"  # Replace with your actual website URL

# --- Function to Fetch Search Results ---
@st.cache_data(show_spinner=False)
def fetch_quantora_results(search_term, api_key, cse_id, **kwargs):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res.get("items", [])
    except Exception as e:
        st.error(f"Quantora encountered a data retrieval anomaly: {e}")
        return []

# --- Function to create a redirect URL ---
def create_redirect_url(target_url):
    # This is a basic example. You might need a more sophisticated
    # redirection mechanism on your website.
    return f"{YOUR_WEBSITE_URL}redirect?url={target_url}"

# --- Futuristic UI Styling ---
st.set_page_config(
    page_title="⚛️ Quantora Search Engine",
    page_icon=":neuron:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for a premium, futuristic look (same as before)
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

        body {
            background-color: #0a0b0e;
            color: #f0f8ff;
            font-family: 'Montserrat', sans-serif;
        }

        .stApp {
            background-color: transparent;
        }

        .stTextInput > div > div > input {
            background-color: #1e212b;
            color: #f0f8ff;
            border: 1px solid #384459;
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 16px;
        }

        .stButton > button {
            background-color: #a78bfa;
            color: #f0f8ff;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #8b5cf6;
        }

        .st-emotion-cache-r421ms { /* Result container */
            background-color: #1e212b;
            color: #f0f8ff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            border: 1px solid #384459;
        }

        .st-emotion-cache-16txtl3 { /* Link style */
            color: #bae6fd;
            text-decoration: none;
        }

        .st-emotion-cache-16txtl3:hover {
            text-decoration: underline;
        }

        .st-emotion-cache-10pw50 { /* Snippet style */
            color: #d1d5db;
            font-size: 14px;
        }

        h1 {
            color: #a78bfa;
            text-align: center;
            margin-bottom: 30px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        h2 {
            color: #f0f8ff;
            margin-top: 25px;
            margin-bottom: 15px;
            font-weight: bold;
        }

        .sidebar .sidebar-content {
            background-color: #1e212b;
            color: #f0f8ff;
        }

        .sidebar h2 {
            color: #a78bfa;
        }

        .st-emotion-cache-1dp50ho { /* Expander header */
            color: #f0f8ff;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Optional: Futuristic Background ---
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64});
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# set_background('futuristic_background.png')

# --- Main Application ---
st.title("Quantora :neuron:")
st.subheader("Intelligent Information Synthesis")

query = st.text_input("Enter your Quantora query:", "")

if query:
    st.info(f"Quantora is processing your request for: '{query}'...")

    # Fetch search results
    results = fetch_quantora_results(query, API_KEY, SEARCH_ENGINE_ID, num=10)

    if results:
        st.subheader("Quantora Insights:")
        for i, result in enumerate(results):
            title = result.get('title', 'No Title')
            link = result.get('link', '#')
            snippet = result.get('snippet', 'No Description')

            # Create the redirect URL
            redirect_url = create_redirect_url(link)

            st.markdown(f"<div class='st-emotion-cache-r421ms'><strong>{i+1}. {title}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<a class='st-emotion-cache-16txtl3' href='{redirect_url}' target='_blank'>{link}</a>", unsafe_allow_html=True)
            st.markdown(f"<p class='st-emotion-cache-10pw50'>{snippet}</p>", unsafe_allow_html=True)
            st.divider()
    else:
        st.warning("Quantora found no relevant insights for this query.")

# --- Sidebar for Advanced Options (Optional) ---
with st.sidebar:
    st.header("Quantora Core Settings")
    safe_search = st.checkbox("Engage Neural Filtering (Filter Explicit Content)", value=True)
    if safe_search:
        safe_level = "active"
    else:
        safe_level = "off"

    results_count = st.slider("Insight Stream Limit (Results per page):", min_value=1, max_value=20, value=10)

    st.markdown("---")
    st.markdown("<p style='color:#d1d5db; font-size:12px;'>Powered by Quantora's Neural Network</p>", unsafe_allow_html=True)
