import streamlit as st
import requests

# --- CONFIG ---
MY_EMAIL = "lucagalea612@gmail.com" # <--- CHANGE THIS

def send_final_order(contact, cart_items):
    url = f"https://formsubmit.co/ajax/{MY_EMAIL}"
    items_text = "\n".join([f"- {item['name']} (€{item['price']})" for item in cart_items])
    total = sum(item['price'] for item in cart_items)
    
    payload = {
        "_subject": f"New Shop Order from {contact}",
        "Customer": contact,
        "Items": items_text,
        "Total_Price": f"€{total}"
    }
    return requests.post(url, json=payload)

# Initialize the cart in the background if it doesn't exist
if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Shop", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("🛒 Your Cart")
if not st.session_state.cart:
    st.sidebar.write("Your cart is empty.")
else:
    for item in st.session_state.cart:
        st.sidebar.write(f"✅ {item['name']} - €{item['price']}")
    
    if st.sidebar.button("Clear Cart"):
        st.session_state.cart = []
        st.rerun()

# --- MAIN PAGE ---
menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Checkout & Custom"])

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
            if st.button(f"Add {p['name']} to Cart", key=f"add_{i}"):
                st.session_state.cart.append(p)
                st.toast(f"Added {p['name']}!")

elif menu == "Checkout & Custom":
    st.title("💳 Finish Your Order")
    
    if not st.session_state.cart:
        st.warning("Your cart is empty! Add something from the catalog first.")
    else:
        st.write("### Items in your order:")
        for item in st.session_state.cart:
