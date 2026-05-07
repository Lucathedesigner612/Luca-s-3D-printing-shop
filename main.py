import streamlit as st
import requests

# --- 1. CONFIG & LOGO ---
# I've updated the URL logic to be more robust
LOGO_URL = "https://i.postimg.cc/ZqQmfG2J/Whats-App-Image-2026-04-28-at-18-05-28-(1).jpg"

st.set_page_config(page_title="Luca's 3D Lab", layout="wide", page_icon="🛠️")

# --- 2. PRODUCT DATABASE ---
products = [
    {"name": "BB-gun", "price": 25, "img": "https://i.postimg.cc/G27js17n/Whats-App-Image-2026-04-28-at-18-44-50.jpg"},
    {"name": "6mm Cartridge", "price": 5, "img": "https://makerworld.bblmw.com/makerworld/model/US4eb0d6d10832a/design/2025-02-21_3d58e70697ae1.jpg"},
    {"name": "Gatling gun", "price": 30, "img": "https://makerworld.bblmw.com/makerworld/model/US92c5fd98860546/design/2025-01-20_b0744fb62f5f2.gif?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "BB-ammo", "price": 0.50, "img": "https://makerworld.bblmw.com/makerworld/model/US14a586903f14f8/design/2025-05-15_b41c34cbd23cb.jpg?x-oss-process=image/resize,w_1000/format,webp"},
    {"name": "Suzuki hayabuza gen-2", "price": 50, "img": "https://i.postimg.cc/sXdzdt9h/Whats-App-Image-2026-04-26-at-11-12-31.jpg"},
    {"name": "JBL XTREME 3 Holder", "price": 10, "img": "https://makerworld.bblmw.com/makerworld/model/USfc9347493e1889/design/2025-08-22_3ffac4e1f6c888.jpg?x-oss-process=image/resize,w_1000/format,webp"}
]

colors = ["🔴 Matte Red", "⚫ Stealth Black", "⚪ Glossy White", "🟡 Silk Gold", "🟢 Apple Green"]

# --- 3. SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []
# --- SIDEBAR NAVIGATION & CART ---
# (Your existing code for menu and cart goes here...)

st.sidebar.divider()
st.sidebar.subheader("✉️ Custom Request")
st.sidebar.write("Want something special? Send Luca a message!")

# 1. Create the Form
with st.sidebar.form("contact_form", clear_on_submit=True):
    email = st.text_input("Your Email Address")
    message = st.text_area("Describe your project (size, color, use)")
    
    # Optional: Link to a file or model if they have one
    model_link = st.text_input("Link to 3D Model (optional)")
    
    submit_button = st.form_submit_button("Send Message")

# 2. Handle the Submission
if submit_button:
    if not email or not message:
        st.sidebar.error("Please provide your email and a message.")
    else:
        # FormSubmit endpoint (Free)
        # Change 'your-email@gmail.com' to your actual email address!
        contact_url = "https://formsubmit.co/ajax/your-email@gmail.com"
        
        payload = {
            "email": email,
            "message": message,
            "model_link": model_link,
            "_subject": "New Custom 3D Print Request!"
        }
        
        try:
            response = requests.post(contact_url, data=payload)
            if response.status_code == 200:
                st.sidebar.success("Message sent! Luca will email you back soon.")
            else:
                st.sidebar.error("Failed to send. Try again later.")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")
# --- 5. PAGE: BROWSE CATALOG ---
if menu == "Browse Catalog":
    st.title("Luca's Custom 3D Prints")
    
    # CSS to force all product images to the same height and crop them
    st.markdown("""
        <style>
        [data-testid="stImage"] img {
            height: 250px;
            object-fit: cover;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.write("Pick a model, choose your color, and add it to your cart!")
    st.divider()

    # Create the 3-column grid
    cols = st.columns(3) 

    for i, p in enumerate(products):
        with cols[i % 3]:
            # The CSS above handles the height, so we just display the image
            st.image(p["img"], use_container_width=True)
            
            # We wrap the info in a container to keep it neat
            with st.container():
                # Force the name to take up exactly two lines so prices align
                st.markdown(f"<div style='height: 50px; overflow: hidden;'><b>{p['name']}</b></div>", unsafe_allow_html=True)
                
                sel_color = st.selectbox(f"Color", colors, key=f"c_{i}", label_visibility="collapsed")
                st.write(f"**€{p['price']}**")
                
                if st.button(f"Add to Cart", key=f"b_{i}", use_container_width=True):
                    st.session_state.cart.append({
                        "display_name": f"{p['name']} ({sel_color})",
                        "price": p["price"]
                    })
                    st.toast(f"Added {p['name']}!")
                    st.rerun()
            st.write("---") # Adds a separator for mobile users
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
