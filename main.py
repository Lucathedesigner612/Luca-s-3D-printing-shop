import streamlit as st
import requests
import stripe

# 1. SETUP & MEMORY (Always first)
if "cart" not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="Luca's 3D Lab", layout="wide")

# 2. DEFINE THE MENU (This defines the variable 'menu')
st.sidebar.title("🛠️ Luca's 3D Lab")
menu = st.sidebar.radio("Navigation", ["Browse Catalog", "Checkout"])

# 3. USE THE MENU (This uses the variable 'menu')
if menu == "Browse Catalog":
    st.title("🚀 Browse Catalog")
    # ... your catalog code ...

elif menu == "Checkout":
    st.title("💳 Checkout")
    # ... your checkout code ...
# --- 5. CHECKOUT PAGE ---
elif menu == "Checkout":
    st.title("💳 Secure Checkout")
    
    # Handle Stripe Redirects
    query_params = st.query_params
    if query_params.get("payment") == "success":
        st.balloons()
        st.success("✅ Payment received! Luca is heating up the printer now.")
        st.session_state.cart = []
        st.stop()
    elif query_params.get("payment") == "cancel":
        st.warning("❌ Payment was cancelled.")

    if not st.session_state.cart:
        st.info("Nothing in your cart yet! Head back to the catalog.")
    else:
        st.write("### Review Your Order:")
        total = 0
        for item in st.session_state.cart:
            st.write(f"- {item['display_name']}: €{item['price']}")
            total += item['price']
        
        st.divider()
        st.write(f"### Total Amount: €{total}")
        
        if st.button("Generate Payment Link"):
            try:
                with st.spinner("Talking to Stripe..."):
                    checkout_url = create_checkout_session(st.session_state.cart)
                
                st.markdown(f"""
                    <a href="{checkout_url}" target="_blank">
                        <button style="
                            background-color: #6772E5;
                            color: white;
                            padding: 15px 32px;
                            text-align: center;
                            font-size: 16px;
                            margin: 10px 0px;
                            cursor: pointer;
                            border: none;
                            border-radius: 8px;
                            width: 100%;
                            ">
                            Pay €{total} Now
                        </button>
                    </a>
                """, unsafe_allow_html=True)
                st.caption("Secure payment processed by Stripe.")
            except Exception as e:
                st.error(f"Error creating checkout: {e}")
