from hstest import CheckResult, StageTest, dynamic_test, TestedProgram
import hashlib, requests


class StageTest4(StageTest):

    @dynamic_test
    def initial_prompt_test(self):
        main = TestedProgram()
        output = main.start().lower().strip()
        if "enter your password" not in output:
            return CheckResult.wrong("Your program should ask for the user's password.")
        return CheckResult.correct()

    valid_pwds = ["mypassword123", "youcantguessme", "abcdefgh", "validpwd"]
    short_pwds = ["123456", "qwerty", "qwertz", "notlong", "short"]

    @dynamic_test(data=short_pwds)
    def short_pwd_length_check(self, x):
        main = TestedProgram()
        main.start().lower()
        output = main.execute(x)

        expected_output = "Your password is too short. Please enter a password of at least 8 characters."

        warning = output.split("\n")[0].strip()
        if expected_output != warning:
            return CheckResult.wrong(f"The program did not warn about a short password.")

        return CheckResult.correct()

    @dynamic_test(data=valid_pwds)
    def hash_output_test(self, x):
        main = TestedProgram()
        main.start().lower()
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
    def test_api_request(self, x):
        main = TestedProgram()
        main.start().lower()

        output = main.execute(x).strip()
        output = output.split("Checking...")[1].strip()

        sha1_hash = hashlib.sha1(x.encode()).hexdigest().lower()

        response = requests.get("https://api.pwnedpasswords.com/range/" + sha1_hash[0:5])
        lines = response.text.splitlines()

        expected_output = "The request returned " + str(len(lines)) + " possibly matching passwords."
        # Add a check to verify that some fetched data is printed
        if expected_output != output:
            return CheckResult.wrong(f"The number of possible matches is not equal to the expected number of matches.\n"
                                     f"Your output: {output}\n"
                                     f"Expected: {expected_output}")

        return CheckResult.correct()


if __name__ == '__main__':
    StageTest4().run_tests()
