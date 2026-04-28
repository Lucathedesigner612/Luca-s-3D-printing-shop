import streamlit as st
import requests

# --- 1. CONFIG & LOGO ---
# I've updated the URL logic to be more robust
LOGO_URL = "https://i.postimg.cc/ZqQmfG2J/Whats-App-Image-2026-04-28-at-18-05-28-(1).jpg"

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# --- 2. PRODUCT DATABASE ---
products = [
    {"name": "BB-gun", "price": 25, "img": "https://i.postimg.cc/V6dfmj38/Whats-App-Image-2026-04-28-at-18-44-50.jpg"},
    {"name": "6mm Cartridge", "price": 5, "img": "https://makerworld.bblmw.com/makerworld/model/US4eb0d6d10832a/design/2025-02-21_3d58e70697ae1.jpg"},
    {"name": "Gatling gun", "price": 30, "img": "https://makerworld.bblmw.com/makerworld/model/US92c5fd98860546/design/2025-01-20_b0744fb62f5f2.gif?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "BB-ammo", "price": 0.50, "img": "https://makerworld.bblmw.com/makerworld/model/US14a586903f14f8/design/2025-05-15_b41c34cbd23cb.jpg?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "Suzuki hayabuza gen-2", "price": 50, "img": "https://i.postimg.cc/sXdzdt9h/Whats-App-Image-2026-04-26-at-11-12-31.jpg"}
]

colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

# --- 3. SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- 4. SIDEBAR ---
# We use st.sidebar.image instead of st.logo for better compatibility
st.sidebar.image(LOGO_URL, use_container_width=True)
st.sidebar.title("🛠️ Luca's 3D Lab")
menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Checkout"])

st.sidebar.divider()
st.sidebar.subheader("🛒 Your Cart")
if not st.session_state.cart:
    st.sidebar.write("Empty")
else:
    for item in st.session_state.cart:
        st.sidebar.write(f"**{item['display_name']}** (€{item['price']})")
    if st.sidebar.button("🗑️ Clear Cart"):
        st.session_state.cart = []
        st.rerun()

# --- 5. PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    # Header with Logo
    col_l, col_r = st.columns([1, 6])
    with col_l:
        st.image(LOGO_URL, width=80)
    with col_r:
        st.title("Luca's Custom 3D Prints")
    
    st.write("Pick a model, choose your color, and add it to your cart!")
    st.divider()

    # Product Grid
    col1, col2 = st.columns(2)
    for i, p in enumerate(products):
        with (col1 if i % 2 == 0 else col2):
            st.image(p["img"], use_container_width=True)
            st.subheader(p["name"])
            sel_color = st.selectbox(f"Color for {p['name']}", colors, key=f"c_{i}")
            st.write(f"**Price: €{p['price']}**")
            
            if st.button(f"Add {p['name']} to Cart", key=f"b_{i}"):
                st.session_state.cart.append({
                    "display_name": f"{p['name']} ({sel_color})",
                    "price": p["price"]
                })
                st.toast(f"Added {p['name']}!")
                st.rerun()

# --- 6. PAGE: CHECKOUT ---
elif menu == "Checkout":
    st.title("💳 Checkout")
    if not st.session_state.cart:
        st.info("Cart is empty.")
    else:
        total = sum(item['price'] for item in st.session_state.cart)
        st.write("### Order Summary:")
        for item in st.session_state.cart:
            st.write(f"- {item['display_name']}: €{item['price']}")
        st.divider()
        st.write(f"## Total: €{total}")
        
        # Payment Logic
        if st.button("🚀 Pay with Apple Pay / Card", type="primary"):
            rev_key = st.secrets.get("REVOLUT_SECRET_KEY", "missing")
            if rev_key == "missing":
                st.error("Add your REVOLUT_SECRET_KEY to Streamlit Secrets!")
            else:
                try:
                    payload = {"amount": int(total * 100), "currency": "EUR", "description": "3D Print Order"}
                    headers = {"Authorization": f"Bearer {rev_key}", "Content-Type": "application/json"}
                    res = requests.post("https://merchant.revolut.com/api/1.0/orders", json=payload, headers=headers)
                    data = res.json()
                    if "public_id" in data:
                        st.link_button("Go to Payment", f"https://checkout.revolut.com/payment?public_id={data['public_id']}")
                    else:
                        st.error(f"Error: {data}")
                except Exception as e:
                    st.error(f"Failed: {e}")
