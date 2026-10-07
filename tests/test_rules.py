import unittest
from analyzer import analyze_and_predict
from rules import (
    calc_delta_difference,
    fibonacci,
    alternating_operations,
    accelerating_difference,
    exponential_difference,
    alternating_sign_difference,
    ratio,
    alternating_shift,
    linear_equation,
)

class TestRules(unittest.TestCase):
    def test_fibonacci(self):
        result = analyze_and_predict([2, 3, 5, 8, 13, 21])

        self.assertEqual(result.prediction, 34)
        self.assertIn("Fibonacci", result.pattern)


    def test_alternating_mul_add(self):
        result = analyze_and_predict([2, 4, 5, 10, 11, 22])

        self.assertEqual(result.prediction, 23)
        self.assertIn("Alternating operations", result.pattern)


    def test_alternating_mul_sub(self):
        result = analyze_and_predict([3, 9, 8, 24, 23, 69])

        self.assertEqual(result.prediction, 68)


    def test_accelerating_difference(self):
        result = analyze_and_predict([1, 3, 6, 10, 15])

        self.assertEqual(result.prediction, 21)


    def test_factorial(self):
        result = analyze_and_predict([1, 2, 6, 24, 120])

        self.assertEqual(result.prediction, 720)


    def test_linear_equation(self):
        result = analyze_and_predict([6, 11, 21, 41, 81])

        self.assertEqual(result.prediction, 161)


    def test_alternating_shift(self):
        result = analyze_and_predict([2, 3, 6, 7, 10, 11])

        self.assertEqual(result.prediction, 14)


    def test_division_rule(self):
        result = analyze_and_predict([240, 120, 60, 30])

        self.assertEqual(result.prediction, 15)


class TestCalcDiffForDelta(unittest.TestCase):
    def test_returns_consecutive_differences(self):
        self.assertEqual(calc_delta_difference([1, 3, 6]), [2, 3])

    def test_single_element_has_no_differences(self):
        self.assertEqual(calc_delta_difference([5]), [])


class TestFibonacci(unittest.TestCase):
    def test_classic_fibonacci(self):
        result = fibonacci([2, 3, 5, 8, 13, 21])

        self.assertEqual(result.prediction, 34)
        self.assertEqual(
            result.pattern,
            "Fibonacci / Lucas sum rule (n1 + n2)",
        )

    def test_lucas_style_sequence(self):
        result = fibonacci([2, 1, 3, 4, 7])
        self.assertEqual(result.prediction, 11)

    def test_too_short_sequence_returns_none(self):
        self.assertIsNone(fibonacci([1, 2]))

    def test_non_fibonacci_sequence_returns_none(self):
        self.assertIsNone(fibonacci([1, 2, 4]))


class TestAlternatingOperations(unittest.TestCase):
    def test_multiply_then_add(self):
        result = alternating_operations([2, 4, 5, 10, 11, 22])

        self.assertEqual(result.prediction, 23)
        self.assertEqual(
            result.pattern,
            "Alternating operations (*2, +1)",
        )

    def test_multiply_then_subtract(self):
        result = alternating_operations([3, 9, 8, 24, 23, 69])
        self.assertEqual(result.prediction, 68)

    def test_explicit_minus_two_tweak(self):
        # Exercises the hard-coded "drop by exactly 2" branch in get_op
        result = alternating_operations([2, 6, 4, 12, 10, 30])

        self.assertEqual(result.prediction, 28)
        self.assertEqual(
            result.pattern,
            "Alternating operations (*3, -2)",
        )

    def test_division_mode(self):
        result = alternating_operations([240, 120, 60, 30])

        self.assertEqual(result.prediction, 15)
        self.assertEqual(
            result.pattern,
            "Alternating operations (/2, /2)",
        )

    def test_too_short_sequence_returns_none(self):
        self.assertIsNone(alternating_operations([1, 2, 3]))

    def test_no_alternating_pattern_returns_none(self):
        self.assertIsNone(alternating_operations([1, 5, 2, 9, 100]))


