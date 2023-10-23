import hashlib
import requests

password = ""
while len(password) < 8:
    print("Enter your password:")
    password = input()
    if len(password) < 8:
        print("Your password is too short. Please enter a password of at least 8 characters.")
    encoded = hashlib.sha1(password.encode())
print("Your hashed password is: " + encoded.hexdigest())
print("Checking...")
response = requests.get("https://api.pwnedpasswords.com/range/" + encoded.hexdigest()[0:5])
lines = response.text.splitlines()
print("The request returned " + str(len(lines)) + " possibly matching passwords.")