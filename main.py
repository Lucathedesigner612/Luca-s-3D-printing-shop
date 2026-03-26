import streamlit as st
import requests

# --- CONFIG ---
# CHANGE THIS TO YOUR EMAIL!
MY_EMAIL = "lucagalea612@gmail.com"

def send_email(subject, message):
    """Sends an email notification via FormSubmit"""
    url = f"https://formsubmit.co/ajax/{MY_EMAIL}"
    payload = {
        "_subject": subject,
        "message": message
    }
    try:
        requests.post(url, json=payload)
    except:
        pass # Fails silently if internet is blipping

# --- UI ---
st.set_page_config(page_title="Luca's 3D Printing", layout="wide")

st.sidebar.title("🛠️ Luca's 3D Shop")
menu = st.sidebar.radio("Go to:", ["Browse Catalog", "Custom Request"])

# --- 1. BROWSE CATALOG ---
if menu == "Browse Catalog":
    st.title("🚀 Featured Prints")
    
    products = [
        {"name": "BB-gun", "price": 25, "img": "https://images.unsplash.com/photo-1595590424283-b8f17842773f?w=500"},
        {"name": "6mm with cartridge", "price": 5, "img": "https://images.unsplash.com/photo-1584346133934-a3afd2a33c4c?w=500"}
    ]
    
    col1, col2 = st.columns(2)
    
    for i, p in enumerate(products):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.image(p["img"], use_container_width=True)
            st.subheader(p["name"])
            st.write(f"**Price:** €{p['price']}")
            
            if st.button(f"Order {p['name']}", key=f"btn_{i}"):
                # SEND EMAIL NOTIFICATION
                msg = f"New Order: {p['name']} for €{p['price']}"
                send_email("New Shop Order!", msg)
                st.success(f"Order for {p['name']} sent to Luca!")

# --- 2. CUSTOM REQUEST ---
elif menu == "Custom Request":
    st.title("📩 Custom Print Request")
    
    with st.form("custom_form"):
        contact = st.text_input("Your Email or Phone Number")
        details = st.text_area("What do you want to print? (Size, Color, etc.)")
        submitted = st.form_submit_button("Submit Request")
        
        if submitted:
            if contact and details:
                # SEND EMAIL NOTIFICATION
                msg = f"Contact: {contact}\nDetails: {details}"
                send_email("New Custom Request!", msg)
                st.success("Request sent! Luca will contact you soon.")
            else:
                st.error("Please fill in both fields.")
