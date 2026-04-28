import streamlit as st
import requests

# --- 1. LOGO & BRANDING ---
# You can use a local file path like "logo.png" or a direct URL
LOGO_URL = ""https://kommodo.ai/i/89Px4YyuczTa43MwDSTJ/logo.png" 

# --- 2. PRODUCT DATABASE ---
products = [
    {"name": "BB-gun", "price": 25, "img": "https://makerworld.bblmw.com/makerworld/model/US18955f0fc513e5/design/2024-01-03_201b2ae71df09.jpg?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "6mm Cartridge", "price": 5, "img": "https://makerworld.bblmw.com/makerworld/model/US4eb0d6d10832a/design/2025-02-21_3d58e70697ae1.jpg"},
    {"name": "Gatling gun", "price": 30, "img": "https://makerworld.bblmw.com/makerworld/model/US92c5fd98860546/design/2025-01-20_b0744fb62f5f2.gif?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "BB-ammo", "price": 0.50, "img": "https://makerworld.bblmw.com/makerworld/model/US14a586903f14f8/design/2025-05-15_b41c34cbd23cb.jpg?x-oss-process=image/resize,w_1000/format,webp"}
]

colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

# --- 3. SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# --- 4. DISPLAY LOGO ---
# Option A: Sidebar Logo (This appears at the top of the sidebar)
st.logo(LOGO_URL, icon_image=LOGO_URL) 

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.title("🛠️ Luca's 3D Lab")
menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Checkout"])

# Sidebar Cart Display...
# (Rest of your sidebar logic remains the same)

# --- 6. MAIN PAGE LOGO ---
if menu == "Browse Catalog":
    # Option B: Main Page Logo (Centered or Left-aligned)
    col_logo, col_text = st.columns([1, 4])
    with col_logo:
        st.image(LOGO_URL, width=100) # Adjust width as needed
    with col_text:
        st.title("🚀 Luca's Custom 3D Prints")
    
    st.write("Pick a model, choose your color, and add it to your cart!")

    # (Rest of your product grid logic remains the same)
    # ...
