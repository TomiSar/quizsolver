from data.models import RuleResult
from rules import (
    fibonacci,
    alternating_operations,
    accelerating_difference,
    exponential_difference,
    alternating_sign_difference,
    ratio,
    alternating_shift,
    linear_equation,
)

RULES = [
    fibonacci,
    alternating_operations,
    accelerating_difference,
    exponential_difference,
    alternating_sign_difference,
    ratio,
    alternating_shift,
    linear_equation,
]

def analyze_and_predict(sequence):
    for rule in RULES:
        result = rule(sequence)

        if result is not None:
            return result

    return RuleResult(prediction=None, pattern="Rule not recognized")
