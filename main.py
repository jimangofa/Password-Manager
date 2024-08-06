import random
import string
import secrets
import json
from cryptography.fernet import Fernet

def generate_password(length, uppercase, lowercase, numbers, special_chars):
    """Generates a random password based on given criteria."""
    characters = ""
    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if numbers:
        characters += string.digits
    if special_chars:
        characters += string.punctuation

    if not characters:
        raise ValueError("No character types selected for password generation.")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_key():
    """Generates a random key for Fernet encryption."""
    key = Fernet.generate_key()
    return Fernet(key)

def encrypt_password(password, fernet):
    """Encrypts the password using the provided Fernet key."""
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, fernet):
    """Decrypts the password using the provided Fernet key."""
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def store_password(username, password, fernet):
    """Stores the encrypted password in a JSON file."""
    encrypted_password = encrypt_password(password, fernet)
    data = {username: encrypted_password.decode()}
    try:
        with open('passwords.json', 'r+') as f:
            try:
                passwords = json.load(f)
            except json.JSONDecodeError:
                passwords = {}
            passwords.update(data)
            f.seek(0)
            json.dump(passwords, f, indent=4)
    except FileNotFoundError:
        with open('passwords.json', 'w') as f:
            json.dump(data, f, indent=4)

def retrieve_password(username, fernet):
    """Retrieves and decrypts the password."""
    try:
        with open('passwords.json', 'r') as f:
            passwords = json.load(f)
            encrypted_password = passwords.get(username)
            if encrypted_password:
                return decrypt_password(encrypted_password.encode(), fernet)
            else:
                return None
    except FileNotFoundError:
        return None

def get_integer_input(prompt):
    """Gets integer input from the user, with error handling."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    fernet = generate_key()
    username = input("Enter a username: ")
    length = get_integer_input("Enter the desired length for the password: ")
    uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
    numbers = input("Include numbers? (y/n): ").lower() == 'y'
    special_chars = input("Include special characters? (y/n): ").lower() == 'y'

    password = generate_password(length, uppercase, lowercase, numbers, special_chars)
    print(f"Generated password for {username}: {password}")

    store_password(username, password, fernet)
    retrieved_password = retrieve_password(username, fernet)
    print(f"Retrieved password for {username}: {retrieved_password}")

if __name__ == "__main__":
    main()
