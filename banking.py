#Sushil Gautam
#Student ID: 11844192

#Define encrypted password to return each character shifted to 3 position
def encrypted_password(password):
  encrypted_password = ""

  for char in password:
    if char.isdigit(): #if digit shift to 3 position
      base = 48
      digit_range = 10
      encrypted_char = chr((ord(char) - base + 3) % digit_range + base)

    elif char.isalpha(): #if alpha shift to 3 position
      alpha_range = 26

      if char.isupper():
        base = 65

      elif char.islower():
        base = 97
      encrypted_char = chr((ord(char) - base + 3) % alpha_range + base)

    else:
      encrypted_char = char #if not both alpha and digit remains unchanged
    encrypted_password = encrypted_password + encrypted_char

  return encrypted_password #return shifted characters

#Define function login user to check input id and password matched
def login_user():
  #Ask user to input id and password
  user_id = input("Enter user ID: ")
  password = encrypted_password(input("Enter password: "))
  if user_id == user_data["ID"] and password == user_data["password"]:
    print(f"User {user_id} logged in successfully.")
    return True  #if matched login successful
  else:
    print("User ID or password did not matched. Please try again.")
    return False #if not matcged login failed

#Define deposit amount function to deposit specific amount given by user
def deposit_amount():

  #Ask user for amount to deposit and convert to float
  amount = float(input("Enter deposit amount: $"))

  if amount > 0: #if amount is greater than zero, deposit and print balance
    balance = user_data["balance"] + amount
    user_data["balance"] = balance
    print(f"New balance: ${balance:.2f}")

  else:  #if amount is less than or equal to zero, print error
    print("Deposit amount must be greater than zero. Transaction failed!")

#Define withdraw amount function to withdraw specific amount given by user
def withdraw_amount():

 #Ask user for amount to withdraw and convert to float
  amount = float(input("Enter withdrawal amount: $"))

  #if amount is greater than zero and equal or less than available balance
  if amount > 0:
    if user_data["balance"] >= amount:
      balance = user_data["balance"] - amount
      user_data["balance"] = balance
      print(f"New balance: ${balance:.2f}") #withdraw amount and print balance

    else: #else print balance not sufficient to withdraw
      print("Insufficient funds! Transaction failed.")

  else: #if amount is not greater than zero, print error
    print("Withdrawn amount must be greater than zero. Transaction failed!")

#Define print balance to print available balance in the account
def print_balance():
  balance = user_data["balance"]
  user_id = user_data["ID"]
  print(f"{user_id} balance: ${balance:.2f}")


#Define change password function to change the password
def change_password():
  new_password = input("Enter new password: ")
  user_data["password"] = encrypted_password(new_password)
  print("Password updated successfully. Please login again.")
  return False #set login as False

#Define logout function to print message when logout from the program
def logout():
  user_id = user_data["ID"]
  print(f"User {user_id} logged out from the account.")
  print("Thank you for using the Simple Banking System!")
  return False #Set login as False


#Define debug fuction to print user_data and login status
def debug():
  print(user_data)
  print(login)


#Ask user to input ID, password, and initial balance and store in dictionary user_data
print("Welcome to the Simple Banking System!")
user_data = {
      "ID" : None,
      "password" : None,
      "balance" : 0.00
      }

user_data["ID"] = input("Enter new user ID: ")
user_data["password"] = encrypted_password(input("Enter password: "))
#if input Initial Balance accepts float and greater or equal to zero
try:
  input_balance = float(input("Enter initial balance: "))
  if input_balance >= 0:
    user_data["balance"] = float(input_balance) #increment amount in dictionary
  else: #else print balance can not be negative
    print("Initial balance can not be negative. Initial Balance set to $0.00")

#If value error initial balance remain unchanged
except ValueError:
  print("Invalid Iitial balance! Initial balance set to $0.00")

print("Account created successfully!")

#Login status of origin is False
login = False


#Main program
while True:
  #prints menu option
  print(f"\n{'*' * 22} MENU {'*' * 22}")
  print("Select a service:")
  print("1. Login to Account")
  print("2. Deposit to Account")
  print("3. Withdraw from Account")
  print("4. Print Balance")
  print("5. Change Password")
  print("6. Exit/Logout")
  print('*' * 50)

  try:
    #Ask user to choose choice
    input_choice = input("Enter choice> ")
    choice = int(input_choice)

#Run function or prints message according to the choice
    if choice == 6 and login: #if choice 1 and login, execute logout & break
      login = logout()
      break

    elif choice == 6: #if choice 6, print message and break
      print("Thanks for using Simple Banking System.")
      break

    elif choice > 1 and not login: #if choice greater than 1 and not login
      print("Account details are hidden from public view") #print message
      print("Login required!") #print message

    elif choice == 1 and login: #if choice 1 and login, print message
      print("You are already logged in.")

    elif choice == 1: #if choice is 1
      login = login_user() #execute login_user

    elif choice == 2 and login: #if choice is 2 and login
      deposit_amount()  #execute deposit_amount

    elif choice == 3 and login: #if choice is 3 and login
      withdraw_amount()  #execute withdraw_amount

    elif choice == 4 and login: #if choice is 4 and login
      print_balance()  #execute print_balance

    elif choice == 5 and login: #if choice is 5 and login
      login = change_password() #execute change_password

    elif choice == 0: #if choice is 0
      debug()  #execute debug

    else:  #else ask input between 1 and 6
      print("Invalid Input! Choose between 1 and 6.")

  except ValueError: #for value error, print amount must be numeric
    print("Input must be numeric. Transaction failed!")
