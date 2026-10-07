def input_log(problems, filename):
    print("\n|------------------------------------------------------------|")
    print(f"|------------ Quiz solver contains {len(problems)} problems --------------|")
    print(f"|- Input file: {filename} with {len(problems)} exercises -|")
    print("|------------------------------------------------------------|\n")

def details_log(problem, solution, pattern):
    print(f"|------------------- {problem.header.replace(':', '')} -------------------|")
    print(f"{problem.header} {problem.sequence_line}")
    print(f"Possible answers: {problem.options_line}")
    print(f"Correct solution: {solution}")
    print(f"Pattern: {pattern}\n")

def summary_log(problems, solved_successfully):
    print("|------------------- Summary -------------------|")
    print(f"Total problems processed: {len(problems)}")
    print(f"Successfully solved: {solved_successfully} / {len(problems)}")
    if solved_successfully == len(problems):
        print("🎉 Excellent! All rules recognized and verified.")
    print("|-----------------------------------------------|")
