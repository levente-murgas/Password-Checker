from hstest import CheckResult, StageTest, dynamic_test, TestedProgram


class StageTest1(StageTest):
    @dynamic_test
    def initial_prompt_test(self):
        main = TestedProgram()
        output = main.start().lower().strip()
        if "enter your password" not in output:
            return CheckResult.wrong("Your program should ask for the user's password.")
        return CheckResult.correct()

    pwds = ["mypassword123", "youcantguessme", "123456", "qwerty", "qwertz"]

    @dynamic_test(data=pwds)
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


if __name__ == '__main__':
    StageTest1().run_tests()
