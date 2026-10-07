from data.models import RuleResult
from rule_utils import (
    calc_delta_difference,
    detect_operation,
    apply_operation,
    format_operation,
    sequence_matches_pattern
)

# 1. Fibonacci / Lucas rule (n1 + n2 ... e.g., 5, 8, 13, 21 -> 21 + 13 = 34)
def fibonacci(sequence):
    if len(sequence) >= 3:
        is_fib = True
        for i in range(2, len(sequence)):
            if sequence[i] != sequence[i - 1] + sequence[i - 2]:
              is_fib = False
              break
        if is_fib:
            return RuleResult(prediction=sequence[-1] + sequence[-2], pattern="Fibonacci / Lucas sum rule (n1 + n2)")

# 2. alternating operations (e.g., *A and +B or *A and -B === (*3, -1 or *2, -10))
def alternating_operations(sequence):
    if len(sequence) < 4:
        return None

    for mode in ["sub", "div"]:
        operation1 = detect_operation(sequence[0], sequence[1], mode)
        operation2 = detect_operation(sequence[1], sequence[2], mode)

        if not sequence_matches_pattern(sequence, operation1, operation2):
            continue

        op1_type, op1_value = operation1
        op2_type, op2_value = operation2

        operation_type, operation_value = (
            operation1
            if (len(sequence) - 1) % 2 == 0
            else operation2
        )

        pattern = ("Alternating operations "
            f"({format_operation(op1_type, op1_value)}, "
            f"{format_operation(op2_type, op2_value)})")

        prediction = apply_operation(sequence[-1], operation_type, operation_value)
        return RuleResult(prediction=prediction, pattern=pattern)

# 3a. Uniformly changing or accelerating differences (e.g., -2, -4, -6, -8 or +1, +2, +3)
def accelerating_difference(sequence):
    diffs = calc_delta_difference(sequence)
    if len(diffs) >= 2:
        diff_of_diffs = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]
        if len(set(diff_of_diffs)) == 1:
            next_diff = diffs[-1] + diff_of_diffs[0]
            step = diff_of_diffs[0]
            rule = (
                f"Constant difference change ({diffs[0]:+})"
                if step == 0
                else f"Accelerating difference ({diffs[0]:+}, {diffs[1]:+}... step {step:+})"
            )
            return RuleResult(prediction=sequence[-1] + next_diff, pattern=rule)
    return None

# 3b. Exponentially changing difference / Doubling differences
def exponential_difference(sequence):
    diffs = calc_delta_difference(sequence)
    if len(diffs) >= 2:
        is_exp_diff = True
        for i in range(len(diffs) - 1):
            if diffs[i] == 0 or diffs[i + 1] / diffs[i] != 2:
                is_exp_diff = False
                break
        if is_exp_diff:
            return RuleResult(
                prediction=sequence[-1] + (diffs[-1] * 2),
                pattern=f"Exponentially doubling differences (+{diffs[0]}, +{diffs[1]}, +{diffs[2]}...)")

# 3c. Alternating sign accelerating difference growth (e.g., +5, -15, +25 -> next is -35)
# grow by a steady step value while changing positive/negative signs: +5, -15, +25 -> next -35
def alternating_sign_difference(sequence):
    diffs = calc_delta_difference(sequence)
    if len(diffs) >= 2:
        abs_diffs = [abs(d) for d in diffs]
        diff_of_abs = [abs_diffs[i + 1] - abs_diffs[i] for i in range(len(abs_diffs) - 1)]

        # Verify the absolute value of the differences scales up steadily
        if len(set(diff_of_abs)) == 1 and diff_of_abs[0] != 0:
            # Check if signs are strictly alternating between positive and negative
            is_alternating_sign = all(diffs[i] * diffs[i + 1] < 0 for i in range(len(diffs) - 1))

            if is_alternating_sign:
                next_abs_diff = abs_diffs[-1] + diff_of_abs[0]
                next_sign = -1 if diffs[-1] > 0 else 1
                next_diff = next_abs_diff * next_sign
                return RuleResult(
                    prediction=sequence[-1] + next_diff,
                    pattern=f"Alternating sign accelerating difference ({diffs[0]:+}, {diffs[1]:+}, {diffs[2]:+}...)",)

# 4. accelerating ratio / factorial (e.g., 1, 2, 6, 24, 120 -> *2, *3, *4, *5)
def ratio(sequence):
    ratios = []
    for i in range(len(sequence) - 1):
        # Enforce that sequence elements are positive to avoid false integer division drops
        if (sequence[i] > 0 and sequence[i + 1] > 0 and sequence[i + 1] % sequence[i] == 0):
            ratios.append(sequence[i + 1] // sequence[i])

    # Check if the ratios are consistent and if they form a pattern
    # Check that we have a valid ratio for every single step in a pure positive sequence
    if len(ratios) == len(sequence) - 1 and len(ratios) >= 2:
        if len(set(ratios)) == 1:
            return RuleResult(
                prediction=sequence[-1] * ratios[0],
                pattern=f"Constant geometric ratio (*{ratios[0]})")

        ratio_diffs = [ratios[i + 1] - ratios[i] for i in range(len(ratios) - 1)]
        if len(set(ratio_diffs)) == 1:
            next_ratio = ratios[-1] + ratio_diffs[0]
            return RuleResult(
                prediction=sequence[-1] * next_ratio,
                pattern="Accelerating ratio / Factorial sequential multiplication")

# 5. Alternating shift sequence (e.g., +1, -2, +3, -4 or +2, -1, +4, -3)
def alternating_shift(sequence):
    diffs = calc_delta_difference(sequence)
    if len(diffs) >= 4 and len(set(diffs[1::2])) == 1:
        even_diffs = diffs[0::2]
        even_shifts = [even_diffs[i + 1] - even_diffs[i] for i in range(len(even_diffs) - 1)]
        if len(set(even_shifts)) == 1:
            next_diff = (diffs[-2] + even_shifts[0] if len(diffs) % 2 == 0 else diffs[1])
            return RuleResult(
                prediction=sequence[-1] + next_diff,
                pattern=f"Alternating shift sequence ({diffs[0]:+}, {diffs[1]:+}, {diffs[2]:+}...)")

# 6. Linear equation rule (e.g., 6, 11, 21, 41, 81 -> *2 - 1)
def linear_equation(sequence):
  if len(sequence) >= 3:
    c_vals = [sequence[i + 1] - 2 * sequence[i] for i in range(len(sequence) - 1)]
    if len(set(c_vals)) == 1:
      return RuleResult(
          prediction=2 * sequence[-1] + c_vals[0],
          pattern=f"Linear equation rule (2 * x_prev {c_vals[0]:+})")
