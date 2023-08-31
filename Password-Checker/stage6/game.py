import hashlib
import requests
import argparse


def check_password(password, show_hash):
    encoded = hashlib.sha1(password.encode())
    if show_hash:
        print("Your hashed password is: " + encoded.hexdigest())
    print("Checking...")
    response = requests.get("https://api.pwnedpasswords.com/range/" + encoded.hexdigest()[0:5])
    results = response.text.split("\n")
    for result in results:
        hash_suffix, count = result.lower().strip().split(":")
        if hash_suffix == encoded.hexdigest()[5:]:
            print(f"Your password has been pwned! The password \"{password}\" appears {count} times in data breaches.")
            return
    print("Good news! Your password hasn't been pwned.")


def get_password():
    while True:
        user_input = input("Enter your password (or 'exit' to quit): ")
        if user_input == "exit":
            print("Goodbye!")
            exit()
        elif len(user_input) < 8:
            print("Your password is too short. Please enter a password of at least 8 characters.")
        else:
            return user_input


def main():
    parser = argparse.ArgumentParser(description='Check if a password has been pwned.')
    parser.add_argument('--show-hash', action='store_true', help='Show the full hashed password in the output')
    args = parser.parse_args()
    while True:
        password = get_password()
        check_password(password, args.show_hash)


if __name__ == '__main__':
    main()
