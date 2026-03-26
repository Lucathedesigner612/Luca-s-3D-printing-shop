import streamlit as st
import requests
import stripe
# Try to import the viewer, but don't crash the whole site if it fails
try:
    from stl_to_streamlit import stl_to_streamlit
except ImportError:
    stl_to_streamlit = None

# --- CONFIG ---
try:
    stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
except:
    st.warning("Stripe Key not found in Secrets.")

# ... inside your Browse Catalog menu ...
if menu == "Browse Catalog":
    if stl_to_streamlit:
        with st.expander("🔍 View 3D Model"):
            stl_url = "https://raw.githubusercontent.com/thevahidal/streamlit-stl/main/examples/models/deer.stl"
            stl_to_streamlit(stl_url)
    else:
        st.error("3D Viewer library is still installing. Please wait a moment.")

def create_checkout_session(items):
    """Creates a Stripe Checkout session and returns the URL"""
    line_items = []
    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': item['display_name']},
                'unit_amount': int(item['price'] * 100), # Cents
            },
            'quantity': 1,
        })
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='https://luca-s-3d-printing-shop.streamlit.app/?payment=success',
        cancel_url='https://luca-s-3d-printing-shop.streamlit.app/?payment=cancel',
    )
    return session.url

# --- 2. SESSION STATE (MEMORY) ---
if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# --- 3. SIDEBAR NAVIGATION & CART ---
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

# --- 4. BROWSE CATALOG ---
if menu == "Browse Catalog":
    st.title("🚀 Featured Prints")
    
    # 3D STL VIEWER SECTION
with st.expander("🔍 View 3D Model (Interactive)", expanded=True):
        st.write("Rotate and zoom to inspect our high-detail model.")
        stl_url = "https://raw.githubusercontent.com/thevahidal/streamlit-stl/main/examples/models/deer.stl"
        # The new library uses this command:
        stl_to_streamlit(stl_url)

if menu == "Browse Catalog":
    st.title("🚀 Luca's 3D Inventory")
      st.divider()  # ERROR: This is indented 6 spaces instead of 4!

    # PRODUCTS LIST
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
            
            # COLOR SELECTOR
            selected_color = st.selectbox(f"Filament Color ({p['name']})", colors, key=f"col_{i}")
            st.write(f"**Price: €{p['price']}**")
            
            if st.button(f"Add to Cart", key=f"add_{i}"):
                # Add customized item to session state
                new_item = p.copy()
                new_item['display_name'] = f"{p['name']} - {selected_color}"
                st.session_state.cart.append(new_item)
                st.toast(f"Added {new_item['display_name']}!")
                st.rerun()

# --- 5. CHECKOUT PAGE ---
elif menu == "Checkout":
    st.title("💳 Secure Checkout")
    
    # Handle Stripe Redirects
    query_params = st.query_params
    if query_params.get("payment") == "success":
        st.balloons()
        st.success("✅ Payment received! Luca is heating up the printer now.")
        st.session_state.cart = []
        st.stop()
    elif query_params.get("payment") == "cancel":
        st.warning("❌ Payment was cancelled.")

    if not st.session_state.cart:
        st.info("Nothing in your cart yet! Head back to the catalog.")
    else:
        st.write("### Review Your Order:")
        total = 0
        for item in st.session_state.cart:
            st.write(f"- {item['display_name']}: €{item['price']}")
            total += item['price']
        
        st.divider()
        st.write(f"### Total Amount: €{total}")
        
        if st.button("Generate Payment Link"):
            try:
                with st.spinner("Talking to Stripe..."):
                    checkout_url = create_checkout_session(st.session_state.cart)
                
                st.markdown(f"""
                    <a href="{checkout_url}" target="_blank">
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
                st.caption("Secure payment processed by Stripe.")
            except Exception as e:
                st.error(f"Error creating checkout: {e}")
