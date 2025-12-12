import bcrypt
import os

#Define the user data file path
USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    #Encode the password to bytes, required by bcrypt
    password_bytes = plain_text_password.encode('utf-8')
    #Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    #Decode the hash back to a string to store in a text file
    return hashed_password.decode('utf-8')  # Decode to string for storage

def verify_password(plain_text_password, hashed_password):
    #Encode both the plaintext password and stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    #bcrypt.checkpw handles extracting the salt and comparing
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def register_user(username, password, role='user'): 
    #Register a new user.
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    
    #Password is hashed before storage
    hashed_password = hash_password(password) 

    #Store user data in the users.txt file
    with open("users.txt", "a") as f: 
       f.write(f"{username},{hashed_password},{role}\n") 
       print(f"User '{username}' registered successfully.")
    return True

def user_exists(username):
    #Check if a user exists in the user data file.
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username = line.split(",", 1)[0]
            if stored_username == username:
                return True
    return False

def login_user(username, password): 
       #Log in an existing user.
    with open("users.txt", "r") as f:
        for line in f.readlines(): 
            user, rest = line.strip().split(",", 1)
            # Get just the password hash part
            hash = rest.split(",")[0]  
            if (user == username):
                if verify_password(password, hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False
        print("Error:Username not found")
        return False

def validate_username(username):
    # Validate username criteria
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters."
    if not username.isalnum():
        return False, "Username must be alphanumeric."
    return True, ""


def validate_password(password):
    #Check password length
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if len(password) > 50:
        return False, "Password must be no more than 50 characters long."
    
    return True, ""

def check_password_strength(password):
    strength = 0
    upper_present = False
    char_present = False
    digit_present = False
    specialchar_present = False
    #Checking if password has more than 8 letters
    if len(password) >= 8:   
        strength=strength+1

    #Checking each character in password
    for char in password:
        #Checking if there is any uppercase letter in password      
        if char.isupper():    
            #Boolean value changes if condition met
            upper_present=True 
         #Checking if there is any lowercase letter in password
        elif char.islower():  
            char_present=True  
         #Checking if there is any number in password
        elif char.isdigit():  
            digit_present=True 
         #Calling a function to check for special character
        elif special_character(char): 
            specialchar_present=True 
    
    #Calculating strength level
    if upper_present:
        strength += 1
    if char_present:
        strength += 1
    if digit_present:
        strength += 1
    if specialchar_present:
        strength += 1

    #Display strength level
    if strength <= 3:
        print("Password is weak")
    elif strength == 4:
        print("Password is moderate")
    else:
        print("Password is strong")

def special_character(char):
   code = ord(char)   #code is the ASCII value(In denary) of char
   #Comparing code with ASCII values
   if (65 <= code <= 90) or (97 <= code <= 122) or (48 <= code <= 57): 
       #Returning false since char is not a special character 
       return False   
   else:
      #Returning true since char is a special character
      return True     

#Display menu function
def display_menu():
 """Displays the main menu options."""
 print("\n" + "="*50)
 print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
 print(" Secure Authentication System")
 print("="*50)
 print("\n[1] Register a new user")
 print("[2] Login")                            
 print("[3] Exit")                                  
 print("-"*50)

#Main program loop function
def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        #Calling display_menu function
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
                                                     
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                print("Re-enter")
                continue
            
            password = input("Enter a password: ").strip() 

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                print("Re-enter")
                continue
            
            #Confirming password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            else:
                check_password_strength(password)
           
            #Register the user
            register_user(username, password)
        elif choice == '2':
            #Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
           
            #Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard or main features.)")
                                                  
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

#Run the main program loop
if __name__ == "__main__":
    main()