class TestAcceleratingDifference(unittest.TestCase):
    def test_constant_difference(self):
        result = accelerating_difference([2, 4, 6, 8])

        self.assertEqual(result.prediction, 10)
        self.assertEqual(
            result.pattern,
            "Constant difference change (+2)",
        )

    def test_accelerating_difference(self):
        result = accelerating_difference([1, 3, 6, 10, 15])
        self.assertEqual(result.prediction, 21)
        self.assertIn("Accelerating difference", result.pattern)

    def test_too_short_sequence_returns_none(self):
        self.assertIsNone(accelerating_difference([5, 7]))

    def test_irregular_differences_return_none(self):
        self.assertIsNone(accelerating_difference([1, 2, 10, 11]))


class TestExponentialDifference(unittest.TestCase):
    def test_doubling_differences(self):
        result = exponential_difference([6, 11, 21, 41, 81])
        self.assertEqual(result.prediction, 161)
        self.assertIn("doubling", result.pattern)

    def test_zero_difference_returns_none(self):
        self.assertIsNone(exponential_difference([5, 5, 5]))

    def test_non_doubling_difference_returns_none(self):
        self.assertIsNone(exponential_difference([1, 2, 5]))

    def test_too_short_sequence_returns_none(self):
        self.assertIsNone(exponential_difference([1, 2]))


class TestAlternatingSignDifference(unittest.TestCase):
    def test_negative_last_difference_flips_positive(self):
        result = alternating_sign_difference([10, 15, 0, 25, -10])

        self.assertEqual(result.prediction, 35)
        self.assertEqual(
            result.pattern,
            "Alternating sign accelerating difference (+5, -15, +25...)",
        )

    def test_positive_last_difference_flips_negative(self):
        result = alternating_sign_difference([10, 15, 0, 25])
        self.assertEqual(result.prediction, -10)

    def test_constant_absolute_difference_returns_none(self):
        self.assertIsNone(alternating_sign_difference([1, 2, 1, 2]))

    def test_same_sign_differences_return_none(self):
        self.assertIsNone(alternating_sign_difference([1, 2, 4, 7]))

    def test_too_short_sequence_returns_none(self):
        self.assertIsNone(alternating_sign_difference([1, 2]))


class TestRatio(unittest.TestCase):
    def test_constant_geometric_ratio(self):
        result = ratio([5, 10, 20, 40])

        self.assertEqual(result.prediction, 80)
        self.assertEqual(
            result.pattern,
            "Constant geometric ratio (*2)",
        )

    def test_factorial_style_ratio(self):
        result = ratio([1, 2, 6, 24, 120])
        self.assertEqual(result.prediction, 720)
        self.assertIn("Accelerating ratio", result.pattern)

    def test_negative_values_return_none(self):
        self.assertIsNone(ratio([-2, -4, -8]))

    def test_non_divisible_step_returns_none(self):
        self.assertIsNone(ratio([1, 2, 5, 11]))

    def test_irregular_ratio_growth_returns_none(self):
        self.assertIsNone(ratio([1, 2, 6, 12]))

    def test_single_ratio_returns_none(self):
        self.assertIsNone(ratio([2, 4]))


class TestAlternatingShift(unittest.TestCase):
    def test_odd_number_of_differences(self):
        result = alternating_shift([2, 3, 6, 7, 10, 11])

        self.assertEqual(result.prediction, 14)
        self.assertEqual(
            result.pattern,
            "Alternating shift sequence (+1, +3, +1...)",
        )

    def test_even_number_of_differences(self):
        result = alternating_shift([2, 3, 6, 7, 10, 11, 14])
        self.assertEqual(result.prediction, 15)

    def test_too_few_differences_return_none(self):
        self.assertIsNone(alternating_shift([1, 2, 3, 4]))

    def test_inconsistent_odd_differences_return_none(self):
        self.assertIsNone(alternating_shift([1, 2, 5, 6, 20, 21]))

    def test_inconsistent_even_shifts_return_none(self):
        self.assertIsNone(alternating_shift([0, 1, 6, 8, 13, 23]))


class TestLinearEquation(unittest.TestCase):
    def test_linear_equation_rule(self):
        result = linear_equation([6, 11, 21, 41, 81])

        self.assertEqual(result.prediction, 161)
        self.assertEqual(
            result.pattern,
            "Linear equation rule (2 * x_prev -1)",
        )

    def test_too_short_sequence_returns_none(self):
        self.assertIsNone(linear_equation([1, 2]))

    def test_non_linear_sequence_returns_none(self):
        self.assertIsNone(linear_equation([1, 2, 3]))

