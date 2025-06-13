import streamlit as st
from googleapiclient.discovery import build
import base64
import json
import time

# --- API Configuration ---
API_KEY = "AIzaSyCZ-1xA0qHy7p3l5VdZYCrvoaQhpMZLjig"
SEARCH_ENGINE_ID = "c38572640fa0441bc"

# --- Page Configuration ---
st.set_page_config(
    page_title="⚛️ Quantora - Advanced Search Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Functions ---
@st.cache_data(show_spinner=False)
def fetch_quantora_results(search_term, api_key, cse_id, **kwargs):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res.get("items", [])
    except Exception as e:
        st.error(f"Search error: {e}")
        return []

@st.cache_data(show_spinner=False)
def fetch_image_results(search_term, api_key, cse_id, num_images=8):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, searchType='image', num=num_images).execute()
        return res.get("items", [])
    except Exception as e:
        return []

# --- Initialize Session State ---
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "web"

# --- Premium UI HTML/CSS/JS ---
premium_ui = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --dark-gradient: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
    --glass-bg: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.1);
    --text-primary: #ffffff;
    --text-secondary: #b8bcc8;
    --accent-blue: #00d4ff;
    --accent-purple: #8b5cf6;
    --accent-pink: #ec4899;
    --success-green: #10b981;
    --warning-orange: #f59e0b;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body, .stApp {
    background: var(--dark-gradient);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
    overflow-x: hidden;
}

/* Animated Background */
.animated-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: var(--dark-gradient);
}

.animated-bg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(120, 219, 226, 0.2) 0%, transparent 50%);
    animation: backgroundShift 20s ease-in-out infinite;
}

@keyframes backgroundShift {
    0%, 100% { transform: translateX(0) translateY(0); }
    25% { transform: translateX(-10px) translateY(-5px); }
    50% { transform: translateX(10px) translateY(5px); }
    75% { transform: translateX(-5px) translateY(10px); }
}

/* Header Styles */
.quantora-header {
    text-align: center;
    padding: 2rem 0;
    position: relative;
}

.quantora-logo {
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    animation: logoGlow 3s ease-in-out infinite alternate;
}

@keyframes logoGlow {
    from { filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.3)); }
    to { filter: drop-shadow(0 0 30px rgba(139, 92, 246, 0.5)); }
}

.quantora-tagline {
    font-size: 1.2rem;
    color: var(--text-secondary);
    font-weight: 300;
    margin-bottom: 2rem;
}

/* Search Container */
.search-container {
    max-width: 800px;
    margin: 0 auto 3rem;
    padding: 0 2rem;
}

.search-box {
    position: relative;
    margin-bottom: 2rem;
}

.search-input {
    width: 100%;
    padding: 1.5rem 6rem 1.5rem 2rem;
    font-size: 1.1rem;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 25px;
    color: var(--text-primary);
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
    outline: none;
    font-family: inherit;
}

.search-input:focus {
    border-color: var(--accent-blue);
    box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
    transform: translateY(-2px);
}

.search-input::placeholder {
    color: var(--text-secondary);
}

.search-btn {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    background: var(--primary-gradient);
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 20px;
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.search-btn:hover {
    transform: translateY(-50%) scale(1.05);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

/* Tab Navigation */
.tab-navigation {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 2rem 0;
    flex-wrap: wrap;
}

.tab-btn {
    padding: 0.8rem 2rem;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 15px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    font-weight: 500;
    position: relative;
    overflow: hidden;
}

.tab-btn.active {
    background: var(--primary-gradient);
    color: white;
    border-color: transparent;
}

.tab-btn:hover:not(.active) {
    color: var(--text-primary);
    border-color: var(--accent-blue);
    transform: translateY(-2px);
}

/* Results Container */
.results-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.result-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--primary-gradient);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.result-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    border-color: var(--accent-blue);
}

.result-card:hover::before {
    transform: scaleX(1);
}

.result-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--accent-blue);
    margin-bottom: 0.5rem;
    text-decoration: none;
    transition: color 0.3s ease;
}

.result-title:hover {
    color: var(--accent-purple);
}

.result-url {
    color: var(--success-green);
    font-size: 0.9rem;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
}

.result-snippet {
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: 1rem;
}

/* Image Grid */
.image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.image-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 15px;
    overflow: hidden;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.image-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.image-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.image-card:hover img {
    transform: scale(1.1);
}

/* Shopping Cards */
.shopping-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.shopping-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    overflow: hidden;
    transition: all 0.3s ease;
    backdrop-filter: blur(20px);
    position: relative;
}

.shopping-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

.shopping-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    background: linear-gradient(45deg, #f0f0f0, #e0e0e0);
}

.shopping-content {
    padding: 1.5rem;
}

