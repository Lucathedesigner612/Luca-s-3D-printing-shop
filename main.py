import streamlit as st
import requests

# --- 1. PRODUCT DATABASE ---
# You can add or change products here easily
products = [
    {
        "name": "BB-gun", 
        "price": 25, 
        "img": "https://makerworld.bblmw.com/makerworld/model/US18955f0fc513e5/design/2024-01-03_201b2ae71df09.jpg?x-oss-process=image/resize,w_1000/format,webp"
    },
    {
        "name": "6mm Cartridge", 
        "price": 5, 
        "img": "https://makerworld.bblmw.com/makerworld/model/US4eb0d6d10832a/design/2025-02-21_3d58e70697ae1.jpg"
    },
    {
        "name": "Gatling gun", 
        "price": 30, 
        "img": "https://makerworld.bblmw.com/makerworld/model/US92c5fd98860546/design/2025-01-20_b0744fb62f5f2.gif?x-oss-process=image/resize,w_1000/format,webp"
    },
    {
        "name": "BB-ammo", 
        "price": 0.50, 
        "img": "https://makerworld.bblmw.com/makerworld/model/US14a586903f14f8/design/2025-05-15_b41c34cbd23cb.jpg?x-oss-process=image/resize,w_1000/format,webp"
    }
]

colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

# --- 2. CONFIG & SECRETS ---
# To make this work, add REVOLUT_SECRET_KEY to your Streamlit Cloud Secrets
if "REVOLUT_SECRET_KEY" in st.secrets:
    REV_KEY = st.secrets["REVOLUT_SECRET_KEY"]
else:
    REV_KEY = "your_sk_here" 

# --- 3. SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# --- 4. SIDEBAR (Navigation & Cart) ---
st.sidebar.title("🛠️ Luca's 3D Lab")
menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Checkout"])

st.sidebar.divider()
st.sidebar.subheader("🛒 Your Cart")

if not st.session_state.cart:
    st.sidebar.write("Your cart is empty.")
else:
    total_cart = sum(item['price'] for item in st.session_state.cart)
    for item in st.session_state.cart:
        st.sidebar.write(f"**{item['display_name']}**")
        st.sidebar.caption(f"€{item['price']}")
    
    st.sidebar.write(f"### Total: €{total_cart}")
    if st.sidebar.button("🗑️ Clear Cart"):
        st.session_state.cart = []
        st.rerun()

# --- 5. PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    st.title("🚀 Custom 3D Prints")
    st.write("Pick a model, choose your color, and add it to your cart!")

    col1, col2 = st.columns(2)
    for i, p in enumerate(products):
        # This alternates products between the two columns
        with (col1 if i % 2 == 0 else col2):
            st.image(p["img"], use_container_width=True)
            st.subheader(p["name"])
            
            # Options
            sel_color = st.selectbox(f"Color for {p['name']}", colors, key=f"select_{i}")
            st.write(f"**Price: €{p['price']}**")
            
            if st.button(f"Add {p['name']} to Cart", key=f"btn_{i}"):
                st.session_state.cart.append({
                    "display_name": f"{p['name']} ({sel_color})",
                    "price": p["price"]
                })
                st.toast(f"Added {p['name']} to cart!")
                st.rerun()

# --- 6. PAGE: CHECKOUT ---
elif menu == "Checkout":
    st.title("💳 Secure Checkout")
    
    if not st.session_state.cart:
        st.info("Your cart is empty! Head back to the catalog to find something cool.")
    else:
        st.write("### Review Your Order:")
        total = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"- {item['display_name']}: €{item['price']}")
        
        st.divider()
        st.write(f"## Total Amount: €{total}")

        if st.button("🚀 Pay with Apple Pay / Card", type="primary"):
            if REV_KEY == "your_sk_here":
                st.error("Missing Revolut API Key! Add 'REVOLUT_SECRET_KEY' to your Streamlit Secrets.")
            else:
                try:
                    # 1. Create the order in Revolut's system
                    payload = {
                        "amount": int(total * 100), # Amount in cents
                        "currency": "EUR",
                        "description": "Order from Luca's 3D Printing Shop"
                    }
                    headers = {
                        "Authorization": f"Bearer {REV_KEY}",
                        "Content-Type": "application/json"
                    }
                    response = requests.post("https://merchant.revolut.com/api/1.0/orders", json=payload, headers=headers)
                    data = response.json()

                    if "public_id" in data:
                        # 2. Provide the link to the secure Revolut checkout page
                        checkout_url = f"https://checkout.revolut.com/payment?public_id={data['public_id']}"
                        st.success("Order Created!")
                        st.link_button("Go to Secure Payment Page", checkout_url)
                        st.info("Apple Pay and Google Pay will be available on the payment page.")
                    else:
                        st.error(f"Revolut API Error: {data.get('message', 'Unknown Error')}")
                
                except Exception as e:
                    st.error(f"Could not connect to payment provider: {e}")

        st.caption("After successful payment, your 3D print will be scheduled for production.")
