import streamlit as st

# Set up mobile-first browser configuration
st.set_page_config(page_title="Kal Kya Banau?", page_icon="🍳", layout="centered")

# ==========================================
# 🔒 SIMPLE SECURITY LOCK SCREEN
# ==========================================
# CHANGE THIS TO YOUR PREFERRED 4-DIGIT PIN
FAMILY_PIN = "1234" 

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🍳 Kal Kya Banau?")
    st.markdown("### 🔒 Family Access Required")
    st.write("Please enter your family PIN to access the kitchen planner engine.")
    
    # Text input styled for mobile numerical entry
    user_pin = st.text_input("Enter 4-Digit PIN:", type="password", max_chars=4, placeholder="••••")
    
    if st.button("Unlock App", use_container_width=True):
        if user_pin == FAMILY_PIN:
            st.session_state.authenticated = True
            st.success("🔓 Access Granted!")
            st.rerun()
        else:
            st.error("❌ Incorrect PIN. Please try again.")
    st.stop() # Stops execution here so nothing else loads unless unlocked

# ==========================================
# CORE APP ENGINE (LOADS ONLY AFTER UNLOCK)
# ==========================================

# Core recipe database containing categories and lunchbox identifiers
DEFAULT_RECIPES = [
    {
        "name": "Classic Homestyle Bataka-Powa",
        "time": "20 mins",
        "staple": "Bataka-Powa",
        "kid_approved": True,
        "is_lunchbox": True,
        "required": ["Poha", "Potato", "Onion"],
        "image": "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?q=80&w=600&auto=format&fit=crop",
        "instructions": [
            "Wash the poha thoroughly in a strainer and let it drain so it stays fluffy.",
            "Heat oil in a pan, add mustard seeds, curry leaves, onions, and small potato cubes.",
            "Cook until potatoes are soft, then add turmeric, salt, and green chilies.",
            "Toss in the damp poha gently so the grains don't break.",
            "Cover and let it steam on low heat for 2 mins. Pack when slightly cooled."
        ]
    },
    {
        "name": "Crispy Cheese Koki (Lunchbox Hero)",
        "time": "20 mins",
        "staple": "Wraps/Frankies",
        "kid_approved": True,
        "is_lunchbox": True,
        "required": ["Wheat Flour / Atta", "Cheese", "Onion"],
        "image": "https://images.unsplash.com/photo-1626700051175-6518c4793f4f?q=80&w=600&auto=format&fit=crop",
        "instructions": [
            "Knead wheat flour with finely chopped onions, green chilies, salt, and a dash of oil to create a stiff dough.",
            "Roll it out thick, place it on a hot tawa, and make small pricks with a fork.",
            "Cook slowly on both sides with ghee until crisp golden spots appear.",
            "Grate a thick layer of cheese directly over the hot koki, fold it smoothly, wrap in foil."
        ]
    },
    {
        "name": "Quick Grilled Veggie & Cheese Sandwiches",
        "time": "15 mins",
        "staple": "Wraps/Frankies",
        "kid_approved": True,
        "is_lunchbox": True,
        "required": ["Bread Slice", "Cheese", "Potato", "Onion"],
        "image": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?q=80&w=600&auto=format&fit=crop",
        "instructions": [
            "Butter two slices of bread and spread green mint chutney or ketchup inside.",
            "Layer with thin slices of boiled potatoes, onions, and capsicum.",
            "Top with a generous handful of grated cheese, close it up, and toast on a pan until crispy."
        ]
    },
    {
        "name": "Aromatic Veg Biryani",
        "time": "35 mins",
        "staple": "Rice & Pulav Dishes",
        "kid_approved": True,
        "is_lunchbox": True,
        "required": ["Rice", "Potato", "Onion", "Tomato"],
        "image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=600&auto=format&fit=crop",
        "instructions": [
            "Parboil seasoned rice with whole spices until 80% cooked, then drain.",
            "Sauté sliced onions, potato cubes, and tomatoes with authentic biryani masala.",
            "Layer the gravy and parboiled rice alternately in a pot, cover tightly, and steam (Dum) on low for 12 minutes."
        ]
    },
    {
        "name": "Traditional Sindhi Pulav with Fried Potato",
        "time": "30 mins",
        "staple": "Rice & Pulav Dishes",
        "kid_approved": True,
        "is_lunchbox": True,
        "required": ["Rice", "Potato", "Onion"],
        "image": "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?q=80&w=600&auto=format&fit=crop",
        "instructions": [
            "Caramelize sliced onions in a pot until deep dark brown to give the rice its authentic rich color.",
            "Add water, basic spices, and pre-soaked rice to cook together until completely fluffy.",
            "Serve the brown rice topped with crispy, seasoned shallow-fried potato chunks."
        ]
    },
    {
        "name": "Cheesy Leftover Sabzi Frankies",
        "time": "15 mins",
        "staple": "Wraps/Frankies",
        "kid_approved": True,
        "is_lunchbox": True,
        "required": ["Roti / Wraps", "Any Dry Leftover Sabzi", "Cheese"],
        "image": "https://images.unsplash.com/photo-1626700051175-6518c4793f4f?q=80&w=600&auto=format&fit=crop",
        "instructions": [
            "Warm up your leftover rotis on a tawa with a little ghee or butter.",
            "Spread a layer of green chutney, tomato ketchup, or mayonnaise.",
            "Place your dry leftover sabzi down the center, grate plenty of cheese, and roll it up tightly in foil."
        ]
    },
    {
        "name": "Loaded Mexican Veggie Bowl",
        "time": "20 mins",
        "staple": "Mexican/Continental",
        "kid_approved": True,
        "is_lunchbox": False,
        "required": ["Rice", "Tomato", "Cheese"],
        "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=600&auto=format&fit=crop",
        "instructions": [
            "Layer cooked fluffy rice at the bottom of a serving bowl.",
            "Top with warm seasoned beans, finely chopped fresh tomatoes, onions, and lettuce.",
            "Garnish heavily with grated cheese and any available salsa or dynamic dips."
        ]
    },
    {
        "name": "Homestyle Punjabi Kadi Chaval",
        "time": "35 mins",
        "staple": "Dal-Chawal",
        "kid_approved": False,
        "is_lunchbox": False,
        "required": ["Curd / Dahi", "Rice", "Onion"],
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?q=80&w=600&auto=format&fit=crop",
        "instructions": [
            "Whisk curd/dahi and gram flour (besan) together with water, turmeric, and salt.",
            "Simmer the kadi mixture on low heat for 20 minutes until rich and thick.",
            "Prepare onion pakodas and gently slide them into the hot seasoned gravy. Serve with hot rice."
        ]
    }
]

