import streamlit as st
import requests
import stripe

# --- 1. SAFE LIBRARY IMPORTS ---
try:
    from stl_to_streamlit import stl_to_streamlit
except ImportError:
    stl_to_streamlit = None

# --- 2. CONFIG & SECRETS ---
# Ensure STRIPE_SECRET_KEY is in your Streamlit Cloud Secrets!
try:
    stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
except:
    stripe.api_key = None

MY_EMAIL = "your-email@gmail.com" # <--- Update this!

# --- 3. SESSION STATE (APP MEMORY) ---
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- 4. PAGE SETUP ---
st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# --- 5. SIDEBAR NAVIGATION (CRITICAL: Define 'menu' here first!) ---
st.sidebar.title("🛠️ Luca's 3D Lab")
menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Checkout"])

st.sidebar.divider()
st.sidebar.subheader("🛒 Your Cart")

if not st.session_state.cart:
    st.sidebar.write("Your cart is empty.")
else:
    for i, item in enumerate(st.session_state.cart):
        st.sidebar.write(f"**{item['display_name']}**")
        st.sidebar.caption(f"€{item['price']}")
    
    if st.sidebar.button("🗑️ Clear Cart"):
        st.session_state.cart = []
        st.rerun()

# --- 6. PAGE LOGIC ---

# PAGE A: BROWSE CATALOG
if menu == "Browse Catalog":
    st.title("🚀 Featured Prints")
    
    # 3D STL Viewer Section
    with st.expander("🔍 View 3D Model (Interactive)", expanded=True):
        if stl_to_streamlit:
            st.write("Rotate and zoom to inspect the model.")
            # Replace this URL with your own Raw GitHub STL link
            stl_url = "https://raw.githubusercontent.com/thevahidal/streamlit-stl/main/examples/models/deer.stl"
            stl_to_streamlit(stl_url)
        else:
            st.info("3D Viewer is initializing... Refresh in 30 seconds.")

    st.divider()

    # Product Data
    products = [
        {"name": "BB-gun", "price": 25, "img": "https://images.unsplash.com/photo-1595590424283-b8f17842773f?w=500"},
        {"name": "6mm with cartridge", "price": 5, "img": "https://images.unsplash.com/photo-1584346133934-a3afd2a33c4c?w=500"}
    ]
    
    colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "✨ Silk Gold", "🔵 Galaxy Blue"]

    col1, col2 = st.columns(2)
    for i, p in enumerate(products):
        with (col1 if i % 2 == 0 else col2):
            st.image(p["img"], use_container_width=True)
            st.subheader(p["name"])
            
            # Selection
            selected_color = st.selectbox(f"Color ({p['name']})", colors, key=f"col_{i}")
            st.write(f"**Price: €{p['price']}**")
            
            if st.button(f"Add to Cart", key=f"add_{i}"):
                new_item = p.copy()
                new_item['display_name'] = f"{p['name']} - {selected_color}"
                st.session_state.cart.append(new_item)
                st.toast(f"Added {new_item['display_name']}!")
                st.rerun()

# PAGE B: CHECKOUT
elif menu == "Checkout":
    st.title("💳 Secure Checkout")
    
    # Check for Stripe success/cancel params
    qp = st.query_params
    if qp.get("payment") == "success":
        st.balloons()
        st.success("✅ Payment received! Luca is heating up the printer.")
        st.session_state.cart = []
        st.stop()
    elif qp.get("payment") == "cancel":
        st.warning("❌ Payment cancelled.")

    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = sum(item['price'] for item in st.session_state.cart)
        st.write("### Review Your Order:")
        for item in st.session_state.cart:
            st.write(f"- {item['display_name']}: €{item['price']}")
        
        st.divider()
        st.write(f"### Total: €{total}")

        if st.button("Generate Payment Link"):
            if not stripe.api_key:
                st.error("Stripe is not configured. Add your Secret Key to Streamlit Secrets!")
            else:
                try:
                    line_items = [{
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {'name': item['display_name']},
                            'unit_amount': int(item['price'] * 100),
                        },
                        'quantity': 1,
                    } for item in st.session_state.cart]

                    session = stripe.checkout.Session.create(
                        payment_method_types=['card'],
                        line_items=line_items,
                        mode='payment',
                        success_url='https://luca-s-3d-printing-shop.streamlit.app/?payment=success',
                        cancel_url='https://luca-s-3d-printing-shop.streamlit.app/?payment=cancel',
                    )
                    
                    st.markdown(f"""
                        <a href="{session.url}" target="_blank">
                            <button style="background-color: #6772E5; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; width: 100%;">
                                Click to Pay €{total}
                            </button>
                        </a>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Stripe Error: {e}")
