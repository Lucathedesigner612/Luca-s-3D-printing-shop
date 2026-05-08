import streamlit as st
import requests

# --- 1. CONFIG & SETTINGS ---
# Set your Revolut Secret Key in the "Secrets" tab of Streamlit Cloud
if "REVOLUT_SECRET_KEY" in st.secrets:
    REV_KEY = st.secrets["REVOLUT_SECRET_KEY"]
else:
    REV_KEY = "your_sk_here" 

# If this link fails, upload 'logo.png' to GitHub and change this to "logo.png"
LOGO_URL = "https://kommodo.ai/i/89Px4YyuczTa43MwDSTJ/logo.png"

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# CSS: This fixes image heights, crops them neatly, and aligns buttons
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
# --- 2. PRODUCT DATABASE (Local Files) ---
products = [
    {"name": "BB-gun", "price": 25, "img": "gun.jpg"},
    {"name": "6mm Cartridge", "price": 5, "img": "cartridge.jpg"},
    {"name": "Gatling gun", "price": 30, "img": "gatling.jpg"},
    {"name": "BB-ammo", "price": 0.50, "img": "ammo.jpg"},
    {"name": "Hayabusa Motorcycle", "price": 45, "img": "bike.jpg"}
]


colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

# --- 3. SESSION STATE (CART) ---
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- 4. SIDEBAR (Navigation, Cart & Contact) ---
try:
    st.sidebar.image(LOGO_URL, use_container_width=True)
except:
    st.sidebar.header("🛠️ Luca's 3D Lab")

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

# CONTACT FORM - Fixed Indentation
with st.sidebar.form("contact_form", clear_on_submit=True):
    u_email = st.text_input("Your Email")
    u_msg = st.text_area("Describe your project")
    u_submit = st.form_submit_button("Send to Luca")

# Send Logic - Aligned with the 'with' block
if u_submit:
    if u_email and u_msg:
        try:
            response = requests.post(
                "https://formsubmit.co/ajax/lucagalea612@gmail.com", 
                data={"email": u_email, "message": u_msg}
            )
            if response.status_code == 200:
                st.sidebar.success("Sent! Check your email to confirm.")
            else:
                st.sidebar.error("Failed to send.")
        except:
            st.sidebar.error("Service unavailable.")
    else:
        st.sidebar.error("Fill in all fields.")

# --- 5.
