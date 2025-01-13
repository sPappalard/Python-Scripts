from cryptography.fernet import Fernet # type: ignore
import hashlib
import base64
import os
import json

#to get the file path
def get_file_path(file_name):
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
        base_path = config.get("base_path", os.getcwd())  
    else:
        # ask to user a path
        base_path = input("Enter the directory to save your files (leave empty for default): ").strip()
        if not base_path:
            base_path = os.getcwd()  # current Directory as default 
        else:
            if not os.path.exists(base_path):
                os.makedirs(base_path)
        # Save the configuration
        with open(config_file, "w") as f:
            json.dump({"base_path": base_path}, f)

    return os.path.join(base_path, file_name)



#to generate a unique SALT
def generate_salt():
    return os.urandom(16)           #16 bytes of random SALT

#to derivate a KEY with PBKDF2
def generate_fernet_key (master_pwd, salt):             #the value salt is used to make the derive key unique
    key = hashlib.pbkdf2_hmac(
        'sha256',               #hash algotithm
        master_pwd.encode(),    #master_passw in bytes
        salt,                   #unique value
        100000                  #number of iterations to make the operation safer 
        )         
    return Fernet(base64.urlsafe_b64encode(key))

#to write a SALT in the file "master_salts.txt"
def save_salt(master_pwd, salt):        
    salts_file = get_file_path("master_salts.txt")              
    if not os.path.exists(salts_file):
        with open(salts_file, "w") as f:
            json.dump({}, f)

    with open(salts_file, "r") as f:
        salts = json.load(f)

    salts[master_pwd] = base64.urlsafe_b64encode(salt).decode()

    with open(salts_file, "w") as f:
        json.dump(salts, f)

#to read a SALT in the file "master_salts.txt"
def load_salt(master_pwd):
    salts_file = get_file_path("master_salts.txt")              
    if not os.path.exists(salts_file):
        return None

    with open(salts_file, "r") as f:
        salts = json.load(f)

    encoded_salt = salts.get(master_pwd)
    if encoded_salt:
        return base64.urlsafe_b64decode(encoded_salt)
    return None

#to view account|password
def view(fer):
    passwords_file = get_file_path("password.txt")
    if not os.path.exists(passwords_file):
        print("No passwords stored yet.")
        return
    
    with open(passwords_file, 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            try:
                user, encrypted_password, salt = data.split("|")
                fer = generate_fernet_key(master_pwd, base64.urlsafe_b64decode(salt))
                decrypted_password = fer.decrypt(encrypted_password.encode()).decode()
                print(f"User: {user} | Password: {decrypted_password}")
            except Exception:
                print(f"User: {user} | Password: PASSWORD ENCRYPTED FOR A DIFFERENT USER")

#to add account|password
def add(fer, salt):
    passwords_file = get_file_path("password.txt")
    name = input("Account Name: ").strip()
    if not name:
        print("Account name cannot be empty.")
        return
    
    pwd = input("Password: ").strip()
    if not pwd:
        print("Password cannot be empty.")
        return
   
    with open(passwords_file, 'a') as f:
        encrypted_password = fer.encrypt(pwd.encode()).decode()
        f.write(f"{name}|{encrypted_password}|{base64.urlsafe_b64encode(salt).decode()}\n")
    print(f"Password for {name} added successfully!")



#MAIN
fer=None
salt=None
master_pwd=None


while True:
    mode = input("Would you like to add a new password, view existing ones, or login with the master password (add/view/login), press q to quit?: ").lower()
    if mode == "q":
        break

    if mode == "login" or 'fer' == None:          
        master_pwd = input("Enter your master password (or set a new one): ")
        salt = load_salt(master_pwd)
        
        if salt is None:
            print("New master password detected. Generating a new salt.")
            salt = generate_salt()
            save_salt(master_pwd,salt)
        else:
            print ("Master password recognized.")

        fer = generate_fernet_key(master_pwd,salt)

    elif mode == "view":
        view(fer)

    elif mode == "add":
        if fer is None:
            print("No master password set. Please set or enter a master password first.")
        else:
            add(fer,salt)

    else:
        print("Invalid mode. Please enter a valid mode.")