DEFAULT_BASE_INGREDIENTS = [
    "Potato", "Onion", "Tomato", "Bell Peppers / Capsicum", "Spinach / Palak", 
    "Opo Squash / Lauki", "Any Dry Leftover Sabzi", "Paneer", "Cheese", 
    "Curd / Dahi", "Gram Flour / Besan", "Bread Slice", "Roti / Wraps", 
    "Wheat Flour / Atta", "Poha", "Rice", "Pasta / Macaroni", 
    "Oats (Flakes/Flour)", "Toor Dal (Arhar)", "Moong Dal", 
    "Chana Dal / Kala Chana", "White Chickpeas (Kabuli Chana)"
]

# Initialize states seamlessly in session memory
if "recipe_db" not in st.session_state:
    st.session_state.recipe_db = DEFAULT_RECIPES
if "custom_ingredients" not in st.session_state:
    st.session_state.custom_ingredients = ["Lettuce"]

# Application Branding Headers
st.title("🍳 Kal Kya Banau?")
st.markdown("##### Smart Mobile Meal Planner & Pantry Engine")
st.divider()

# Core Tab Navigation Structure
tab1, tab2, tab3, tab4 = st.tabs([
    "🛒 1. Fridge Stock", 
    "🍽️ 2. Main Meals", 
    "🎒 3. Kids Lunchbox / Breakfast", 
    "✍️ 4. Add Recipe"
])

