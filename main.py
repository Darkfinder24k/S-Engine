import streamlit as st
from googleapiclient.discovery import build
import base64  # For background image

# --- API Configuration ---
API_KEY = "AIzaSyCZ-1xA0qHy7p3l5VdZYCrvoaQhpMZLjig"  # Your API key
SEARCH_ENGINE_ID = "c38572640fa0441bc"  # Your Search Engine ID

# --- Your Website URL (not directly used for iframe) ---
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

# --- Function to Fetch Image Results ---
@st.cache_data(show_spinner=False)
def fetch_image_results(search_term, api_key, cse_id, num_images=5):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, searchType='image', num=num_images).execute()
        return res.get("items", [])
    except Exception as e:
        st.error(f"Quantora encountered an image retrieval anomaly: {e}")
        return []

# --- Futuristic UI Styling ---
st.set_page_config(
    page_title="⚛️ Quantora",
    page_icon=":neuron:",
    layout="wide",
    initial_sidebar_state="expanded", # Sidebar will be open by default
)

# Custom CSS (same as before)
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

        .st-emotion-cache-16txtl3 { /* Link style - now a button */
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

        .image-container {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            overflow-x: auto; /* Enable horizontal scrolling for many images */
        }

        .image-container img {
            max-width: 150px;
            height: auto;
            border-radius: 4px;
            box-shadow: 2px 2px 5px #00000020;
        }

        .inline-iframe-container {
            width: 100%;
            height: 400px; /* Adjust height as needed */
            border: 1px solid #384459;
            border-radius: 8px;
            margin-top: 10px;
            margin-bottom: 15px;
        }

        .inline-iframe-container iframe {
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 8px;
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

# --- Sidebar Navigation ---
with st.sidebar:
    st.header("Quantora Navigation")
    page = st.radio(
        "Explore:",
        ["Insights", "Visual Media", "Marketplace"],
    )

    if page == "Insights":
        st.session_state['current_page'] = "insights"
    elif page == "Visual Media":
        st.session_state['current_page'] = "visual_media"
    elif page == "Marketplace":
        st.session_state['current_page'] = "marketplace"

    st.markdown("---")
    st.markdown("<p style='color:#d1d5db; font-size:12px;'>Powered by Quantora</p>", unsafe_allow_html=True)

# --- Main Application Logic Based on Sidebar Selection ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "insights" # Default page
    st.session_state['last_search_query'] = ""

if st.session_state['current_page'] == "insights":
    st.title("⚛️ Quantora Search Engine")
    st.subheader("Intelligent Information Synthesis")

    query = st.text_input("Enter your Quantora query:", "")

    if query:
        st.session_state['last_search_query'] = query # Store the search query
        st.info(f"Quantora is processing your request for: '{query}'...")

        # Fetch search results
        results = fetch_quantora_results(query, API_KEY, SEARCH_ENGINE_ID, num=3) # Reduced number of text results

        st.subheader("Quantora Insights:")
        if results:
            for i, result in enumerate(results):
                title = result.get('title', 'No Title')
                link = result.get('link', '#')
                snippet = result.get('snippet', 'No Description')

                st.markdown(f"<div class='st-emotion-cache-r421ms'><strong>{i+1}. {title}</strong></div>", unsafe_allow_html=True)
                st.markdown(f"<p class='st-emotion-cache-10pw50'>{snippet}</p>", unsafe_allow_html=True)
                if st.button(f"View: {link}", key=f"view_link_{i}"):
                    st.session_state['inline_iframe_url'] = link
                    st.rerun()
                if 'inline_iframe_url' in st.session_state and st.session_state['inline_iframe_url'] == link:
                    st.markdown(f"<div class='inline-iframe-container'><iframe src='{link}'></iframe></div>", unsafe_allow_html=True)
                    del st.session_state['inline_iframe_url']
                st.divider()
        else:
            st.warning("Quantora found no relevant insights for this query.")

elif st.session_state['current_page'] == "visual_media":
    st.title("🖼️ Quantora Visual Media Hub")
    if 'last_search_query' in st.session_state and st.session_state['last_search_query']:
        st.subheader(f"Related Images for: '{st.session_state['last_search_query']}'")
        image_results = fetch_image_results(st.session_state['last_search_query'], API_KEY, SEARCH_ENGINE_ID, num_images=10) # Increased number of images
        if image_results:
            st.markdown("<div class='image-container'>", unsafe_allow_html=True)
            for image_result in image_results:
                image_url = image_result.get('link')
                if image_url:
                    st.markdown(f"<img src='{image_url}' alt='Related Image'>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(f"No related images found for '{st.session_state['last_search_query']}'.")
    else:
        st.info("Search for a topic on the 'Insights' page to see related images here.")

elif st.session_state['current_page'] == "marketplace":
    st.title("🛒 Quantora Marketplace")
    query = st.session_state.get('last_search_query', '')
    if query:
        shopping_query = f"{query} buy shop price" # Append shopping-related keywords
        st.subheader(f"Shopping Results for: '{query}'")
        shopping_results = fetch_quantora_results(shopping_query, API_KEY, SEARCH_ENGINE_ID, num=5) # Fetch potential shopping results
        if shopping_results:
            for i, result in enumerate(shopping_results):
                title = result.get('title', 'No Product Title')
                link = result.get('link', '#')
                snippet = result.get('snippet', 'No Description Available')
                st.markdown(f"<div class='st-emotion-cache-r421ms'><strong>{i+1}. {title}</strong></div>", unsafe_allow_html=True)
                st.markdown(f"<a class='st-emotion-cache-16txtl3' href='{link}' target='_blank'>{link}</a>", unsafe_allow_html=True) # Open in new tab for shopping
                st.markdown(f"<p class='st-emotion-cache-10pw50'>{snippet}</p>", unsafe_allow_html=True)
                st.divider()
        else:
            st.info(f"No specific shopping results found for '{query}'.")
    else:
        st.info("Search for a topic on the 'Insights' page to see potential shopping options here.")
