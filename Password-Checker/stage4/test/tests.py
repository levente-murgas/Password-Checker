from hstest import CheckResult, StageTest, dynamic_test, TestedProgram
import hashlib


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

        warning = output.split("\n")[0]
        if expected_output != warning.strip():
            return CheckResult.wrong(f"The program did not warn about a short password.")

        return CheckResult.correct()

    @dynamic_test(data=valid_pwds)
    def test_api_request(self, x):
        main = TestedProgram()
        main.start().lower()

        output = main.execute(x).lower().strip()

        if "https://api.pwnedpasswords.com/range/" not in output:
            return CheckResult.wrong("The program did not display the API URL.")

        # Check if the URL contains the first 5 characters of the hashed password
        sha1_hash = hashlib.sha1(x.encode()).hexdigest().lower()
        if sha1_hash[:5] not in output:
            return CheckResult.wrong("The URL did not contain the correct first 5 characters of the hashed password.")

        return CheckResult.correct()


if __name__ == '__main__':
    StageTest4().run_tests()
