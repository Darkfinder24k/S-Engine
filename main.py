import streamlit as st
from googleapiclient.discovery import build
import base64  # For background image
import json # To handle structured data (hypothetical)

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
def fetch_image_results(search_term, api_key, cse_id, num_images=1): # Fetching only 1 image per shopping item
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

# Custom CSS - Enhanced with animations and more refined elements
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        body {
            background-color: #0a0b0e;
            color: #f0f8ff;
            font-family: 'Montserrat', sans-serif;
            overflow-x: hidden; /* Prevent horizontal scrollbar */
        }

        .stApp {
            background-color: transparent;
        }

        .stTextInput > div > div > input {
            background-color: #1e212b;
            color: #f0f8ff;
            border: 1px solid #384459;
            border-radius: 12px; /* More rounded */
            padding: 12px 20px; /* Increased padding */
            font-size: 16px;
            transition: border-color 0.3s ease;
        }

        .stTextInput > div > div > input:focus {
            border-color: #a78bfa;
            outline: none;
            box-shadow: 0 0 8px rgba(167, 139, 250, 0.5);
        }

        .stButton > button {
            background-color: #a78bfa;
            color: #f0f8ff;
            border: none;
            border-radius: 12px; /* More rounded */
            padding: 14px 28px; /* Increased padding */
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .stButton > button:hover {
            background-color: #8b5cf6;
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
        }

        .marketplace-item {
            display: flex;
            align-items: center;
            background-color: #1e212b;
            color: #f0f8ff;
            padding: 20px; /* Increased padding */
            margin-bottom: 20px; /* Increased margin */
            border-radius: 12px; /* More rounded */
            border: 1px solid #384459;
            animation: fadeIn 0.5s ease forwards;
        }

        .marketplace-item-details {
            flex-grow: 1;
            margin-right: 20px; /* Increased margin */
        }

        .marketplace-item-image {
            max-width: 120px; /* Slightly larger image */
            height: auto;
            border-radius: 8px;
            box-shadow: 3px 3px 8px #00000020;
            animation: pulse 2s infinite alternate;
        }

        .marketplace-item strong {
            font-size: 1.2em; /* Slightly larger font */
            color: #bae6fd; /* Accent color for emphasis */
        }

        .marketplace-item a {
            color: #a78bfa; /* Consistent accent color */
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .marketplace-item a:hover {
            text-decoration: underline;
            color: #d8b4fe;
        }

        .marketplace-item p {
            color: #d1d5db;
            font-size: 0.95em; /* Slightly larger font */
            line-height: 1.6; /* Improved readability */
        }

        h1, h2, h3 {
            color: #f0f8ff;
            letter-spacing: 0.5px; /* Subtle spacing for a modern look */
        }

        .sidebar .sidebar-content {
            background-color: #1e212b;
            color: #f0f8ff;
            border-radius: 10px;
            padding: 20px;
        }

        .sidebar h2 {
            color: #a78bfa;
            margin-bottom: 15px;
        }

        .sidebar-radio > label {
            color: #d1d5db;
            font-size: 16px;
            padding: 8px 15px;
            border-radius: 8px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        .sidebar-radio > label:hover {
            background-color: #384459;
            color: #a78bfa;
        }

        .inline-iframe-container {
            width: 100%;
            height: 900px; /* Further increased height */
            border: 1px solid #384459;
            border-radius: 12px;
            margin-top: 15px; /* Increased margin */
            margin-bottom: 20px; /* Increased margin */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .inline-iframe-container iframe {
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 12px;
        }

        .st-emotion-cache-r421ms strong { /* Style for result titles */
            color: #a78bfa;
            font-size: 1.15em;
        }

        .st-emotion-cache-10pw50 { /* Style for result snippets */
            color: #d1d5db;
            font-size: 0.9em;
            line-height: 1.5;
        }

        .image-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); /* Responsive image grid */
            gap: 15px;
            margin-top: 15px;
        }

        .image-container img {
            width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease-in-out;
        }

        .image-container img:hover {
            transform: scale(1.05);
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
    st.header("⚛️ Quantora Navigation")
    page = st.radio(
        "Explore:",
        ["Insights", "Visual Media", "Marketplace"],
        label_visibility="collapsed" # Clean up radio button labels
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

elif st.session_state['current_page'] == "insights":
    st.title("⚛️ Quantora Insights")
    st.subheader("Uncover Intelligent Information")

    query = st.text_input("Enter your Quantora query:", st.session_state.get('last_search_query', ""), placeholder="Explore the universe...", key="insights_query")

    if query:
        st.session_state['last_search_query'] = query # Store the search query
        with st.spinner(f"Quantora is synthesizing insights for '{query}'..."):
            results = fetch_quantora_results(query, API_KEY, SEARCH_ENGINE_ID, num=5) # Slightly increased results

        if results:
            st.subheader("Relevant Insights:")
            for i, result in enumerate(results):
                title = result.get('title', 'No Title')
                link = result.get('link', '#')
                snippet = result.get('snippet', 'No Description')

                with st.expander(f"**{i+1}. {title}**"): # Using expander for a cleaner look
                    st.markdown(f"<p style='color:#d1d5db;'>{snippet}</p>", unsafe_allow_html=True)
                    cols = st.columns([3, 1]) # Adjust column widths
                    with cols[0]:
                        if st.button(f"Explore Further", key=f"view_link_{i}"):
                            st.session_state['inline_iframe_url'] = link
                            st.rerun()
                    with cols[1]:
                        st.markdown(f"[View Source]({link})", unsafe_allow_html=True)
            st.divider()
        else:
            st.warning("Quantora found no relevant insights for this query.")

    st.subheader("Open a Specific URL")
    direct_url = st.text_input("Enter a URL to explore directly:", "", placeholder="https://example.com", key="direct_url_input")
    open_url_button = st.button("Open URL", key="open_url_button")

    if open_url_button and direct_url:
        st.session_state['inline_iframe_url'] = direct_url
        st.rerun()

    if 'inline_iframe_url' in st.session_state and 'last_viewed_url' not in st.session_state:
        st.subheader("Website Preview:")
        st.markdown(f"<div class='inline-iframe-container'><iframe src='{st.session_state['inline_iframe_url']}'></iframe></div>", unsafe_allow_html=True)
        st.session_state['last_viewed_url'] = st.session_state['inline_iframe_url'] # To avoid re-rendering on every rerun
    elif 'inline_iframe_url' in st.session_state and st.session_state['inline_iframe_url'] != st.session_state.get('last_viewed_url'):
        st.subheader("Website Preview:")
        st.markdown(f"<div class='inline-iframe-container'><iframe src='{st.session_state['inline_iframe_url']}'></iframe></div>", unsafe_allow_html=True)
        st.session_state['last_viewed_url'] = st.session_state['inline_iframe_url']

elif st.session_state['current_page'] == "visual_media":
    st.title("🖼️ Quantora Visuals")
    if 'last_search_query' in st.session_state and st.session_state['last_search_query']:
        st.subheader(f"Related Images for: '{st.session_state['last_search_query']}'")
        with st.spinner("Fetching visual media..."):
            image_results = fetch_image_results(st.session_state['last_search_query'], API_KEY, SEARCH_ENGINE_ID, num_images=12) # More images
        if image_results:
            st.markdown("<div class='image-container'>", unsafe_allow_html=True)
            for image_result in image_results:
                image_url = image_result.get('link')
                if image_url:
                    st.image(image_url, use_column_width=True) # More integrated image display
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
        st.subheader(f"Explore Shopping Options for: '{query}'")
        with st.spinner("Searching the marketplace..."):
            shopping_results = fetch_quantora_results(shopping_query, API_KEY, SEARCH_ENGINE_ID, num=6) # More results
        if shopping_results:
            st.markdown("<div class='row'>", unsafe_allow_html=True) # Basic grid layout
            for result in shopping_results:
                title = result.get('title', 'No Product Title')
                link = result.get('link', '#')
                snippet = result.get('snippet', 'No Description Available')
                image_results = fetch_image_results(title, API_KEY, SEARCH_ENGINE_ID, num_images=1) # Fetch image for the title
                image_url = image_results[0].get('link') if image_results else None

                st.markdown(f"""
                    <div class='marketplace-item'>
                        <div class='marketplace-item-details'>
                            <strong>{title}</strong><br>
                            <a href='{link}' target='_blank'>{link}</a><br>
                            <p>{snippet}</p>
                        </div>
                        {'<img src="' + image_url + '" alt="' + title + '" class="marketplace-item-image">' if image_url else ''}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(f"No specific shopping results found for '{query}'.")
    else:
        st.info("Search for a topic on the 'Insights' page to see potential shopping options here.")
