import streamlit as st
import requests

# --- CONFIG ---
MY_EMAIL = "lucagalea612@gmail.com" # <--- Change this to your real email

def send_final_order(contact, cart_items):
    url = f"https://formsubmit.co/ajax/{MY_EMAIL}"
    items_text = "\n".join([f"- {item['name']} (€{item['price']})" for item in cart_items])
    total = sum(item['price'] for item in cart_items)
    payload = {
        "_subject": f"New Order from {contact}",
        "Customer": contact,
        "Items": items_text,
        "Total": f"€{total}"
    }
    return requests.post(url, json=payload)

# 1. INITIALIZE MEMORY (This only runs once when the app starts)
if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Shop", layout="wide")

# --- SIDEBAR CART ---
st.sidebar.title("🛒 Your Cart")

# 2. DISPLAY ITEMS FROM MEMORY
if not st.session_state.cart:
    st.sidebar.write("Your cart is empty.")
else:
    for i, item in enumerate(st.session_state.cart):
        st.sidebar.write(f"{i+1}. {item['name']} - €{item['price']}")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Clear Cart"):
        st.session_state.cart = []
        st.rerun() # Refresh to show empty cart

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
            
            # 3. ADD TO MEMORY AND REFRESH
            if st.button(f"Add {p['name']} to Cart", key=f"add_{i}"):
                st.session_state.cart.append(p)
                st.toast(f"Added {p['name']} to cart!")
                st.rerun() # THIS IS THE MAGIC LINE that fixes the display

elif menu == "Checkout":
    st.title("💳 Finish Your Order")
    if not st.session_state.cart:
        st.warning("Your cart is empty! Go to the catalog to add items.")
    else:
        st.write("### Review Items:")
        total_price = 0
        for item in st.session_state.cart:
            st.write(f"- {item['name']}: €{item['price']}")
            total_price += item['price']
