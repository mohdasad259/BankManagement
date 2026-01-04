import streamlit as st
import json
import datetime
import pandas as pd
import pytz  # Timezone fix karne ke liye
from pathlib import Path
from streamlit_option_menu import option_menu

# --- PAGE CONFIG ---
st.set_page_config(page_title="Hotel Management System", page_icon="🏨", layout="wide")

# --- TIMEZONE SETUP ---
IST = pytz.timezone('Asia/Kolkata')

# --- FIXED RATES ---
RATES = {
    "Single (Ac)": 2000,
    "Single (Non-Ac)": 1500,
    "Double (Ac)": 4000,
    "Double (Non-Ac)": 3000
}

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Montserrat:wght@300;400;600&family=Cinzel+Decorative:wght@700;900&display=swap');

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    input, div[data-baseweb="select"], .stNumberInput input {
        background-color: #111111 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
    }
    .hero-text {
        font-family: 'Cinzel Decorative', cursive;
        background: linear-gradient(to right, #BF953F 20%, #FCF6BA 40%, #B38728 60%, #FBF5B7 80%, #AA771C 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: clamp(45px, 10vw, 85px); font-weight: 900; text-align: center;
        margin-bottom: 0px; animation: shine 4s linear infinite;
        filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.3));
        line-height: 1.1;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .sub-text {
        font-family: 'Playfair Display', serif; text-align: center;
        color: #D4AF37 !important; letter-spacing: clamp(3px, 1vw, 8px); font-size: clamp(12px, 3vw, 18px);
        text-transform: uppercase; margin-bottom: 30px; font-style: italic; opacity: 0.8;
    }
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #D4AF37 !important; font-weight: 700 !important; }
    .bill-box {
        border: 2px solid #D4AF37; padding: 20px; border-radius: 15px;
        background: #0a0a0a !important; box-shadow: 0 0 25px rgba(212, 175, 55, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LOGIC ---
class Hotel:
    R_FILE = 'rooms_file.json'
    C_FILE = 'customers_file.json'

    @staticmethod
    def load_data():
        rooms = json.load(open(Hotel.R_FILE)) if Path(Hotel.R_FILE).exists() else []
        custs = json.load(open(Hotel.C_FILE)) if Path(Hotel.C_FILE).exists() else []
        
        now = datetime.datetime.now(IST)
        cleaned_custs = []
        for c in custs:
            if c.get('Check_out'):
                co_time = datetime.datetime.fromisoformat(c['Check_out'])
                # Timezone aware comparison
                if (now.replace(tzinfo=None) - co_time.replace(tzinfo=None)).total_seconds() < 604800: 
                    cleaned_custs.append(c)
            else:
                cleaned_custs.append(c)
        return rooms, cleaned_custs

    @staticmethod
    def save_data(rooms, custs):
        with open(Hotel.R_FILE, 'w') as f: json.dump(rooms, f, indent=4)
        with open(Hotel.C_FILE, 'w') as f: json.dump(custs, f, indent=4)

if 'rooms' not in st.session_state:
    st.session_state.rooms, st.session_state.customers = Hotel.load_data()

def sync():
    Hotel.save_data(st.session_state.rooms, st.session_state.customers)

# --- HEADER ---
st.markdown('<p class="hero-text">ROYAL   GRAND</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Experience Pure Majesty</p>', unsafe_allow_html=True)

# --- NAVIGATION ---
selected = option_menu(
    menu_title=None,
    options=["Dashboard", "All Rooms", "Available Rooms", "Search", "Book Now", "Current Guests", "Checkout", "History"],
    icons=["speedometer2", "list-ul", "check2-square", "search", "plus-circle", "people", "door-open", "clock-history"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border": "1px solid #D4AF37", "padding": "2px"},
        "nav-link": {"font-family": "Montserrat", "font-size": "11px", "padding": "5px"},
        "nav-link-selected": {"background-color": "#D4AF37", "color": "#000", "font-weight": "bold"}
    }
)

# --- 1. DASHBOARD ---
if selected == "Dashboard":
    c1, c2, c3 = st.columns(3)
    t = len(st.session_state.rooms)
    a = len([r for r in st.session_state.rooms if r['Available']])
    c1.metric("Total Rooms", t)
    c2.metric("Available Now", a)
    c3.metric("Booked", t-a)
    st.image("https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80")

# --- 2. ALL ROOMS ---
elif selected == "All Rooms":
    st.subheader("Inventory Management")
    with st.expander("➕ Register a New Room"):
        with st.form("add_form"):
            r_no = st.text_input("Room No")
            r_type = st.selectbox("Type", list(RATES.keys()))
            cap = st.number_input("Capacity", min_value=1)
            if st.form_submit_button("Save Room"):
                price = RATES[r_type]
                st.session_state.rooms.append({"Room_No": r_no, "Room_Type": r_type, "Price": price, "Capacity": cap, "Available": True})
                sync()
                st.success(f"Room {r_no} registered at Rs.{price}/day")
    
    if st.session_state.rooms:
        df = pd.DataFrame(st.session_state.rooms)
        df['Available'] = df['Available'].apply(lambda x: "Yes" if x else "No")
        st.dataframe(df, use_container_width=True, hide_index=True)

# --- 3. AVAILABLE ROOMS ---
elif selected == "Available Rooms":
    st.subheader("Available Suites")
    avail = [r for r in st.session_state.rooms if r['Available']]
    if avail:
        st.dataframe(pd.DataFrame(avail), use_container_width=True, hide_index=True)
    else:
        st.warning("No rooms are currently available.")

# --- 4. SEARCH ---
elif selected == "Search":
    st.subheader("🔍 Search Filter")
    choice = st.radio("Search By:", ["Room Type", "Capacity"], horizontal=True)
    results = []
    if choice == "Room Type":
        stype = st.selectbox("Select Type", list(RATES.keys()))
        results = [r for r in st.session_state.rooms if stype == r['Room_Type']]
    elif choice == "Capacity":
        cap_val = st.number_input("Capacity", min_value=1)
        results = [r for r in st.session_state.rooms if r['Capacity'] == cap_val]
    
    if results:
        df_res = pd.DataFrame(results)
        df_res['Available'] = df_res['Available'].apply(lambda x: "Yes" if x else "No")
        st.dataframe(df_res, use_container_width=True, hide_index=True)
    else:
        st.error("❌ No rooms available matching your criteria.")

# --- 5. BOOK NOW ---
elif selected == "Book Now":
    st.subheader("New Guest Registration")
    r_type_sel = st.selectbox("Choose Room Type", list(RATES.keys()))
    filtered_rooms = [r for r in st.session_state.rooms if r['Available'] and r['Room_Type'] == r_type_sel]
    
    if not filtered_rooms:
        st.error(f"Sorry! No {r_type_sel} rooms are available right now.")
    else:
        with st.form("book_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Customer Name").title()
                phone = st.text_input("Phone Number")
            with c2:
                aadhar = st.text_input("Aadhar ID")
                r_sel = st.selectbox("Select Available Room", [f"{r['Room_No']} (Cap: {r['Capacity']})" for r in filtered_rooms])
            guests = st.number_input("Number of Guests", min_value=1)
            
            if st.form_submit_button("Confirm Booking"):
                r_no = r_sel.split(" (")[0]
                room = next(r for r in filtered_rooms if r['Room_No'] == r_no)
                
                if guests > room['Capacity']:
                    st.error(f"Cannot Book! Max capacity of Room {r_no} is {room['Capacity']} guests.")
                elif len(phone) != 10 or not phone.isdigit():
                    st.error("Invalid Phone Number (10 digits required)")
                else:
                    room['Available'] = False
                    # Check-in time fixed with IST
                    st.session_state.customers.append({
                        "Name": name, "Phone": phone, "Aadhar": aadhar, "Room_No": r_no, 
                        "Price": room['Price'], "Check_in": str(datetime.datetime.now(IST)), "Check_out": None
                    })
                    sync()
                    st.success(f"Success! Room {r_no} has been reserved for {name}.")

# --- 6. CURRENT GUESTS ---
elif selected == "Current Guests":
    st.subheader("Guests Currently In-House")
    current = [c for c in st.session_state.customers if not c.get('Check_out')]
    if current:
        st.dataframe(pd.DataFrame(current), use_container_width=True, hide_index=True)
    else:
        st.info("No guests are staying in the hotel at the moment.")

# --- 7. CHECKOUT ---
elif selected == "Checkout":
    st.subheader("Checkout & Billing")
    active = [c for c in st.session_state.customers if not c.get('Check_out')]
    if active:
        names = [f"{c['Name']} (Room {c['Room_No']})" for c in active]
        sel = st.selectbox("Select Guest for Checkout", names)
        
        if st.button("Finalize & Generate Bill"):
            c_name = sel.split(" (")[0]
            cust = next(c for c in active if c['Name'] == c_name)
            
            check_in = datetime.datetime.fromisoformat(cust['Check_in'])
            check_out = datetime.datetime.now(IST)
            
            # Duration calculation (Fixed naive vs aware comparison)
            delta = check_out.replace(tzinfo=None) - check_in.replace(tzinfo=None)
            days = delta.days
            if days <= 0: days = 1
            total = days * cust['Price']
            
            st.markdown(f"""
            <div class="bill-box">
                <h2 style="text-align:center; color:#D4AF37; margin-bottom:10px;">ROYAL GRAND HOTEL</h2>
                <p style="text-align:center; font-style:italic;">Official Invoice</p>
                <hr style="border-color:#D4AF37;">
                <table style="width:100%; color:white; font-size:16px;">
                    <tr><td><b>Guest Name:</b></td><td style="text-align:right;">{cust['Name']}</td></tr>
                    <tr><td><b>Room Number:</b></td><td style="text-align:right;">{cust['Room_No']}</td></tr>
                    <tr><td><b>Check-in:</b></td><td style="text-align:right;">{check_in.strftime('%Y-%m-%d %I:%M %p')}</td></tr>
                    <tr><td><b>Check-out:</b></td><td style="text-align:right;">{check_out.strftime('%Y-%m-%d %I:%M %p')}</td></tr>
                    <tr><td><b>Daily Rate:</b></td><td style="text-align:right;">Rs. {cust['Price']}</td></tr>
                    <tr><td><b>Stay Duration:</b></td><td style="text-align:right;">{days} Day(s)</td></tr>
                </table>
                <hr style="border-color:#D4AF37;">
                <h3 style="text-align:right; color:#D4AF37;">NET PAYABLE: Rs. {total}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            cust['Check_out'] = str(check_out)
            cust['Total_Bill'] = total
            for r in st.session_state.rooms:
                if r['Room_No'] == cust['Room_No']: r['Available'] = True
            sync()
            st.success("Guest checked out successfully.")
    else:
        st.info("No active guests found.")

# --- 8. HISTORY ---
elif selected == "History":
    st.subheader("Booking Archives (Last 7 Days)")
    st.session_state.rooms, st.session_state.customers = Hotel.load_data()
    sync()
    history_data = [c for c in st.session_state.customers if c.get('Check_out')]
    if history_data:
        st.dataframe(pd.DataFrame(history_data), use_container_width=True, hide_index=True)
    else:
        st.info("No booking history available from the last 7 days.")