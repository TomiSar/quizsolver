import unittest
from parser import parse_file
from analyzer import analyze_and_predict

class TestE2E(unittest.TestCase):
    def test_known_sequences(self):
        test_cases = [
            ([2, 4, 5, 10, 11, 22], 23),
            ([3, 9, 8, 24, 23, 69], 68),
            ([1, 3, 6, 10, 15], 21),
            ([5, 10, 20, 40], 80),
            ([240, 120, 60, 30], 15),
        ]

        for sequence, expected in test_cases:
            result = analyze_and_predict(sequence)
            self.assertEqual(result.prediction, expected)


    def assert_dataset_is_fully_solved(self, filename):
        problems = parse_file(filename)

        solved = 0

        for problem in problems:
            prediction = analyze_and_predict(problem.sequence).prediction

            for _, value in problem.options:
                if value == prediction:
                    solved += 1
                    break

        self.assertEqual(solved, len(problems))

    def test_exercises_uno_dataset_is_fully_solved(self):
        self.assert_dataset_is_fully_solved("problems/exercises_uno.txt")

    def test_exercises_dos_dataset_is_fully_solved(self):
        self.assert_dataset_is_fully_solved("problems/exercises_dos.txt")
