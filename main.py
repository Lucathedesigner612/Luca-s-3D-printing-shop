import streamlit as st
import requests

# --- 1. CONFIG & SETTINGS ---
# Replace with your real Revolut Merchant Secret Key in Streamlit Secrets
if "REVOLUT_SECRET_KEY" in st.secrets:
    REV_KEY = st.secrets["REVOLUT_SECRET_KEY"]
else:
    REV_KEY = "your_sk_here" 

LOGO_URL = "https://kommodo.ai/i/89Px4YyuczTa43MwDSTJ/logo.png"

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# CSS to fix image heights and align buttons/dropdowns perfectly
st.markdown("""
    <style>
    [data-testid="stImage"] img {
        height: 250px;
        object-fit: cover;
        border-radius: 10px;
    }
    .product-title {
        height: 50px;
        overflow: hidden;
        font-weight: bold;
        line-height: 1.2;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PRODUCT DATABASE ---
products = [
    {"name": "BB-gun", "price": 25, "img": "https://makerworld.bblmw.com/makerworld/model/US18955f0fc513e5/design/2024-01-03_201b2ae71df09.jpg?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "6mm Cartridge", "price": 5, "img": "https://makerworld.bblmw.com/makerworld/model/US4eb0d6d10832a/design/2025-02-21_3d58e70697ae1.jpg"},
    {"name": "Gatling gun", "price": 30, "img": "https://makerworld.bblmw.com/makerworld/model/US92c5fd98860546/design/2025-01-20_b0744fb62f5f2.gif?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "BB-ammo", "price": 0.50, "img": "https://makerworld.bblmw.com/makerworld/model/US14a586903f14f8/design/2025-05-15_b41c34cbd23cb.jpg?x-oss-process=image/resize,w_1000/format,webp"},
  
]

colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

# --- 3. SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- 4. SIDEBAR (Navigation, Cart, & Contact) ---
st.sidebar.image(LOGO_URL, use_container_width=True)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Browse Catalog", "Checkout"])

st.sidebar.divider()
st.sidebar.subheader("🛒 Your Cart")
if not st.session_state.cart:
    st.sidebar.write("Cart is empty.")
else:
    total_cart = sum(item['price'] for item in st.session_state.cart)
    for item in st.session_state.cart:
        st.sidebar.write(f"• {item['display_name']} (€{item['price']})")
    st.sidebar.write(f"**Total: €{total_cart}**")
    if st.sidebar.button("🗑️ Clear Cart"):
        st.session_state.cart = []
        st.rerun()

st.sidebar.divider()
st.sidebar.subheader("✉️ Custom Request")
with st.sidebar.form("contact_form", clear_on_submit=True):
    u_email = st.text_input("Your Email")
    u_msg = st.text_area("Describe your project")
    u_submit = st.form_submit_button("Send to Luca")
    if u_submit:
        if u_email and u_msg:
            # Change this to your real email
            requests.post("lucagalea612@gmail.com", 
                          data={"email": u_email, "message": u_msg})
            st.sidebar.success("Message sent!")
        else:
            st.sidebar.error("Fill in all fields.")

# --- 5. PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    col_l, col_r = st.columns([1, 6])
    with col_l:
        st.image(LOGO_URL, width=80)
    with col_r:
        st.title("Luca's Custom 3D Prints")
    
    st.write("Select a model and color to add to your order.")
    st.divider()

    # 3x3 Grid Logic
    rows = st.columns(3)
    for i, p in enumerate(products):
        with rows[i % 3]:
            st.image(p["img"], use_container_width=True)
