import streamlit as st
import requests

# --- 1. CONFIG & SETTINGS ---
# Set your REVOLUT_SECRET_KEY in the "Secrets" tab of Streamlit Cloud
if "REVOLUT_SECRET_KEY" in st.secrets:
    REV_KEY = st.secrets["REVOLUT_SECRET_KEY"]
else:
    REV_KEY = "your_sk_here" 

# PRO TIP: Upload 'logo.png' to GitHub and change this to "logo.png" for better reliability
LOGO_URL = "https://kommodo.ai/i/89Px4YyuczTa43MwDSTJ/logo.png"

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# CSS: Fixes image heights and aligns UI elements
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

# --- CONTACT FORM SECTION ---
# Fixed indentation for the entire block
with st.sidebar.form("contact_form", clear_on_submit=True):
    u_email = st.text_input("Your Email")
    u_msg = st.text_area("Describe your project")
    u_submit = st.form_submit_button("Send to Luca")

# Logic must be OUTSIDE the 'with' block, aligned with the 'w' in 'with'
if u_submit:
    if u_email and u_msg:
        try:
            # Correct URL format for FormSubmit AJAX
            response = requests.post(
                "https://formsubmit.co/ajax/lucagalea612@gmail.com", 
                data={"email": u_email, "message": u_msg}
            )
            if response.status_code == 200:
                st.sidebar.success("Sent! Luca, check your inbox/spam now.")
            else:
                st.sidebar.error("Failed to send.")
        except:
            st.sidebar.error("Service unavailable.")
    else:
        st.sidebar.error("Fill in all fields.")

# --- 5. PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    col_l, col_r = st.columns([1, 6])
    with col_l:
        # Fixed NameError by using width=80
        try:
            st.image(LOGO_URL, width=80) 
        except:
            st.write("🛠️")
    with col_r:
        st.title("Luca's Custom 3D Prints")
    
    st.write("Select a model and color to add to your order.")
    st.divider()

    # 3x3 Grid Logic
    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i % 3]:
            try:
                st.image(p["img"], use_container_width=True)
            except:
                st.error("Image loading failed.")
                
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
                st.error("Set your REVOLUT_SECRET_KEY in Streamlit Secrets!")
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
                        st.error(f"Revolut Error: {data.get('message', 'Check API Key')}")
                except Exception as e:
                    st.error(f"Payment failed: {e}")
