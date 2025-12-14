 #Represents a user in the Multi-Domain Intelligence Platform.
def __init__(self, username, password_hash, role):
    # Store the user's username, hashed password, and role
    self.__username = username
    self.__password_hash = password_hash
    self.__role = role

def get_username(self):
    return self.__username

def verify_password(self, plain_password: str, hasher):
    # Check if the given password matches the stored hashed password
    return hasher.check_password(plain_password, self.__password_hash)

def get_role(self):
    return self.__role

def __str__(self):
    # Return a readable string for this user
    return f"User({self.__username}, role={self.__role})"