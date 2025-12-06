from pathlib import Path
import json
import random
import string


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
        alpha   = random.choices(string.ascii_letters, k=5)
        digits  = random.choices(string.digits, k=4)
        acc     = alpha + digits

        random.shuffle(acc)
        return "".join(acc)
    
    def create_account(self):
        Name        = input("Please enter your name: ")
        Email_Id    = input("Please enter your email id: ")
        Phone_No    = input("Please enter your 10-digit phone number: ")
        PIN         = input("Please enter your 4-digit PIN: ")

        if not Name or not Email_Id or not Phone_No or not PIN:
            print("Incomplete details. Please fill all information!")
            return
        if len(Phone_No) != 10 or not Phone_No.isdigit():
            print("Please enter valid 10-digit phone number!")
            return
        if len(PIN) != 4 or not PIN.isdigit():
            print("Please enter correct 4-digit PIN!")
            return
        
        d = {
            "Name"          : Name,
            "Email_Id"      : Email_Id,
            "Phone_No"      : Phone_No,
            "PIN"           : PIN,
            "Account_No"    : Bank.__accountno(),
            "Balance"       : 0,
            "Transactions"  : [] 
        }
        
        Bank.data.append(d)
        Bank.__update()
        print("\nAccount created successfully!")
        print(f"Your account number: {d['Account_No']}\n")

        #""""""""""""""""""DEPOSIT MONEY """"""""""""""""""

    def deposit_money(self):
        accNo   = input("Please enter your account number: ")
        PIN     = input("Please enter your 4-digit PIN: ")

        user_data = [i for i in Bank.data if accNo == i['Account_No'] and PIN == i['PIN']]

        if not user_data:
            print("User not found!")
            return
        
        user = user_data[0]
        print(f"\nWelcome {user['Name']}!")
        print(f"Your current balance: {user['Balance']}.")

        while True:
            try:
                amount = int(input("Please enter amount to deposit: "))

                if amount <= 0:
                    print("Amount must be in positive!")
                    return
                elif amount > 25000:
                    print("Deposit limit is ₹25,000!")
                    return
                break
            except ValueError:
                print("Wrong input!\nEnter amount in numbers.")
                continue

        user['Balance'] += amount
        user['Transactions'].append({
            "Type": "Deposit",
            "Amount": amount
        })

        Bank.__update()

        print("Amount credited successfully!")
        print(f"Your new balance: {user['Balance']}")          

        #""""""""""""""""""WITHDRAW MONEY """"""""""""""""""

    def withdraw_money(self):
        accNo   = input("Please enter your account number: ")
        PIN     = input("Please enter your 4-digit PIN: ")

        user_data = [i for i in Bank.data if accNo == i['Account_No'] and PIN == i['PIN']]

        if not user_data:
            print("User not found!")
            return
        
        user = user_data[0]
        print(f"\nWelcome {user['Name']}!")
        print(f"Your current balance: {user['Balance']}.")

        while True:
            try:
                amount = int(input("Please enter amount to withdraw: "))

                if amount <= 0:
                    print("Amount must be in positive!")
                    return
                elif amount > 10000:
                    print("Withdraw limit is ₹10,000!")
                    return
                elif amount > user['Balance']:
                    print("Insufficient Fund!")
                    return
                break
            except ValueError:
                print("Wrong input! Please enter amount in numbers.")
                continue

        user['Balance'] -= amount

        user['Transactions'] .append({
            "Type": "Withdraw",
            "Amount": amount
        })

        Bank.__update()
        print("\nAmount debited successfully!")
        print(f"Your new balance: {user['Balance']}")

        #""""""""""""""""""USER DETAILS """"""""""""""""""

    def user_details(self):
        accNo   = input("Please enter your account number: ")
        PIN     = input("Please enter your 4-digit PIN: ")

        user_data = [i for i in Bank.data if accNo == i['Account_No'] and PIN == i['PIN']]

        if not user_data:
            print("User not found!")
            return
        
        user = user_data[0]

        print("\n----- USER DETAILS -----")
        for key, value in user.items():
            if key != "PIN" and key != "Transactions":
                print(f"{key}: {value}")
        print("------------------------------\n")

        #""""""""""""""""""UPDATE DETAILS """"""""""""""""""

    def update_details(self):
        accNo   = input("Please enter your account number: ")
        PIN     = input("Please enter your 4-digit PIN: ")

        user_data = [i for i in Bank.data if accNo == i['Account_No'] and PIN == i['PIN']]

        if not user_data:
            print("User not found!")
            return
        
        user = user_data[0]

        print("\n----- Current Details -----")
        for key, value in user.items():
            if key != "Transactions":
                print(f"{key}: {value}")
        print("------------------------------")

        print("\nPlease enter new details(Press enter to skip): ")

        new_name        = input("New Name: ")
        new_email_id    = input("New Email id: ")
        new_phone_no    = input("New Phone number: ")
        new_PIN         = input("New PIN: ")

        if new_phone_no and (len(new_phone_no) != 10 or not new_phone_no.isdigit()):
            print("Please enter valid 10-digit number!")
            return
        if new_PIN and (len(new_PIN) != 4 or not new_PIN.isdigit()):
            print("PIN must be 4-digit: ")
            return
        
        if new_name     : user['Name'] = new_name
        if new_email_id : user['Email_Id'] = new_email_id
        if new_phone_no : user['Phone_No'] = new_phone_no
        if new_PIN      : user['PIN'] = new_PIN

        Bank.__update()
        print("Details updated successfully!")
        
    # ------------------- CHECK BALANCE -------------------

    def check_balance(self):
        accNo   = input("Please enter your account number: ")
        PIN     = input("Please enter your 4-digit PIN: ")

        user_data = [i for i in Bank.data if accNo == i['Account_No'] and PIN == i['PIN']]

        if not user_data:
            print("User not found!")
            return
        
        user = user_data[0]  

        print(f"\nHello, {user['Name']}\nYour current balance is {user['Balance']}")

    # ------------------- TRANSACTION HISTORY -------------------

    def view_transaction_history(self):
        accNo   = input("Please enter your account number: ")
        PIN     = input("Please enter your 4-digit PIN: ")

        user_data = [i for i in Bank.data if accNo == i['Account_No'] and PIN == i['PIN']]

        if not user_data:
            print("User not found!")
            return
        
        user = user_data[0] 
        
        if not user['Transactions']:
            print("No transactions yet")
        else:
            print(f"\nHello, {user['Name']}!\nYour current balance is {user['Balance']}.")
            for t in user['Transactions']:
                print(f"{t['Type']}: {t['Amount']}")
            print("---------------------------") 

    # ------------------- DELETE ACCOUNT -------------------

    def delete_account(self):
        accNo   = input("Please enter your account number: ")
        PIN     = input("Please enter your 4-digit PIN: ")

        user_data = [i for i in Bank.data if accNo == i['Account_No'] and PIN == i['PIN']]

        if not user_data:
            print("User not found!")
            return
        
        user = user_data[0]  
        confirm = input(f"Are you sure you want to delete {user['Name']}'s account? (y/n): ").lower()
        if confirm != 'y':
            print("Account deletion cancelled.")
            return
        Bank.data.remove(user)
        Bank.__update()
        print(f"Account of {user['Name']} deleted successfully!")                                               
            
    # ------------------- FUND TRANSFER -------------------

    def fund_transfer(self):
        sender_accNo   = input("Please enter your account number: ")
        sender_PIN     = input("Please enter your 4-digit PIN: ")

        sender_data = [i for i in Bank.data if sender_accNo == i['Account_No'] and sender_PIN == i['PIN']]

        if not sender_data:
            print("Sender not found!")
            return
        
        sender = sender_data[0] 

        receiver_accNo = input("Please enter receiver's account number: ")
        receiver_data = [k for k in Bank.data if receiver_accNo == k['Account_No']]

        if not receiver_data:
            print("Receiver not found")
            return
        
        receiver = receiver_data[0]

        amount = int(input("Please enter amount to transfer: "))

        if amount <= 0:
            print("Amount must be in positive!")
            return
        if amount > sender['Balance']:
            print("Insufficient Amount!")
            return
        if amount > 25000:
            print("Transfer limit is ₹25,000!")
            return
        
        sender['Balance'] -= amount
        receiver['Balance'] += amount

        sender['Transactions'].append({
            "Type": f"Fund Transfered to {receiver['Name']}",
            "Amount": amount
        })
        receiver['Transactions'].append({
            "Type": f"Fund Received from {sender['Name']}",
            "Amount": amount     
        })

        Bank.__update()
        print(f"\nTransfer successfull!\nYou sent {amount} to {receiver['Name']}'s account.")
        print(f"Your new balance is {sender['Balance']}....")

    # ------------------- CALCULATE INTEREST -------------------

    def calculate_interest(self):
        accNo   = input("Please enter your account number: ")
        PIN     = input("Please enter your 4-digit PIN: ")

        user_data = [i for i in Bank.data if accNo == i['Account_No'] and PIN == i['PIN']]

        if not user_data:
            print("User not found!")
            return
        
        user = user_data[0] 

        rate = 5
        year = 1

        SI = (user['Balance'] * rate * year) / 100

        print(f"\nHello, {user['Name']}!\nYour yearly interest at 5% rate is {SI}.")


user = Bank()
while True:
    print("\n----- Bank Menu -----")
    print("1. Create Account.")
    print("2. Deposit Money.")
    print("3. Withdraw Money.")
    print("4. User Details.")
    print("5. Update Details.")
    print("6. Check Balance.")
    print("7. View Transaction History")
    print("8. Delete Account")
    print("9. Fund Transfer")
    print("10. Calculate Interest")
    print("0. Exit")

    try:
        choice = int(input("Select your option: "))
    except:
        print("That's not a number!")
        continue
    print(f"You entered: {choice}")
        
    if choice == 1:
        user.create_account()
    elif choice == 2:
        user.deposit_money()
    elif choice == 3:
        user.withdraw_money()
    elif choice == 4:
        user.user_details()
    elif choice == 5:
        user.update_details()
    elif choice == 6:
        user.check_balance()
    elif choice == 7:
        user.view_transaction_history()   
    elif choice == 8:
        user.delete_account()
    elif choice == 9:
        user.fund_transfer()
    elif choice == 10:
        user.calculate_interest()
    elif choice == 0:
        print("Exiting program.....")
        break

    else:
        print("Invalid choice! Try again.")
        break
