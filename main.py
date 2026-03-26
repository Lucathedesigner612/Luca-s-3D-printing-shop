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
    st.write("Ready-to-order designs. Select an item to see details.")
    
 products = [
        {
            "name": "BB-gun", 
            "price": 15, 
             
            "price": 10, 
            "img": "https://makerworld.bblmw.com/makerworld/model/USdcbb85be85cd53/design/2025-03-15_5ca8ff6c28f938.jpg?x-oss-process=image/resize,w_1000/format,webp", 
            "desc": "A cool gun with no pain but endless fun!!"
        },
        {
            "name": "BB-gun ammo cartridge with ammo", 
            "price": 12, 
            "img": "https://makerworld.bblmw.com/makerworld/model/US4eb0d6d10832a/design/2025-02-21_3d58e70697ae1.jpg?x-oss-process=image/resize,w_1000/format,webp", 
            "desc": "A box with alot of ammo for elite fun!!"
        },
        {", 
       
        
            "name": "Tech Desk Stand", 
            "price": 8, 
            "img": "https://images.unsplash.com/photo-1618090584126-129cd1f3fbae?w=500", 
            "desc": "Sturdy stand for your smartphone or small tablet."
        }
    ]
    # Line 62: Make sure this is indented exactly 4 spaces (1 tab)
    col1, col2 = st.columns(2)
    
    for i, p in enumerate(products):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.image(p["img"], use_container_width=True)
            st.subheader(p["name"])
            st.write(f"**Price:** €{p['price']}")
            # Use .get to prevent the KeyError from before!
            st.caption(p.get("desc", "No description available."))
            
            if st.button(f"Order {p['name']}", key=f"btn_{i}"):
                st.success(f"Added {p['name']} to your request!")


# --- 2. CUSTOM REQUEST ---
if st.button(f"Order {p['name']}", key=p['name']):
                st.toast(f"Added {p['name']} to your request!")
# <-- Make sure there is no extra code here that isn't indented!
elif menu == "Custom Request":
    st.title("📩 Custom Print Request")
    st.write("Have your own STL file? Upload it or describe it here.")
    
    with st.form("custom_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Contact Email / WhatsApp")
        color = st.selectbox("Filament Color", ["Matte Black", "Silk Gold", "Electric Blue", "Neon Green"])
        details = st.text_area("Describe your project (size, usage, etc.)")
        
        submitted = st.form_submit_button("Submit Request")
        if submitted:
            st.balloons()
            st.success("Request Sent! I'll get back to you with a quote within 24 hours.")

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
