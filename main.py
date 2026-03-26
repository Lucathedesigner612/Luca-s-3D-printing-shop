import streamlit as st
import requests

# ⚠️ CHANGE THIS to your actual email!
MY_EMAIL = "lucagalea612@gmail.com"

def send_email(subject, message):
    # This sends the data to FormSubmit
    url = f"https://formsubmit.co/ajax/{MY_EMAIL}"
    payload = {"_subject": subject, "message": message}
    response = requests.post(url, json=payload)
    return response.status_code == 200

st.set_page_config(page_title="Luca's 3D Shop")

st.sidebar.title("🛠️ Luca's 3D Lab")
menu = st.sidebar.radio("Menu", ["Browse Catalog", "Custom Request"])

if menu == "Browse Catalog":
    st.title("🚀 Featured Prints")
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
            if st.button(f"Order {p['name']}", key=f"btn_{i}"):
                if send_email(f"ORDER: {p['name']}", f"Someone wants to buy the {p['name']} for €{p['price']}"):
                    st.success("Order sent! Check your email for confirmation.")
                else:
                    st.error("Email failed to send. Check your MY_EMAIL setting.")

elif menu == "Custom Request":
    st.title("📩 Custom Request")
    with st.form("custom_form"):
        contact = st.text_input("Email/Phone")
        details = st.text_area("Details")
        if st.form_submit_button("Send Request"):
            if contact and details:
                send_email("New Custom Request", f"From: {contact}\nDetails: {details}")
                st.success("Sent! Luca will contact you.")
