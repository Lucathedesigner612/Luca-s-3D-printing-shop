import streamlit as st
import requests

# --- 1. CONFIG & SETTINGS ---
# Using a more standard placeholder if your link is broken
LOGO_URL = "https://kommodo.ai/i/89Px4YyuczTa43MwDSTJ/logo.png"

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# CSS to fix image heights and align buttons/dropdowns
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
    {"name": "Hayabusa Motorcycle", "price": 45, "img": "https://makerworld.bblmw.com/makerworld/model/US095904d60c41/design/2024-06-12_6d8f8a8b8b8b8.jpg"}
]

colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

# --- 3. SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- 4. SIDEBAR ---
# FIXED: Only show logo if the URL works, otherwise show text
try:
    st.sidebar.image(LOGO_URL, use_container_width=True)
except:
    st.sidebar.title("🛠️ Luca's 3D Lab")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Browse Catalog", "Checkout"])

# --- CONTACT FORM ---
st.sidebar.divider()
st.sidebar.subheader("✉️ Custom Request")

# The Form
with st.sidebar.form("contact_form", clear_on_submit=True):
    u_email = st.text_input("Your Email (so Luca can reply)")
    u_msg = st.text_area("What would you like me to print?")
    u_submit = st.form_submit_button("Send Request")

# The Logic (Aligned with 'with')
if u_submit:
    if u_email and u_msg:
        try:
            # This sends the data to FormSubmit, which forwards it to you
           # Make sure it says /ajax/ and has your full email
           requests.post("https://formsubmit.co/ajax/lucagalea612@gmail.com", 
              data={"Customer Email": u_email, "Message": u_msg})
               
            
            if response.status_code == 200:
                st.sidebar.success("Sent! Check your email soon, Luca will reply.")
            else:
                st.sidebar.error("Send failed. Please try again.")
        except Exception as e:
            st.sidebar.error("Could not connect to the mail server.")
    else:
        st.sidebar.error("Please fill in both fields!")

# --- 5. PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    col_l, col_r = st.columns([1, 6])
    with col_l:
        # FIXED: Added width=80 explicitly to avoid NameError
        st.image(LOGO_URL, width=80) 
    with col_r:
        st.title("Luca's Custom 3D Prints")
    
    st.write("Select a model and color to add to your order.")
    st.divider()

    # 3x3 Grid
    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i % 3]:
            # Use try/except so one broken image doesn't crash the whole shop
            try:
                st.image(p["img"], use_container_width=True)
            except:
                st.warning("Image failed to load")
                
            st.markdown(f"<div class='product-title'>{p['name']}</div>", unsafe_allow_html=True)
            sel_color = st.selectbox(f"Color", colors, key=f"c_{i}", label_visibility="collapsed")
            st.write(f"**€{p['price']}**")
            
            if st.button(f"Add to Cart", key=f"b_{i}", use_container_width=True):
                st.session_state.cart.append({"display_name": f"{p['name']} ({sel_color})", "price": p["price"]})
                st.toast(f"Added {p['name']}!")
                st.rerun()