.shopping-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    line-height: 1.4;
}

.shopping-price {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--accent-blue);
    margin-bottom: 1rem;
}

.shopping-description {
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 1rem;
}

.shop-btn {
    width: 100%;
    padding: 0.8rem;
    background: var(--secondary-gradient);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.shop-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(240, 147, 251, 0.4);
}

/* Loading Animation */
.loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
    flex-direction: column;
    gap: 1rem;
}

.loading-spinner {
    width: 50px;
    height: 50px;
    border: 3px solid var(--glass-border);
    border-top: 3px solid var(--accent-blue);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-text {
    color: var(--text-secondary);
    font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
    .quantora-logo {
        font-size: 2.5rem;
    }
    
    .search-input {
        padding: 1.2rem 5rem 1.2rem 1.5rem;
        font-size: 1rem;
    }
    
    .tab-navigation {
        gap: 0.5rem;
    }
    
    .tab-btn {
        padding: 0.6rem 1.5rem;
        font-size: 0.9rem;
    }
    
    .result-card {
        padding: 1.5rem;
    }
    
    .image-grid {
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .shopping-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
}

/* Utility Classes */
.text-gradient {
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.glass-effect {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
}

.hover-lift {
    transition: transform 0.3s ease;
}

.hover-lift:hover {
    transform: translateY(-5px);
}

/* Hide Streamlit elements */
.stApp > header {
    display: none;
}

.stApp > footer {
    display: none;
}

#MainMenu {
    display: none;
}

.stDeployButton {
    display: none;
}

.stDecoration {
    display: none;
}

</style>

<div class="animated-bg"></div>

<div class="quantora-header">
    <div class="quantora-logo">⚛️ QUANTORA</div>
    <div class="quantora-tagline">Advanced Search Intelligence • Discover • Explore • Shop</div>
</div>

<script>
// Add interactive background particles
function createParticles() {
    const container = document.querySelector('.animated-bg');
    if (!container) return;
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 2px;
            background: rgba(0, 212, 255, 0.5);
            border-radius: 50%;
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            animation: float ${5 + Math.random() * 10}s ease-in-out infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        container.appendChild(particle);
    }
}

// Floating animation for particles
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% { transform: translateY(0px) translateX(0px); opacity: 0; }
        10%, 90% { opacity: 1; }
        50% { transform: translateY(-20px) translateX(10px); }
    }
