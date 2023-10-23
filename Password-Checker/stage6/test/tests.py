from hstest import CheckResult, StageTest, dynamic_test, TestedProgram
import hashlib
import requests


class StageTest6(StageTest):
    valid_pwds = ["mypassword123", "youcantguessme", "abcdefgh", "validpwd", "adefkfnreogbroegbroegb", "wfwbfodbuoadbcuodavc"]
    pwned_pwds = ["12345678", "password", "mypassword"]
    exit_cmd = ["exit"]
    short_pwds = ["123456", "qwerty", "qwertz", "notlong", "short"]

    @dynamic_test
    def test_prompt_and_hash(self):
        main = TestedProgram()
        output = main.start().lower()
        if "enter your password" not in output:
            return CheckResult.wrong("The program did not prompt for the password.")
        return CheckResult.correct()

    @dynamic_test
    def test_exit_prompt(self):
        main = TestedProgram()
        output = main.start().strip()

        expected_output = "Enter your password (or 'exit' to quit):"

        if expected_output != output:
            return CheckResult.wrong(f"The program did not provide an option for the user to exit the program at any "
                                     "time.\n"
                                     f"Your output was: {output}")
        return CheckResult.correct()

    @dynamic_test(data=short_pwds)
    def short_pwd_length_check(self, x):
        main = TestedProgram()
        main.start().lower()
        output = main.execute(x)

        expected_output = "Your password is too short. Please enter a password of at least 8 characters."

        warning = output.split("\n")[0]
        if expected_output != warning.strip():
            return CheckResult.wrong(f"The program did not warn about a short password.")

        return CheckResult.correct()

    @dynamic_test
    def test_continuous_prompt(self):
        main = TestedProgram()
        output = main.start().lower()

        if "enter your password" not in output:
            return CheckResult.wrong("The program did not prompt for the password initially.")

        output = main.execute("test_password").lower()
        if "enter your password" not in output:
            return CheckResult.wrong("The program did not prompt for the password again.")

        return CheckResult.correct()

    @dynamic_test(data=valid_pwds)
    def hash_output_test(self, x):
        main = TestedProgram()
        main.start("--show-hash")

        output = main.execute(x).strip()

        expected_hash = hashlib.sha1(x.encode()).hexdigest()

        expected_output = "Your hashed password is: " + expected_hash

        display_hash_output = output.split("\n")[0].strip()

        if expected_output != display_hash_output:
            return CheckResult.wrong("The program should output the hashed password.\n" +
                                     "Expected: \"" + expected_output + "\".\n" +
                                     "Got: \"" + display_hash_output + "\". ")
        return CheckResult.correct()

    @dynamic_test(data=valid_pwds)
    def test_output_hash(self, x):
        main = TestedProgram()
        main.start().lower()
        output = main.execute(x).lower()

        sha1_hash = hashlib.sha1(x.encode()).hexdigest().lower()

        if sha1_hash in output:
            return CheckResult.wrong(f"The program should NOT display the hashed password, " +
                                     "if --show-hash was not given.")

        return CheckResult.correct()

    @dynamic_test(data=pwned_pwds)
    def test_pwned_pwd(self, x):
        main = TestedProgram()
        main.start().lower()
        output = main.execute(x)
        output = output.split("Checking...")[1].strip()
        output = output.split("Enter your password (or 'exit' to quit):")[0].strip()

        sha1_hash = hashlib.sha1(x.encode()).hexdigest().lower()

        response = requests.get("https://api.pwnedpasswords.com/range/" + sha1_hash[0:5],
                                headers={"Add-Padding": "true"})
        results = response.text.split("\n")

        found = False
        final_count = 0
        for result in results:
            hash_suffix, count = result.lower().strip().split(":")
            if hash_suffix == sha1_hash[5:]:
                found = True
                final_count = count
                break

        if found:
            expected_output = f"Your password has been pwned! The password \"{x}\" appears {final_count} times in data breaches."
            if expected_output != output:
                return CheckResult.wrong(
                    "This password has been pwned " + final_count + " times, but your output was: \n" + output)
            else:
                return CheckResult.correct()
        else:
            expected_output = "Good news! Your password hasn't been pwned."
            if expected_output != output:
                return CheckResult.wrong(
                    "This password hasn't been pwned, but your output was: \n" + output)
            else:
                return CheckResult.correct()

    @dynamic_test(data=exit_cmd)
    def test_exit_option(self, x):
        main = TestedProgram()
        main.start()
        output = main.execute(x).lower()
        if "goodbye" not in output:
            return CheckResult.wrong("The program did not exit when the 'exit' command was entered.")
        return CheckResult.correct()

    @dynamic_test(data=valid_pwds)
    def test_show_hash_argument(self, x):
        main = TestedProgram()
        main.start("--show-hash")
        output = main.execute(x).lower()
        sha1_hash = hashlib.sha1(x.encode()).hexdigest().lower()

        if sha1_hash not in output:
            return CheckResult.wrong("The hashed password should be displayed when --show-hash is used.")

        return CheckResult.correct()


if __name__ == '__main__':
    StageTest6().run_tests()
