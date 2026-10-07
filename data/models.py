from dataclasses import dataclass


@dataclass
class Problem:
    header: str
    sequence_line: str
    options_line: str
    sequence: list[int]
    options: list[tuple[str, int]]

@dataclass
class RuleResult:
    prediction: int
    pattern: str

@dataclass
class SequenceAnalysis:
    sequence: list[int]
    diffs: list[int]
