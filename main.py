import streamlit as st
import requests
import stripe

# --- CONFIG ---
# This line tells the app to pull the key from the "Secrets" menu you just filled out
try:
    stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
except:
    st.error("Missing Stripe Key! Please add STRIPE_SECRET_KEY to your App Secrets.")

MY_EMAIL = "lucagalea612@gmail.com" 

# ... rest of your code ...
def create_checkout_session(items):
    """Creates a Stripe Checkout session and returns the URL"""
    line_items = []
    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': item['name']},
                'unit_amount': int(item['price'] * 100), # Stripe uses cents
            },
            'quantity': 1,
        })
    
    # This creates the link the user clicks to pay
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='https://luca-s-3d-printing-shop.streamlit.app/?payment=success',
        cancel_url='https://luca-s-3d-printing-shop.streamlit.app/?payment=cancel',
    )
    return session.url

# Initialize Cart
if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Shop", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("🛒 Cart")
for i, item in enumerate(st.session_state.cart):
    st.sidebar.write(f"{item['name']} - €{item['price']}")

if st.sidebar.button("Clear Cart"):
    st.session_state.cart = []
    st.rerun()

# --- MAIN NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Checkout"])

if menu == "Browse Catalog":
    st.title("🚀 Luca's 3D Inventory")
    products = [
        {"name": "BB-gun", "price": 25, "img": "https://images.unsplash.com/photo-1595590424283-b8f17842773f?w=500"},
        {"name": "6mm with cartridge", "price": 5, "img": "https://images.unsplash.com/photo-1584346133934-a3afd2a33c4c?w=500"}
    ]
    
    col1, col2 = st.columns(2)
    for i, p in enumerate(products):
        with (col1 if i % 2 == 0 else col2):
            st.image(p["img"], use_container_width=True)
            st.subheader(p["name"])
            st.write(f"Price: €{p['price']}")
            if st.button(f"Add {p['name']}", key=f"add_{i}"):
                st.session_state.cart.append(p)
                st.rerun()

elif menu == "Checkout":
    st.title("💳 Secure Checkout")
    
    # Check if they just came back from a successful payment
    query_params = st.query_params
    if query_params.get("payment") == "success":
        st.balloons()
        st.success("✅ Payment Successful! Luca is starting your print now.")
        st.session_state.cart = [] # Clear cart
    elif query_params.get("payment") == "cancel":
        st.warning("❌ Payment cancelled. Your items are still in the cart.")

    if st.session_state.cart:
        total = sum(item['price'] for item in st.session_state.cart)
        st.write(f"### Total Amount: €{total}")
        
        if st.button("Pay with Card (Stripe)"):
            try:
                checkout_url = create_checkout_session(st.session_state.cart)
                st.info("Redirecting to secure payment page...")
                st.markdown(f'<a href="{checkout_url}" target="_self" style="display: inline-block; padding: 10px 20px; background-color: #6772E5; color: white; text-decoration: none; border-radius: 5px;">Click Here to Pay €{total}</a>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Stripe Error: {e}")
