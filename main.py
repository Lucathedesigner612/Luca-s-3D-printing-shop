import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Luca 3D Lab | Malta", page_icon="🖨️", layout="wide")

# --- CUSTOM CSS FOR A MODERN LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #00FFA3; color: black; font-weight: bold; }
    .product-card { border: 1px solid #333; padding: 15px; border-radius: 15px; background: #161B22; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION & STATUS ---
st.sidebar.title("🖨️ Luca 3D Lab")

# LIVE PRINTER STATUS
# You can change this to "Busy" or "Maintenance" when you are printing!
printer_status = "Available" 

if printer_status == "Available":
    st.sidebar.success("🟢 Status: Ready to Print")
elif printer_status == "Busy":
    st.sidebar.warning("🟡 Status: Printer is Busy")
else:
    st.sidebar.error("🔴 Status: Maintenance")

st.sidebar.info("High-Quality 3D Prints in Malta 🇲🇹")
st.sidebar.divider()

menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Custom Request", "Pricing Calculator"])
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
            # THIS LINE BELOW IS LINE 63 - IT MUST BE INDENTED LIKE THIS
            if st.button(f"Order {p['name']}", key=f"btn_{i}"):
                st.success(f"Added {p['name']} to your request!")

# --- 2. CUSTOM REQUEST ---
elif menu == "Custom Request":
    st.title("📩 Custom Print Request")
    st.write("Fill out the form below for a quote.")
    
    contact = st.text_input("Your Email or Phone")
    details = st.text_area("Describe what you want to print")
    uploaded_file = st.file_uploader("Upload STL file (optional)")
    
    if st.button("Submit Request"):
        if contact and details:
            st.success("Request sent! Luca will contact you soon.")
        else:
            st.error("Please fill in your contact info and details.")

# --- 3. PRICING CALCULATOR ---
elif menu == "Pricing Calculator":
    st.title("📊 Instant Quote Tool")
    st.write("Estimate the cost of your print based on weight and time.")
    
    weight = st.number_input("Object Weight (grams)", min_value=1, value=50)
    hours = st.number_input("Estimated Print Time (hours)", min_value=1, value=3)
    
    # Simple Malta Market Logic: €0.05 per gram + €1.50 per hour
    material_cost = weight * 0.05
    machine_cost = hours * 1.50
    total = material_cost + machine_cost
    
    st.divider()
    st.metric("Estimated Total", f"€{total:.2f}")
    st.info("Note: Final price may vary based on design complexity.")