# ==========================================
# TAB 1: ALWAYS-STOCKED PANTRY CHECKLIST
# ==========================================
with tab1:
    st.markdown("### 🎛️ Active Stock Management")
    st.caption("Everything is checked by default. Uncheck items ONLY if you are completely out of stock.")
    
    active_inventory = []
    
    with st.expander("🥦 Fresh Produce & Leftovers", expanded=True):
        for item in ["Potato", "Onion", "Tomato", "Bell Peppers / Capsicum", "Spinach / Palak", "Opo Squash / Lauki", "Any Dry Leftover Sabzi"]:
            if st.checkbox(item, value=True, key=f"base_{item}"):
                active_inventory.append(item)
                
    with st.expander("🧀 Proteins, Dairy & Flours", expanded=False):
        for item in ["Paneer", "Cheese", "Curd / Dahi", "Gram Flour / Besan", "Wheat Flour / Atta"]:
            if st.checkbox(item, value=True, key=f"base_{item}"):
                active_inventory.append(item)

    with st.expander("🌾 Grains, Staples & Pulses", expanded=False):
        for item in ["Bread Slice", "Roti / Wraps", "Poha", "Rice", "Pasta / Macaroni", "Oats (Flakes/Flour)", "Toor Dal (Arhar)", "Moong Dal", "Chana Dal / Kala Chana", "White Chickpeas (Kabuli Chana)"]:
            if st.checkbox(item, value=True, key=f"base_{item}"):
                active_inventory.append(item)

    st.markdown("---")
    st.markdown("#### 🔒 Add New Active Ingredients:")
    
    new_item_input = st.text_input("Type item name (e.g., Cucumber, Mushrooms):", placeholder="e.g., Lettuce")
    if st.button("➕ Add Ingredient to List", use_container_width=True):
        cleaned_item = new_item_input.strip()
        if cleaned_item and cleaned_item not in st.session_state.custom_ingredients and cleaned_item not in DEFAULT_BASE_INGREDIENTS:
            st.session_state.custom_ingredients.append(cleaned_item)
            st.success(f"🎉 '{cleaned_item}' added!")
            st.rerun()

    if st.session_state.custom_ingredients:
        with st.expander("⭐ Your Custom Additions", expanded=True):
            for idx, item in enumerate(st.session_state.custom_ingredients):
                col1, col2 = st.columns([0.85, 0.15])
                with col1:
                    if st.checkbox(item, value=True, key=f"perm_check_{idx}"):
                        active_inventory.append(item)
                with col2:
                    if st.button("🗑️", key=f"del_ing_{idx}"):
                        st.session_state.custom_ingredients.remove(item)
                        st.rerun()

