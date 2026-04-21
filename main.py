import streamlit as st
import requests

# --- 1. PRODUCT DATABASE ---
# Add or remove your 3D models here
products = [
    {"name": "BB-gun", "price": 25, "img": "https://makerworld.bblmw.com/makerworld/model/US18955f0fc513e5/design/2024-01-03_201b2ae71df09.jpg?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "6mm Cartridge", "price": 5, "img": "https://makerworld.bblmw.com/makerworld/model/US4eb0d6d10832a/design/2025-02-21_3d58e70697ae1.jpg"},
    {"name": "Gatling gun", "price": 30, "img": "https://makerworld.bblmw.com/makerworld/model/US92c5fd98860546/design/2025-01-20_b0744fb62f5f2.gif?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "BB-ammo", "price": 0.50, "img": "https://makerworld.bblmw.com/makerworld/model/US14a586903f14f8/design/2025-05-15_b41c34cbd23cb.jpg?x-oss-process=image/resize,w_1000/format,webp"}
]

colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

# --- 2. CONFIG & SECRETS ---
# Replace with your real Revolut Merchant Secret Key
# Better: Add REVOLUT_SECRET_KEY to your Streamlit Secrets
if "REVOLUT_SECRET_KEY" in st.secrets:
    REV_KEY = st.secrets["REVOLUT_SECRET_KEY"]
else:
    REV_KEY = "your_sk_here" 

# --- 3. SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# --- 4. SIDEBAR (Cart Summary) ---
st.sidebar.title("🛠️ Luca's 3D Lab")
menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Checkout"])

st.sidebar.divider()
st.sidebar.subheader("🛒 Your Cart")

if not st.session_state.cart:
    st.sidebar.write("Empty")
else:
    total_cart = sum(item['price'] for item in st.session_state.cart)
    for i, item in enumerate(st.session_state.cart):
        st.sidebar.write(f"**{item['display_name']}** (€{item['price']})")
    
    st.sidebar.write(f"### Total: €{total_cart}")
    if st.sidebar.button("🗑️ Clear"):
        st.session_state.cart = []
        st.rerun()

# --- 5. PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    st.title("🚀 Custom 3D Prints")
    st.write("Pick your model and color, then head to Checkout.")

    col1, col2 = st.columns(2)
    for i, p in enumerate(products):
        with (col1 if i % 2 == 0 else col2):
            st.image(p["img"], use_container_width=True)
            st.subheader(p["name"])
            
            # Options
            sel_color = st.selectbox(f"Color for {p['name']}", colors, key=f"c_{i}")
            st.write(f"**Price: €{p['price']}**")
            
            if st.button(f"Add to Cart", key=f"b
