import unittest

from data.models import RuleResult
from analyzer import analyze_and_predict


class TestAnalyzer(unittest.TestCase):
    def test_unrecognized_sequence_returns_fallback(self):
        self.assertEqual(
            analyze_and_predict([1, 7, 2, 99]),
            RuleResult(prediction=None, pattern="Rule not recognized"),
        )

    def test_random_sequence_is_not_forced_into_a_rule(self):
        result = analyze_and_predict([3, 1, 4, 1, 5, 9])

        self.assertIsNone(result.prediction)
        self.assertEqual(result.pattern, "Rule not recognized")

    def test_first_matching_rule_wins(self):
        # [6, 11, 21, 41, 81] matches both the doubling-difference rule and the
        # linear-equation rule; the analyzer order decides which one is reported.
        result = analyze_and_predict([6, 11, 21, 41, 81])

        self.assertIn("doubling", result.pattern)

    def test_empty_sequence_is_handled(self):
        result = analyze_and_predict([])

        self.assertIsNone(result.prediction)
        self.assertEqual(result.pattern, "Rule not recognized")

    def test_single_element_sequence_is_handled(self):
        result = analyze_and_predict([42])

        self.assertIsNone(result.prediction)
        self.assertEqual(result.pattern, "Rule not recognized")