# ==========================================
# PROCESSING UTILITY LOGIC FOR MATCH CALCULATIONS
# ==========================================
def calculate_recipe_matches(recipe_list, current_stock):
    results = []
    for recipe in recipe_list:
        matched_items = [item for item in recipe["required"] if item in current_stock]
        missing_items = [item for item in recipe["required"] if item not in current_stock]
        score = len(matched_items) / len(recipe["required"]) if recipe["required"] else 0
        results.append({
            "recipe": recipe,
            "matched": matched_items,
            "missing": missing_items,
            "score": score
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)

# ==========================================
# TAB 2: MAIN MEALS SUGGESTION PAGE
# ==========================================
with tab2:
    st.subheader("🤖 Live Meal Planner Engine")
    main_matches = calculate_recipe_matches(st.session_state.recipe_db, active_inventory)
    
    teen_only = st.toggle("🚀 Show Only Teen Favorites (10 & 15 yr olds)", key="teen_toggle_main")
    if teen_only:
        main_matches = [m for m in main_matches if m["recipe"]["kid_approved"]]

    if main_matches:
        st.success(f"✨ Found **{len(main_matches)} options**")
        
        dropdown_options = []
        option_map = {}
        for m in main_matches:
            r = m["recipe"]
            status = "🟢 Ready" if m["score"] == 1.0 else f"🟡 Missing {len(m['missing'])}" if m["score"] > 0 else "🔴 Out of Stock"
            label = f"{status}: {r['name']} ({r['time']})"
            if r["kid_approved"]:
                label += " 🌟"
            dropdown_options.append(label)
            option_map[label] = m

        selected_label = st.selectbox("Pick a meal option to see cooking details:", dropdown_options, key="main_selectbox")
        if selected_label:
            match = option_map[selected_label]
            rec = match["recipe"]
            st.markdown(f"### {rec['name']}")
            st.caption(f"⏱️ Time: {rec['time']} | Tag: {rec['staple']}")
            if match["missing"]:
                st.warning(f"⚠️ **Missing items:** {', '.join(match['missing'])}")
            st.image(rec["image"], use_container_width=True)
            st.markdown("**📑 Preparation steps:**")
            for idx, step in enumerate(rec["instructions"]):
                st.markdown(f"{idx+1}. {step}")

# ==========================================
# TAB 3: DEDICATED BREAKFAST & DRY LUNCHBOX FILTERS
# ==========================================
with tab3:
    st.subheader("🎒 Dry Breakfast & School Lunchbox Options")
    
    lunchbox_recipes = [r for r in st.session_state.recipe_db if r.get("is_lunchbox", False)]
    lunchbox_matches = calculate_recipe_matches(lunchbox_recipes, active_inventory)
    
    if not lunchbox_matches:
        st.info("No lunchbox items matched.")
    else:
        lunch_dropdown_options = []
        lunch_option_map = {}
        for m in lunchbox_matches:
            r = m["recipe"]
            status = "🟢 Ready" if m["score"] == 1.0 else f"🟡 Missing {len(m['missing'])} items"
            label = f"{status}: {r['name']}"
            if r["kid_approved"]:
                label += " 🌟"
            lunch_dropdown_options.append(label)
            lunch_option_map[label] = m
            
        selected_lunch_label = st.selectbox("Select morning lunchbox plan:", lunch_dropdown_options, key="lunch_selectbox")
        if selected_lunch_label:
            match = lunch_option_map[selected_lunch_label]
            rec = match["recipe"]
            st.markdown(f"### {rec['name']}")
            if match["missing"]:
                st.error(f"❌ Missing items: {', '.join(match['missing'])}")
            st.image(rec["image"], use_container_width=True)
            st.markdown("**🎒 Packing Instructions:**")
            for idx, step in enumerate(rec["instructions"]):
                st.markdown(f"{idx+1}. {step}")

# ==========================================
# TAB 4: USER RECIPE LOGGING PORTAL
# ==========================================
with tab4:
    st.subheader("✍️ Log a New Recipe")
    
    with st.form("permanent_recipe_form", clear_on_submit=True):
        new_name = st.text_input("Recipe Title:", placeholder="e.g., Soya Chunk Fried Rice")
        new_time = st.text_input("Cooking Duration:", placeholder="e.g., 20 mins")
        new_staple = st.selectbox("Meal Category Tag:", ["Bataka-Powa", "Wraps/Frankies", "Dal-Chawal", "Rice & Pulav Dishes", "Mexican/Continental"])
        
        new_is_lunchbox = st.checkbox("🍱 Is this a safe, dry breakfast item suitable for school lunchboxes?")
        new_is_teen = st.checkbox("🌟 Is this a kid/teen approved favorite dish?")
        
        new_req_text = st.text_input("Required Ingredients (comma-separated entries):", placeholder="Rice, Onion, Tomato")
        new_steps_text = st.text_area("Cooking Instructions (One step per line description):", placeholder="Step 1...\nStep 2...")
        new_img_url = st.text_input("Photo Link:", value="https://images.unsplash.com/photo-1498837167922-ddd27525d352?q=80&w=600&auto=format&fit=crop")
        
        if st.form_submit_button("💾 Save to App Session"):
            if not new_name or not new_req_text or not new_steps_text:
                st.error("Please fill out Name, Ingredients, and Steps before saving!")
            else:
                ingredients_parsed = [i.strip() for i in new_req_text.split(",") if i.strip()]
                steps_parsed = [s.strip() for s in new_steps_text.split("\n") if s.strip()]
                
                new_recipe_dict = {
                    "name": new_name.strip(),
                    "time": new_time.strip() if new_time.strip() else "20 mins",
                    "staple": new_staple,
                    "kid_approved": new_is_teen,
                    "is_lunchbox": new_is_lunchbox,
                    "required": ingredients_parsed,
                    "image": new_img_url.strip(),
                    "instructions": steps_parsed
                }
                
                st.session_state.recipe_db.append(new_recipe_dict)
                st.success(f"🎉 '{new_name}' added to your app! Check Tab 2 or Tab 3.")
                st.rerun()
