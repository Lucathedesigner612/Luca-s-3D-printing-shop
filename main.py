import streamlit as st

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
    total_cart = sum(item['price'] for item in st.session_state.cart)
    for item in st.session_state.cart:
        st.sidebar.write(f"**{item['display_name']}**")
        st.sidebar.caption(f"€{item['price']}")
    
    st.sidebar.write(f"### Total: €{total_cart}")
    
    if st.sidebar.button("🗑️ Clear Cart"):
        st.session_state.cart = []
        st.rerun()

# --- PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    st.title("🚀 Custom 3D Prints")
    st.write("Add items to your cart, then head to Checkout to pay via Revolut.")
    
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
            selected_color = st.selectbox(f"Select Color", colors, key=f"col_{i}")
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
    st.title("💳 Checkout via Revolut")
    
    if not st.session_state.cart:
        st.info("Your cart is empty! Head back to the catalog to add items.")
    else:
        st.write("### Review Your Order:")
        total = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"- {item['display_name']}: €{item['price']}")
        
        st.divider()
        st.write(f"### Total Amount: €{total}")
        st.warning("Please note: After paying on Revolut, your order will be processed manually.")

        # This creates the dynamic Revolut link
        revolut_url = f"https://revolut.me/lucaf2nfx/{total}"
        
        st.link_button(f"Pay €{total} on Revolut", revolut_url, type="primary")
        
        if st.button("I have finished paying"):
            st.balloons()
            st.success("Thanks! Once Luca confirms the transfer, your print will start!")
            st.session_state.cart = []
