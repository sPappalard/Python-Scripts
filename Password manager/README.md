# Password Manager with Encryption

This is a command-line password manager application that securely stores and manages account passwords. The passwords are encrypted using a master password and the Fernet encryption algorithm. The application allows users to store, view, and manage account credentials securely. It also provides the option to customize the storage directory.

## Features

- **Master Password Protection**: A master password is used to encrypt and decrypt passwords stored in the system.
- **Password Encryption**: Passwords are encrypted using the Fernet algorithm derived from the master password and a salt.
- **Account Management**: Users can add, view, and manage passwords for their accounts.
- **Custom Directory**: Users can specify a custom directory for storing password-related files. If no directory is provided, the current working directory is used.
- **Salt and Key Management**: The program generates a unique salt for each master password to ensure secure encryption.

## Files Used

- `password.txt`: Stores the account names, encrypted passwords, and salts used for encryption.
- `master_salts.txt`: Stores the salts for each master password to ensure unique encryption keys.
- `config.json`: Stores the user-specified base path for file storage.

The script supports the following operations:
- **Login**: Log in with an existing master password or create a new one.
- **Add Password**: Add a new account and its encrypted password to the system.
- **View Passwords**: View stored passwords by decrypting them using the master password.

## How to Use the Script

1. **Run the Script**: 
   - Run the script from the terminal or command prompt using Python.
   - The script will ask for the mode of operation: add a password, view existing passwords, or log in with the master password.

2. **Login or Set a New Master Password**:
   - If it's your first time using the script, you will be prompted to set a master password.
   - If you already have a master password, simply enter it to log in.
   - The master password is used to encrypt and decrypt stored passwords, so it must be kept secure.

3. **Add a New Password**:
   - After logging in, you can add new passwords.
   - The script will prompt you for an account name and password.
   - The password is encrypted using the master password, and the encrypted data is saved in the `password.txt` file.

4. **View Existing Passwords**:
   - You can view stored passwords by selecting the "view" option.
   - The script will decrypt the passwords using the master password and display them along with the corresponding account names.

5. **Custom Directory**:
   - You can specify a custom directory for storing password-related files during the initial setup.
   - If no directory is specified, the script will use the current working directory.

6. **Exit the Script**:
   - To exit the script, type `q` when prompted.

## Example Usage

When you first run the script, you will be prompted to set a master password. After that, you can add new passwords or view existing ones by following the on-screen prompts.

## Example Usage

When you first run the script, you will be prompted to set a master password. After that, you can add new passwords or view existing ones by following the on-screen prompts.

### Example Session (Windows Command Prompt)


#### First User (Master Password: `masterpassword1`)

```cmd
C:\> python password_manager.py
Would you like to add a new password, view existing ones, or login with the master password (add/view/login), press q to quit?: login
Enter your master password (or set a new one): masterpassword1
Master password recognized.

Would you like to add a new password, view existing ones, or login with the master password (add/view/login), press q to quit?: add
Account Name: Google
Password: googlepassword123
Password for Google added successfully!

Would you like to add a new password, view existing ones, or login with the master password (add/view/login), press q to quit?: view
User: Google | Password: googlepassword123

C:\>
```


#### Second User (Master Password: `masterpassword2`)
```cmd
C:\> python password_manager.py
Would you like to add a new password, view existing ones, or login with the master password (add/view/login), press q to quit?: login
Enter your master password (or set a new one): masterpassword2
Master password recognized.

Would you like to add a new password, view existing ones, or login with the master password (add/view/login), press q to quit?: add
Account Name: Facebook
Password: facebookpassword456
Password for Facebook added successfully!

Would you like to add a new password, view existing ones, or login with the master password (add/view/login), press q to quit?: view
User: Google | Password: PASSWORD CRIPTATA PER UN'ALTRA UTENZA
User: Facebook | Password: facebookpassword456
C:\>
```

#### Explanation:
The second user is logged in with masterpassword2.
The output then shows the passwords:
- Google: The password is encrypted for a different user (masterpassword1), so it cannot be decrypted and is shown as "PASSWORD CRIPTATA PER UN'ALTRA UTENZA."
- Facebook: This password is decrypted successfully as it was added by the second user with the same master password (masterpassword2).