`;
document.head.appendChild(style);

// Initialize particles when page loads
setTimeout(createParticles, 1000);

// Add smooth scrolling
document.addEventListener('DOMContentLoaded', function() {
    document.documentElement.style.scrollBehavior = 'smooth';
});
</script>
"""

# --- Render Premium UI ---
st.markdown(premium_ui, unsafe_allow_html=True)

# --- Search Interface ---
search_col1, search_col2 = st.columns([6, 1])

with search_col1:
    search_query = st.text_input(
        "",
        value=st.session_state.search_query,
        placeholder="🔍 Enter your search query...",
        key="main_search",
        label_visibility="collapsed"
    )

with search_col2:
    search_clicked = st.button("🚀 Search", key="search_btn", use_container_width=True)

# --- Tab Navigation ---
tab_col1, tab_col2, tab_col3, tab_col4 = st.columns(4)

with tab_col1:
    if st.button("🌐 Web Results", key="web_tab", use_container_width=True):
        st.session_state.current_tab = "web"

with tab_col2:
    if st.button("🖼️ Images", key="images_tab", use_container_width=True):
        st.session_state.current_tab = "images"

with tab_col3:
    if st.button("🛒 Shopping", key="shopping_tab", use_container_width=True):
        st.session_state.current_tab = "shopping"

with tab_col4:
    if st.button("📰 News", key="news_tab", use_container_width=True):
        st.session_state.current_tab = "news"

# --- Search Logic ---
if search_clicked and search_query:
    st.session_state.search_query = search_query
    
    # Show loading animation
    with st.spinner("🔍 Quantora is processing your query..."):
        if st.session_state.current_tab == "web":
            st.session_state.search_results = fetch_quantora_results(
                search_query, API_KEY, SEARCH_ENGINE_ID, num=10
            )
        elif st.session_state.current_tab == "images":
            st.session_state.search_results = fetch_image_results(
                search_query, API_KEY, SEARCH_ENGINE_ID, num_images=16
            )
        elif st.session_state.current_tab == "shopping":
            shopping_query = f"{search_query} buy shop price store"
            st.session_state.search_results = fetch_quantora_results(
                shopping_query, API_KEY, SEARCH_ENGINE_ID, num=12
            )
        elif st.session_state.current_tab == "news":
            news_query = f"{search_query} news latest"
            st.session_state.search_results = fetch_quantora_results(
                news_query, API_KEY, SEARCH_ENGINE_ID, num=10
            )

# --- Display Results ---
if st.session_state.search_query and st.session_state.search_results:
    
    # Results count
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0; color: var(--text-secondary);">
        Found <span style="color: var(--accent-blue); font-weight: 600;">{len(st.session_state.search_results)}</span> 
        results for "<span style="color: var(--text-primary);">{st.session_state.search_query}</span>"
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.current_tab == "web":
        # Web Results
        for i, result in enumerate(st.session_state.search_results):
            title = result.get('title', 'No Title')
            link = result.get('link', '#')
            snippet = result.get('snippet', 'No description available')
            
            st.markdown(f"""
            <div class="result-card">
                <a href="{link}" target="_blank" class="result-title">{title}</a>
                <div class="result-url">{link}</div>
                <div class="result-snippet">{snippet}</div>
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.current_tab == "images":
        # Image Results
        st.markdown('<div class="image-grid">', unsafe_allow_html=True)
        
        cols = st.columns(4)
        for i, result in enumerate(st.session_state.search_results):
            image_url = result.get('link', '')
            title = result.get('title', 'Image')
            
            with cols[i % 4]:
                try:
                    st.image(image_url, caption=title[:50] + "..." if len(title) > 50 else title)
                except:
                    st.info("Image unavailable")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.current_tab == "shopping":
        # Shopping Results
        st.markdown('<div class="shopping-grid">', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, result in enumerate(st.session_state.search_results):
            title = result.get('title', 'Product')
            link = result.get('link', '#')
            snippet = result.get('snippet', 'No description available')
            
            # Try to get product image
            try:
                image_results = fetch_image_results(title, API_KEY, SEARCH_ENGINE_ID, num_images=1)
                image_url = image_results[0].get('link') if image_results else None
            except:
                image_url = None
            
            with cols[i % 3]:
                st.markdown(f"""
                <div class="shopping-card">
                    {f'<img src="{image_url}" class="shopping-image" alt="{title}">' if image_url else '<div class="shopping-image" style="background: linear-gradient(45deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem;">🛒</div>'}
                    <div class="shopping-content">
                        <div class="shopping-title">{title[:80]}{'...' if len(title) > 80 else ''}</div>
                        <div class="shopping-description">{snippet[:100]}{'...' if len(snippet) > 100 else ''}</div>
                        <a href="{link}" target="_blank">
                            <button class="shop-btn">View Product →</button>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.current_tab == "news":
        # News Results
        for i, result in enumerate(st.session_state.search_results):
            title = result.get('title', 'No Title')
            link = result.get('link', '#')
            snippet = result.get('snippet', 'No description available')
            
            st.markdown(f"""
            <div class="result-card">
                <a href="{link}" target="_blank" class="result-title">📰 {title}</a>
                <div class="result-url">{link}</div>
                <div class="result-snippet">{snippet}</div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.search_query and not st.session_state.search_results:
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0; color: var(--text-secondary);">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">No results found</div>
        <div>Try different keywords or check your spelling</div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Welcome message
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0; color: var(--text-secondary);">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🚀</div>
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">Welcome to Quantora</div>
        <div>Your advanced search intelligence platform</div>
        <div style="margin-top: 2rem;">
            <div style="display: inline-block; margin: 0 1rem; padding: 1rem; background: var(--glass-bg); border-radius: 10px; backdrop-filter: blur(10px);">
                <div style="font-size: 1.5rem;">🌐</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">Web Search</div>
            </div>
            <div style="display: inline-block; margin: 0 1rem; padding: 1rem; background: var(--glass-bg); border-radius: 10px; backdrop-filter: blur(10px);">
                <div style="font-size: 1.5rem;">🖼️</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">Image Search</div>
            </div>
            <div style="display: inline-block; margin: 0 1rem; padding: 1rem; background: var(--glass-bg); border-radius: 10px; backdrop-filter: blur(10px);">
                <div style="font-size: 1.5rem;">🛒</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">Shopping</div>
            </div>
            <div style="display: inline-block; margin: 0 1rem; padding: 1rem; background: var(--glass-bg); border-radius: 10px; backdrop-filter: blur(10px);">
                <div style="font-size: 1.5rem;">📰</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">News</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style="text-align: center; margin: 4rem 0 2rem; padding: 2rem; border-top: 1px solid var(--glass-border);">
    <div style="color: var(--text-secondary); font-size: 0.9rem;">
        Powered by <span class="text-gradient" style="font-weight: 600;">Quantora Advanced Search Intelligence</span>
    </div>
    <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.5rem;">
        Built with ⚛️ Modern Web Technologies
    </div>
</div>
""", unsafe_allow_html=True)
