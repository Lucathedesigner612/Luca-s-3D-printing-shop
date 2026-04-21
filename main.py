import streamlit as st
import requests

# --- CONFIG ---
# Get your API Key from Revolut Business: Settings -> APIs -> Merchant API
REVOLUT_API_KEY = "your_rev_prod_secret_key" 

if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Lab", layout="wide")

# --- CATALOG LOGIC (Same as before) ---
st.sidebar.title("🛒 Your Cart")
total_cart = sum(item['price'] for item in st.session_state.cart)
for item in st.session_state.cart:
    st.sidebar.write(f"{item['display_name']} - €{item['price']}")

# --- REVOLUT ORDER CREATION ---
def create_revolut_order(amount):
    url = "https://merchant.revolut.com/api/1.0/orders"
    headers = {
        "Authorization": f"Bearer {REVOLUT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "amount": int(amount * 100), # Revolut expects cents/pence
        "currency": "EUR",
        "description": "3D Printing Order from Luca's Lab"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# --- CHECKOUT PAGE ---
st.title("💳 Checkout")

if not st.session_state.cart:
    st.info("Cart is empty.")
else:
    st.write(f"### Total to Pay: €{total_cart}")
    
    if st.button("Proceed to Apple Pay / Card", type="primary"):
        if REVOLUT_API_KEY == "your_rev_prod_secret_key":
            st.error("You need to add your real Revolut Merchant API key!")
        else:
            order_data = create_revolut_order(total_cart)
            
            if "public_id" in order_data:
                # This opens the official Revolut checkout page which handles Apple Pay
                checkout_url = f"https://checkout.revolut.com/payment?public_id={order_data['public_id']}"
                st.link_button("🚀 Open Secure Payment", checkout_url)
                st.info("Apple Pay will be available on the payment page.")
            else:
                st.error("Could not create order. Check your API Key.")

    if st.button("Clear Cart"):
        st.session_state.cart = []
        st.rerun()
