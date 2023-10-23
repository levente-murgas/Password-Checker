from hstest import CheckResult, StageTest, dynamic_test, TestedProgram
import random


def generate_data():
    data_arr = []
    for i in range(5):
        number_of_short_pwds = random.randint(1, 10)
        data = [f"short{i}" for i in range(number_of_short_pwds)]
        data.append("validpassword")
        data_arr.append(data)
    return data_arr


class StageTest2(StageTest):
    @dynamic_test
    def initial_prompt_test(self):
        main = TestedProgram()
        output = main.start().lower().strip()
        if "enter your password" not in output:
            return CheckResult.wrong("Your program should ask for the user's password.")
        return CheckResult.correct()

    valid_pwds = ["mypassword123", "youcantguessme", "abcdefgh", "validpwd"]
    short_pwds = ["123456", "qwerty", "qwertz", "notlong", "short"]


    @dynamic_test(data=valid_pwds)
    def input_test(self, x):
        main = TestedProgram()
        output = main.start().lower()
        output2 = main.execute(x)

        expected_output = "You entered: " + x  # Replace with the exact string your program should output

        if not output2:
            return CheckResult.wrong("Your program's output is empty. It should display the entered password.")

        if expected_output != output2.strip():
            return CheckResult.wrong(
                f"Your program should display '{expected_output}', but your output is: '{output2}'")

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

    @dynamic_test(data=valid_pwds)
    def valid_pwd_length_check(self, x):
        main = TestedProgram()
        main.start().lower()
        output = main.execute(x)

        if x not in output:
            return CheckResult.wrong("The program did not confirm the valid password.")

        return CheckResult.correct()

    @dynamic_test(data=generate_data())
    def prompt_again_check_2(self, *args):
        main = TestedProgram()
        main.start().lower()

        for arg in args[:-1]:  # Passing all but the last password
            main.execute(arg)
            if main.is_finished():
                return CheckResult.wrong("The program finished without asking for a password again after a short one.")

        # Now pass the valid password
        output = main.execute(args[-1]).strip()

        expected_output = "You entered: " + args[-1]

        if expected_output != output:
            return CheckResult.wrong(f"The program did not confirm that a valid password was entered.\n"
                                     f"Your output was: {output}")

        return CheckResult.correct()


if __name__ == '__main__':
    StageTest2().run_tests()
