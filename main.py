import streamlit as st
import requests
import stripe

# --- CONFIG & SECRETS ---
# Ensure "STRIPE_SECRET_KEY" is added to your Streamlit Cloud Secrets!
if "STRIPE_SECRET_KEY" in st.secrets:
    stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
else:
    stripe.api_key = None

MY_EMAIL = "your-email@gmail.com" # <--- Update this to your real email

# --- SESSION STATE (Memory) ---
if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🛠️ Luca's 3D Lab")
menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Checkout"])

st.sidebar.divider()
st.sidebar.subheader("🛒 Your Cart")

if not st.session_state.cart:
    st.sidebar.write("Your cart is empty.")
else:
    total_cart = 0
    for i, item in enumerate(st.session_state.cart):
        st.sidebar.write(f"**{item['display_name']}**")
        st.sidebar.caption(f"€{item['price']}")
        total_cart += item['price']
    
    st.sidebar.write(f"**Total: €{total_cart}**")
    
    if st.sidebar.button("🗑️ Clear Cart"):
        st.session_state.cart = []
        st.rerun()

# --- PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    st.title("🚀 Custom 3D Prints")
    st.write("Select your items and choose your favorite filament colors.")
    
    # Simple Product List
    products = [
        {"name": "BB-gun", "price": 25, "img": "https://makerworld.bblmw.com/makerworld/model/US18955f0fc513e5/design/2024-01-03_201b2ae71df09.jpg?x-oss-process=image/resize,w_1000/format,webp"},
        {"name": "6mm Cartridge", "price": 5, "img": "https://makerworld.bblmw.com/makerworld/model/US4eb0d6d10832a/design/2025-02-21_3d58e70697ae1.jpg"},
        {"name": "Gatling gun", "price": 30, "img": "https://makerworld.bblmw.com/makerworld/model/US92c5fd98860546/design/2025-01-20_b0744fb62f5f2.gif?x-oss-process=image/resize,w_1000/format,webp"},
        {"name": "BB-ammo", "price": 0.50,"img": "https://makerworld.bblmw.com/makerworld/model/US14a586903f14f8/design/2025-05-15_b41c34cbd23cb.jpg?x-oss-process=image/resize,w_1000/format,webp"}
    ]
    
    colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

    col1, col2 = st.columns(2)
    for i, p in enumerate(products):
        with (col1 if i % 2 == 0 else col2):
            st.image(p["img"], use_container_width=True)
            st.subheader(p["name"])
            
            # Color Selector
            selected_color = st.selectbox(f"Select Color ({p['name']})", colors, key=f"col_{i}")
            st.write(f"**Price: €{p['price']}**")
            
            if st.button(f"Add {p['name']} to Cart", key=f"btn_{i}"):
                new_item = {
                    "display_name": f"{p['name']} ({selected_color})",
                    "price": p["price"]
                }
                st.session_state.cart.append(new_item)
                st.toast(f"Added {new_item['display_name']}!")
                st.rerun()

# --- PAGE: CHECKOUT ---
elif menu == "Checkout":
    st.title("💳 Secure Checkout")
    
    # Handle Stripe redirect success/cancel
    qp = st.query_params
    if qp.get("payment") == "success":
        st.balloons()
        st.success("✅ Payment received! Luca is heating up the printer.")
        st.session_state.cart = []
        st.stop()
    elif qp.get("payment") == "cancel":
        st.warning("❌ Payment was cancelled.")

    if not st.session_state.cart:
        st.info("Your cart is empty! Head back to the catalog to add items.")
    else:
        st.write("### Review Your Order:")
        total = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"- {item['display_name']}: €{item['price']}")
        
        st.divider()
        st.write(f"### Total Amount: €{total}")

        if st.button("Generate Payment Link"):
            if not stripe.api_key:
                st.error("Stripe Secret Key missing! Add it to Streamlit Secrets.")
            else:
                try:
                    # Prepare Stripe items
                    line_items = [{
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {'name': item['display_name']},
                            'unit_amount': int(item['price'] * 100),
                        },
                        'quantity': 1,
                    } for item in st.session_state.cart]

                    # Create Stripe Session
                    session = stripe.checkout.Session.create(
                        payment_method_types=['card'],
                        line_items=line_items,
                        mode='payment',
                        # IMPORTANT: Update this URL to your actual Streamlit URL
                        success_url='https://luca-s-3d-printing-shop.streamlit.app/?payment=success',
                        cancel_url='https://luca-s-3d-printing-shop.streamlit.app/?payment=cancel',
                    )
                    
                    # Blue Checkout Button
                    st.markdown(f"""
                        <a href="{session.url}" target="_blank">
                            <button style="
                                background-color: #6772E5;
                                color: white;
                                padding: 15px 32px;
                                text-align: center;
                                font-size: 16px;
                                margin: 10px 0px;
                                cursor: pointer;
                                border: none;
                                border-radius: 8px;
                                width: 100%;
                                ">
                                Pay €{total} Now
                            </button>
                        </a>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Stripe Error: {e}")
