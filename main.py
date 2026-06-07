import streamlit as st
import requests

# --- 1. CONFIG & SETTINGS ---
# Set your REVOLUT_SECRET_KEY in Streamlit Cloud Secrets
if "REVOLUT_SECRET_KEY" in st.secrets:
    REV_KEY = st.secrets["REVOLUT_SECRET_KEY"]
else:
    REV_KEY = "your_sk_here" 

# TIP: Upload 'logo.png' to your GitHub folder for this to work 100%
LOGO_URL = "logo.png" 

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# CSS: Standardizing the Shop Appearance
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
    .stButton>button {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PRODUCT DATABASE ---
# Adjust the 'img' names to match the files you upload to GitHub
products = [
    {"name": "Japanese ONI Mask", "price": 25, "img": "https://ibb.co/Qv9TSByh"},
    {"name": "6mm Cartridge", "price": 5, "img": "cartridge.jpg"},
    {"name": "Gatling gun", "price": 30, "img": "gatling.jpg"},
    {"name": "BB-ammo", "price": 0.50, "img": "ammo.jpg"},
    {"name": "Hayabusa Motorcycle", "price": 45, "img": "bike.jpg"}
]

colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

# --- 3. SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- 4. SIDEBAR ---
try:
    st.sidebar.image(LOGO_URL, use_container_width=True)
except:
    st.sidebar.title("🛠️ Luca's 3D Lab")

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

# --- ADJUSTED CONTACT FORM ---
with st.sidebar.form("contact_form", clear_on_submit=True):
    u_email = st.text_input("Your Email")
    u_msg = st.text_area("Describe your project")
    u_submit = st.form_submit_button("Send to Luca")

if u_submit:
    if u_email and u_msg:
        try:
            # ADJUSTMENT: Removing /ajax/ for the first send to force the redirect/activation
            # Change back to "https://formsubmit.co/ajax/lucagalea612@gmail.com" after you confirm!
            response = requests.post(
                "https://formsubmit.co/lucagalea612@gmail.com", 
                data={
                    "Customer": u_email, 
                    "Message": u_msg,
                    "_captcha": "false" # Bypasses the robot check
                }
            )
            if response.status_code == 200:
                st.sidebar.success("Request processed! Check your email NOW.")
            else:
                st.sidebar.error("Error connecting to mail server.")
        except:
            st.sidebar.error("Service unavailable.")
    else:
        st.sidebar.error("Please fill in both fields.")

# --- 5. PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    st.title("Luca's Custom 3D Prints")
    st.write("Pick a model, choose a color, and build your order.")
    st.divider()

    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i % 3]:
            # Image Fallback Logic
            try:
                st.image(p["img"], use_container_width=True)
            except:
                st.info(f"📸 Image: {p['img']} (Upload to GitHub to see)")
                
            st.markdown(f"<div class='product-title'>{p['name']}</div>", unsafe_allow_html=True)
            sel_color = st.selectbox(f"Color", colors, key=f"c_{i}", label_visibility="collapsed")
            st.write(f"**€{p['price']}**")
            
            if st.button(f"Add to Cart", key=f"b_{i}", use_container_width=True):
                st.session_state.cart.append({
                    "display_name": f"{p['name']} ({sel_color})",
                    "price": p["price"]
                })
                st.toast(f"Added {p['name']}!")
                st.rerun()
            st.write("") 

# --- 6. PAGE: CHECKOUT ---
elif menu == "Checkout":
    st.title("💳 Secure Checkout")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        st.write("### Review Your Order:")
        total = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"- {item['display_name']}: €{item['price']}")
        
        st.divider()
        st.write(f"## Total Amount: €{total}")

        if st.button("🚀 Pay with Apple Pay / Card", type="primary", use_container_width=True):
            if REV_KEY == "your_sk_here":
                st.error("Please set your REVOLUT_SECRET_KEY in Streamlit Secrets.")
            else:
                try:
                    payload = {"amount": int(total * 100), "currency": "EUR", "description": "3D Shop Order"}
                    headers = {"Authorization": f"Bearer {REV_KEY}", "Content-Type": "application/json"}
                    res = requests.post("https://merchant.revolut.com/api/1.0/orders", json=payload, headers=headers)
                    data = res.json()
                    
                    if "public_id" in data:
                        pay_url = f"https://checkout.revolut.com/payment?public_id={data['public_id']}"
                        st.link_button("Confirm & Pay Now", pay_url, use_container_width=True)
                    else:
                        st.error("Revolut API configuration error.")
                except:
                    st.error("Payment system offline.")
