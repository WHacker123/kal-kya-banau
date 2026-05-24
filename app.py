import streamlit as st
import json
import os

# Set up mobile-first browser configuration
st.set_page_config(page_title="Kal Kya Banau?", page_icon="🍳", layout="centered")

# File path for permanent database storage across page refreshes
DB_FILE = "recipe_pantry_db.json"

# Core recipe database containing categories and lunchbox identifiers
DEFAULT_RECIPES = [
    {
        "name": "Classic Homestyle Bataka-Powa",
        "time": "20 mins",
        "staple": "Bataka-Powa",
        "kid_approved": True,
        "is_lunchbox": True,  # Dry food suited for school afternoon lunch boxes
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
        "is_lunchbox": False, # Too messy/wet for school lunchbox
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

# Helper function to load app state from local storage file
def load_permanent_db():
    if not os.path.exists(DB_FILE):
        initial_data = {
            "recipes": DEFAULT_RECIPES,
            "custom_ingredients": ["Lettuce"] # Pre-loaded so it is ready
        }
        with open(DB_FILE, "w") as f:
            json.dump(initial_data, f, indent=4)
        return initial_data
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"recipes": DEFAULT_RECIPES, "custom_ingredients": ["Lettuce"]}

# Helper function to write app state back to local storage file
def save_permanent_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load data and sync into Session States
app_data = load_permanent_db()
if "recipe_db" not in st.session_state:
    st.session_state.recipe_db = app_data["recipes"]
if "custom_ingredients" not in st.session_state:
    st.session_state.custom_ingredients = app_data["custom_ingredients"]

# Application Branding Headers
st.title("🍳 Kal Kya Banau?")
st.markdown("##### Smart Mobile Meal Planner & Permanent Pantry Engine")
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
    
    # 1. Fresh vegetables section
    with st.expander("🥦 Fresh Produce & Leftovers", expanded=True):
        for item in ["Potato", "Onion", "Tomato", "Bell Peppers / Capsicum", "Spinach / Palak", "Opo Squash / Lauki", "Any Dry Leftover Sabzi"]:
            if st.checkbox(item, value=True, key=f"base_{item}"):
                active_inventory.append(item)
                
    # 2. Proteins & Flours section
    with st.expander("🧀 Proteins, Dairy & Flours", expanded=False):
        for item in ["Paneer", "Cheese", "Curd / Dahi", "Gram Flour / Besan", "Wheat Flour / Atta"]:
            if st.checkbox(item, value=True, key=f"base_{item}"):
                active_inventory.append(item)

    # 3. Grains & Pulses section
    with st.expander("🌾 Grains, Staples & Pulses", expanded=False):
        for item in ["Bread Slice", "Roti / Wraps", "Poha", "Rice", "Pasta / Macaroni", "Oats (Flakes/Flour)", "Toor Dal (Arhar)", "Moong Dal", "Chana Dal / Kala Chana", "White Chickpeas (Kabuli Chana)"]:
            if st.checkbox(item, value=True, key=f"base_{item}"):
                active_inventory.append(item)

    # 4. Permanent Ingredient Addition Section
    st.markdown("---")
    st.markdown("#### 🔒 Add New Permanent Ingredients:")
    st.caption("Items typed here save permanently into the app database file and survive page refreshes.")
    
    new_item_input = st.text_input("Type item name (e.g., Cucumber, Mushrooms):", placeholder="e.g., Lettuce")
    if st.button("➕ Save Ingredient to App", use_container_width=True):
        cleaned_item = new_item_input.strip()
        if cleaned_item and cleaned_item not in st.session_state.custom_ingredients and cleaned_item not in DEFAULT_BASE_INGREDIENTS:
            st.session_state.custom_ingredients.append(cleaned_item)
            app_data["custom_ingredients"] = st.session_state.custom_ingredients
            save_permanent_db(app_data)
            st.success(f"🎉 '{cleaned_item}' is now permanently added to your app checklist!")
            st.rerun()

    # Display dynamically saved additions with active checkboxes and deletion keys
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
                        app_data["custom_ingredients"] = st.session_state.custom_ingredients
                        save_permanent_db(app_data)
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
        st.success(f"✨ Found **{len(main_matches)} options** sorted by active availability percentages.")
        
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
                st.warning(f"⚠️ **Missing items to buy/prepare:** {', '.join(match['missing'])}")
            st.image(rec["image"], use_container_width=True)
            st.markdown("**📑 Preparation steps:**")
            for idx, step in enumerate(rec["instructions"]):
                st.markdown(f"{idx+1}. {step}")

# ==========================================
# TAB 3: DEDICATED BREAKFAST & DRY LUNCHBOX FILTERS
# ==========================================
with tab3:
    st.subheader("🎒 Dry Breakfast & School Lunchbox Options")
    st.caption("This tab filters out messy, wet curries. It displays dry food items (like Poha, Cheese Koki, Sandwiches, Pulav, Biryani) that stay perfect in a school bag until afternoon lunch period.")
    
    # Filter strictly for dry, lunchbox-safe recipes
    lunchbox_recipes = [r for r in st.session_state.recipe_db if r.get("is_lunchbox", False)]
    lunchbox_matches = calculate_recipe_matches(lunchbox_recipes, active_inventory)
    
    if not lunchbox_matches:
        st.info("No lunchbox items matched. Head to tab 4 to add new custom recipes!")
    else:
        st.info("💡 **Packing Tip:** Let these cool down slightly before shutting the lunch box lids to avoid condensation and sogginess.")
        
        lunch_dropdown_options = []
        lunch_option_map = {}
        for m in lunchbox_matches:
            r = m["recipe"]
            status = "🟢 Pack Ready" if m["score"] == 1.0 else f"🟡 Missing {len(m['missing'])} items"
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
                st.error(f"❌ Missing items to fulfill packing requirement: {', '.join(match['missing'])}")
            st.image(rec["image"], use_container_width=True)
            st.markdown("**🎒 Packing Instructions:**")
            for idx, step in enumerate(rec["instructions"]):
                st.markdown(f"{idx+1}. {step}")

# ==========================================
# TAB 4: PERMANENT USER RECIPE LOGGING PORTAL
# ==========================================
with tab4:
    st.subheader("✍️ Log a New Permanent Recipe")
    st.caption("Saved meals write directly into the persistent storage file layout instantly.")
    
    with st.form("permanent_recipe_form", clear_on_submit=True):
        new_name = st.text_input("Recipe Title:", placeholder="e.g., Soya Chunk Fried Rice")
        new_time = st.text_input("Cooking Duration:", placeholder="e.g., 20 mins")
        new_staple = st.selectbox("Meal Category Tag:", ["Bataka-Powa", "Wraps/Frankies", "Dal-Chawal", "Rice & Pulav Dishes", "Mexican/Continental"])
