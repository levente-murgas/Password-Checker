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
response = requests.get("https://api.pwnedpasswords.com/range/" + encoded.hexdigest()[0:5], headers={"Add-Padding": "true"})
results = response.text.split("\n")
found = False
for result in results:
    hash_suffix, count = result.lower().strip().split(":")
    if hash_suffix == encoded.hexdigest()[5:]:
        found = True
        print(f"Your password has been pwned! The password \"{password}\" appears {count} times in data breaches.")
        exit()
if not found:
    print("Good news! Your password hasn't been pwned.")
exit()
