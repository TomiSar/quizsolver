from parser import parse_file
from data.models import Problem
from helpers import input_log, details_log, summary_log
from analyzer import analyze_and_predict

def solve_quiz_with_file(filename: str):
    problems: list[Problem] = parse_file(filename)
    input_log(problems, filename)

    solved_successfully = 0
    for problem in problems:
        result = analyze_and_predict(problem.sequence)

        if result:
            predicted_value = result.prediction
            pattern = result.pattern
        else:
            predicted_value = None
            pattern = "Rule not recognized"

        solution = "Rule not recognized"

        for letter, value in problem.options:
            if predicted_value == value:
                solution = f"{letter}) {value}"
                solved_successfully += 1
                break

        # Log the details of the problem, the solution, and the pattern detected
        details_log(problem, solution, pattern)
    # Summarize the results after all problems have been processed
    summary_log(problems, solved_successfully)

solve_quiz_with_file('problems/exercises_uno.txt')
solve_quiz_with_file('problems/exercises_dos.txt')
