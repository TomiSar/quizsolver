import os
import tempfile
import unittest

from parser import parse_file

class TestParser(unittest.TestCase):
    def test_exercises_file_contains_20_problems(self):
        problems = parse_file("problems/exercises_uno.txt")
        self.assertEqual(len(problems), 20)

    def test_first_problem_loaded_correctly(self):
        problems = parse_file("problems/exercises_uno.txt")

        problem = problems[0]

        self.assertEqual(problem.header, "Problem 1:")
        self.assertEqual(problem.sequence, [2, 4, 5, 10, 11, 22])

    def test_options_parsed_correctly(self):
        problems = parse_file("problems/exercises_uno.txt")
        problem = problems[0]
        self.assertEqual(problem.options, [
            ("A", 23),
            ("B", 24),
            ("C", 44),
            ("D", 21),
        ])


class TestParserEdgeCases(unittest.TestCase):
    def write_file(self, content):
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".txt", delete=False, encoding="utf-8"
        )
        with handle as file:
            file.write(content)
        self.addCleanup(os.unlink, handle.name)
        return handle.name

    def test_truncated_trailing_problem_is_skipped(self):
        path = self.write_file(
            "Problem 1.\n"
            "1, 2, 3, ?\n"
            "A) 4 B) 5 C) 6 D) 7\n"
            "Problem 2.\n"
            "2, 4, 6, ?\n"
        )

        problems = parse_file(path)

        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0].header, "Problem 1:")

    def test_blank_lines_are_ignored(self):
        path = self.write_file(
            "\n\nProblem 1.\n\n   \n"
            "1, 2, 3, ?\n"
            "A) 4 B) 5 C) 6 D) 7\n"
        )

        problems = parse_file(path)

        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0].sequence, [1, 2, 3])

    def test_file_without_problems_returns_empty_list(self):
        path = self.write_file("just some notes\nand more notes\n")

        self.assertEqual(parse_file(path), [])

    def test_negative_numbers_are_parsed(self):
        path = self.write_file(
            "Problem 1.\n"
            "-5, -10, -15, ?\n"
            "A) -20 B) -25 C) 20 D) 0\n"
        )

        problem = parse_file(path)[0]

        self.assertEqual(problem.sequence, [-5, -10, -15])
        self.assertEqual(
            problem.options,
            [("A", -20), ("B", -25), ("C", 20), ("D", 0)],
        )

    def test_header_dots_are_replaced_with_colons(self):
        path = self.write_file(
            "Problem 7.\n"
            "1, 2, 3, ?\n"
            "A) 4 B) 5 C) 6 D) 7\n"
        )

        self.assertEqual(parse_file(path)[0].header, "Problem 7:")

    def test_raw_lines_are_preserved(self):
        path = self.write_file(
            "Problem 1.\n"
            "1, 2, 3, ?\n"
            "A) 4 B) 5 C) 6 D) 7\n"
        )

        problem = parse_file(path)[0]

        self.assertEqual(problem.sequence_line, "1, 2, 3, ?")
        self.assertEqual(problem.options_line, "A) 4 B) 5 C) 6 D) 7")
