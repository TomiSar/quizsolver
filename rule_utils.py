# Pre-calculate simple differences for delta analysis
def calc_delta_difference(sequence):
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]

# Detect the operation between two consecutive numbers based on the given mode
def detect_operation(previous, current, mode):
    if current < previous and (previous - current) == 2:
        return ("add", current - previous)

    if mode == "div" and current != 0 and previous % current == 0:
        return ("div", previous // current)

    if previous != 0 and current % previous == 0:
        return ("mul", current // previous)

    return ("add", current - previous)

def apply_operation(value, operation_type, operation_value):
    if operation_type == "mul":
        return value * operation_value

    if operation_type == "div":
        return value // operation_value

    return value + operation_value

def format_operation(operation_type, operation_value):
    if operation_type == "mul":
        return f"*{operation_value}"

    if operation_type == "div":
        return f"/{operation_value}"

    return f"{operation_value:+}"

def sequence_matches_pattern(sequence, op1, op2):
    op1_type, op1_value = op1
    op2_type, op2_value = op2

    for i in range(len(sequence) - 1):
        operation_type, operation_value = (
            (op1_type, op1_value)
            if i % 2 == 0
            else (op2_type, op2_value)
        )

        expected = apply_operation(
            sequence[i],
            operation_type,
            operation_value,
        )

        if sequence[i + 1] != expected:
            return False

    return True
