import unittest
from io import StringIO
from unittest.mock import patch

from data.models import Problem
from helpers import details_log, input_log, summary_log


def capture(func, *args):
    with patch("sys.stdout", new=StringIO()) as fake_output:
        func(*args)
        return fake_output.getvalue()


class TestInputLog(unittest.TestCase):
    def test_reports_problem_count_and_filename(self):
        output = capture(input_log, [1, 2, 3], "problems/exercises.txt")

        self.assertIn("contains 3 problems", output)
        self.assertIn("problems/exercises.txt", output)
        self.assertIn("3 exercises", output)

    def test_handles_empty_problem_list(self):
        output = capture(input_log, [], "problems/empty.txt")

        self.assertIn("contains 0 problems", output)


class TestDetailsLog(unittest.TestCase):
    def make_problem(self):
        return Problem(
            header="Problem 1",
            sequence_line="2, 4, 5, ?",
            options_line="A) 23 B) 24",
            sequence=[2, 4, 5],
            options=[("A", 23), ("B", 24)],
        )

    def test_prints_header_sequence_options_and_solution(self):
        output = capture(
            details_log, self.make_problem(), "A) 23", "Alternating operations"
        )

        self.assertIn("Problem 1", output)
        self.assertIn("2, 4, 5, ?", output)
        self.assertIn("Possible answers: A) 23 B) 24", output)
        self.assertIn("Correct solution: A) 23", output)
        self.assertIn("Pattern: Alternating operations", output)

    def test_prints_unrecognized_solution(self):
        output = capture(
            details_log,
            self.make_problem(),
            "Rule not recognized",
            "Rule not recognized",
        )

        self.assertIn("Correct solution: Rule not recognized", output)


class TestSummaryLog(unittest.TestCase):
    def test_summary_log_output(self):
        output = capture(summary_log, [1, 2, 3], 3)

        self.assertIn("Total problems processed: 3", output)
        self.assertIn("Successfully solved: 3 / 3", output)
        self.assertIn("Excellent!", output)

    def test_partial_success_omits_celebration(self):
        output = capture(summary_log, [1, 2, 3], 2)

        self.assertIn("Successfully solved: 2 / 3", output)
        self.assertNotIn("Excellent!", output)

    def test_empty_run_counts_as_fully_solved(self):
        output = capture(summary_log, [], 0)

        self.assertIn("Successfully solved: 0 / 0", output)
        self.assertIn("Excellent!", output)
