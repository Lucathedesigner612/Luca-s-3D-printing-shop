elif choice == "3D Print Store":
    st.title("🖨️ Luca's 3D Print Lab")
    st.subheader("Custom Prints & Designs | Ships from Malta 🇲🇹")

    # Catalog Data (You can add more items here)
    items = [
        {"name": "Articulated Dragon", "price": "€15", "img": "https://images.unsplash.com/photo-1631002165109-7794e8dd87c0?w=400", "desc": "Fully moving joints, 20cm long."},
        {"name": "Planter Pot", "price": "€10", "img": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400", "desc": "Geometric design for succulents."},
        {"name": "Custom Keychain", "price": "€5", "img": "https://images.unsplash.com/photo-1618090584126-129cd1f3fbae?w=400", "desc": "Personalized with your name."}
    ]

    # Displaying the Items in a Grid
    col1, col2 = st.columns(2)

    for i, item in enumerate(items):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.image(item["img"], use_container_width=True)
            st.markdown(### {item['name']})
            st.write(f"**Price:** {item['price']}")
            st.caption(item["desc"])
            
            # THE "BUY" BUTTON
            if st.button(f"Order {item['name']}", key=item['name']):
                st.success(f"Great choice! Please fill out the form below to order the {item['name']}.")
                
    st.divider()
    
    # --- ORDER FORM ---
    st.header("📩 Place an Order")
    with st.form("order_form"):
        cust_name = st.text_input("Your Name")
        item_choice = st.selectbox("Select Item", [i["name"] for i in items])
        color = st.select_slider("Select Filament Color", ["Red", "Blue", "Silver", "Black", "Gold"])
        notes = st.text_area("Specific Requests (Size, etc.)")
        
        submitted = st.form_submit_code("Send Request")
        if submitted:
            st.balloons()
            st.write(f"Thanks {cust_name}! I'll contact you about the **{color} {item_choice}**.")