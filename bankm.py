import streamlit as st
from pathlib import Path
import json
import random
import string

# -----------------------------------------------------
# ---------------------- BACKEND ----------------------
# -----------------------------------------------------

class Bank:
    database = 'database.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                try:
                    data = json.load(fs)
                except:
                    data = []
        else:
            data = []
    except Exception as err:
        print(f"An error occured: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        acc = alpha + digits
        random.shuffle(acc)
        return "".join(acc)

    def create_account(self, Name, Email_Id, Phone_No, PIN):
        if not Name or not Email_Id or not Phone_No or not PIN:
            return False, "All fields required."
        if len(Phone_No) != 10 or not Phone_No.isdigit():
            return False, "Invalid phone number!"
        if len(PIN) != 4 or not PIN.isdigit():
            return False, "PIN must be 4 digits!"

        d = {
            "Name": Name,
            "Email_Id": Email_Id,
            "Phone_No": Phone_No,
            "PIN": PIN,
            "Account_No": Bank.__accountno(),
            "Balance": 0,
            "Transactions": []
        }
        Bank.data.append(d)
        Bank.__update()
        return True, d["Account_No"]

    def verify_user(self, acc, pin):
        user = [u for u in Bank.data if u["Account_No"] == acc and u["PIN"] == pin]
        return user[0] if user else None

    def deposit(self, user, amount):
        if amount <= 0: return False, "Amount must be positive"
        if amount > 25000: return False, "Deposit limit ₹25,000"
        user["Balance"] += amount
        user["Transactions"].append({"Type": "Deposit", "Amount": amount})
        Bank.__update()
        return True, "Done"

    def withdraw(self, user, amount):
        if amount <= 0: return False, "Amount must be positive"
        if amount > 10000: return False, "Withdraw limit ₹10,000"
        if amount > user["Balance"]: return False, "Insufficient balance"
        user["Balance"] -= amount
        user["Transactions"].append({"Type": "Withdraw", "Amount": amount})
        Bank.__update()
        return True, "Done"

    def update(self, user, name, email, phone, pin):
        if phone and (len(phone) != 10 or not phone.isdigit()):
            return False, "Invalid phone number"
        if pin and (len(pin) != 4 or not pin.isdigit()):
            return False, "PIN must be 4 digits"

        if name: user["Name"] = name
        if email: user["Email_Id"] = email
        if phone: user["Phone_No"] = phone
        if pin: user["PIN"] = pin

        Bank.__update()
        return True, "Updated"

    def transfer(self, sender, receiver, amount):
        if amount <= 0: return False, "Amount must be positive"
        if amount > 25000: return False, "Limit ₹25,000"
        if amount > sender["Balance"]: return False, "Insufficient balance"

        sender["Balance"] -= amount
        receiver["Balance"] += amount

        # Updated friendly transaction messages
        sender["Transactions"].append({"Type": f"Fund transferred to {receiver['Name']}", "Amount": amount})
        receiver["Transactions"].append({"Type": f"Fund received from {sender['Name']}", "Amount": amount})

        Bank.__update()
        return True, "Done"

    def interest(self, user):
        return (user["Balance"] * 5 * 1) / 100

    def delete(self, user):
        Bank.data.remove(user)
        Bank.__update()
        return True

bank = Bank()

# -----------------------------------------------------
# ---------------- CORPORATE GOLD UI -------------------
# -----------------------------------------------------

st.set_page_config(page_title="Royal Banking Suite", layout="centered")

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
body {
    background: linear-gradient(135deg, #0A2342, #031527, #000B18);
}
h1, h2, h3 {
    color: #FFD700 !important;
    font-family: 'Playfair Display', serif;
}
.gold-line {
    height: 3px;
    background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
    border-radius: 4px;
    margin-bottom: 20px;
}
.gold-card {
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(255, 215, 0, 0.6);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.25);
}
.stButton > button {
    background: linear-gradient(135deg, #daa520, #ffd700);
    color: black;
    font-weight: 600;
    border-radius: 10px;
    padding: 12px 26px;
    border: none;
    font-size: 17px;
    transition: 0.3s ease-in-out;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ffd700, #fff5b3);
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
}
.css-1d391kg {
    background: #081a30 !important;
}
.css-1d391kg * {
    color: #ffd700 !important;
}
[data-testid="stSidebar"] {
    border-right: 2px solid rgba(255, 215, 0, 0.25);
}
input {
    border-radius: 8px !important;
    border: 1px solid #ffd700 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏛 PRIME BANKING SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<div class='gold-line'></div>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "💠 Executive Menu",
    ["🏦 Create Account", "💰 Deposit Money", "🏧 Withdraw Money", "📊 Check Balance",
     "👤 User Details", "✏ Update Details", "📜 Transaction History",
     "🔁 Fund Transfer", "📈 Interest Calculator", "❌ Close Account"]
)

def card_start():
    st.markdown("<div class='gold-card'>", unsafe_allow_html=True)

def card_end():
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CREATE ACCOUNT ----------------
if menu == "🏦 Create Account":
    card_start()
    st.subheader("Open a New Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    pin = st.text_input("4-Digit PIN", type="password")
    if st.button("Create Account"):
        ok, msg = bank.create_account(name, email, phone, pin)
        if ok:
            st.success(f"🎉 Account Created!\nAccount Number: {msg}")
        else:
            st.error(msg)
    card_end()

# ---------------- DEPOSIT ----------------
elif menu == "💰 Deposit Money":
    card_start()
    st.subheader("Deposit Funds")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Deposit Amount", min_value=1)
    if st.button("Deposit"):
        user = bank.verify_user(acc, pin)
        if user:
            ok, msg = bank.deposit(user, amount)
            if ok:
                st.success("Amount Deposited")
            else:
                st.error(msg)
        else:
            st.error("Invalid Credentials")
    card_end()

# ---------------- WITHDRAW ----------------
elif menu == "🏧 Withdraw Money":
    card_start()
    st.subheader("Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Withdraw Amount", min_value=1)
    if st.button("Withdraw"):
        user = bank.verify_user(acc, pin)
        if user:
            ok, msg = bank.withdraw(user, amount)
            if ok:
                st.success("Withdrawal Successful")
            else:
                st.error(msg)
        else:
            st.error("Invalid Credentials")
    card_end()

# ---------------- BALANCE ----------------
elif menu == "📊 Check Balance":
    card_start()
    st.subheader("Account Balance Inquiry")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Check Balance"):
        user = bank.verify_user(acc, pin)
        if user:
            st.success(f"Current Balance: ₹{user['Balance']}")
        else:
            st.error("Invalid Credentials")
    card_end()

# ---------------- USER DETAILS ----------------
elif menu == "👤 User Details":
    card_start()
    st.subheader("Account Holder Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Show Details"):
        user = bank.verify_user(acc, pin)
        if user:
            st.info(f"Name: {user['Name']}")
            st.info(f"Email: {user['Email_Id']}")
            st.info(f"Phone: {user['Phone_No']}")
            st.info(f"Balance: ₹{user['Balance']}")
        else:
            st.error("Invalid Credentials")
    card_end()

# ---------------- UPDATE DETAILS ----------------
elif menu == "✏ Update Details":
    card_start()
    st.subheader("Update Account Information")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    name = st.text_input("New Name")
    email = st.text_input("New Email")
    phone = st.text_input("New Phone Number")
    new_pin = st.text_input("New PIN", type="password")
    if st.button("Update"):
        user = bank.verify_user(acc, pin)
        if user:
            ok, msg = bank.update(user, name, email, phone, new_pin)
            if ok:
                st.success("Details Updated")
            else:
                st.error(msg)
        else:
            st.error("Invalid Credentials")
    card_end()

# ---------------- TRANSACTION HISTORY ----------------
elif menu == "📜 Transaction History":
    card_start()
    st.subheader("Transaction History")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Show History"):
        user = bank.verify_user(acc, pin)
        if user:
            if user["Transactions"]:
                for t in user["Transactions"]:
                    st.write(f"**{t['Type']}** — ₹{t['Amount']}")
            else:
                st.info("No transactions yet.")
        else:
            st.error("Invalid Credentials")
    card_end()

# ---------------- FUND TRANSFER ----------------
elif menu == "🔁 Fund Transfer":
    card_start()
    st.subheader("Transfer Funds")
    s_acc = st.text_input("Sender Account")
    s_pin = st.text_input("Sender PIN", type="password")
    r_acc = st.text_input("Receiver Account")
    amount = st.number_input("Transfer Amount", min_value=1)
    if st.button("Transfer"):
        sender = bank.verify_user(s_acc, s_pin)
        receiver = next((u for u in bank.data if u["Account_No"] == r_acc), None)
        if not sender:
            st.error("Invalid Sender Credentials")
        elif not receiver:
            st.error("Receiver Account Not Found")
        else:
            ok, msg = bank.transfer(sender, receiver, amount)
            if ok:
                st.success("Transfer Successful")
            else:
                st.error(msg)
    card_end()

# ---------------- INTEREST ----------------
elif menu == "📈 Interest Calculator":
    card_start()
    st.subheader("5% Annual Interest")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Calculate Interest"):
        user = bank.verify_user(acc, pin)
        if user:
            st.success(f"Annual Interest: ₹{bank.interest(user)}")
        else:
            st.error("Invalid Credentials")
    card_end()

# ---------------- DELETE ACCOUNT ----------------
elif menu == "❌ Close Account":
    card_start()
    st.subheader("Close Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Delete Account"):
        user = bank.verify_user(acc, pin)
        if user:
            bank.delete(user)
            st.success("Account Closed Successfully")
        else:
            st.error("Invalid Credentials")
    card_end()
