# 🧠 IQ Quiz Sequence Solver & Analyzer

A modular, extensible **Python 3 CLI engine** designed to systematically parse, analyze, and automatically solve mathematical number sequence problems commonly found in intelligence and logic tests.

The core design utilizes an decoupled pipe pattern architecture. It evaluates incoming raw numerical arrays through a matrix of independent pattern-matching rule engines, scores options dynamically, and verifies solutions with 100% test pipeline stability.

---

## 🚀 Key Features

- **Dynamic Sequence Pattern Recognition**: Detects everything from basic arithmetic steps to advanced progressive exponential anomalies and alternating sign leaps.
- **Smart Verification & Option Scoring**: Parses the full problem string block (`Problem`, `Sequence`, `Options`) and performs iterative validation to map the calculated logic strictly against multiple-choice choices (`A, B, C, D`).
- **Decoupled Architecture**: Modular rules engine separating data serialization, parser tokenization, analytical orchestration, and output pipelines.
- **Comprehensive Test Suite & Coverage**: Packaged with over 70 automated integration and unit test assets maintaining a zero-regression lifecycle.

---

## 🧮 Supported Mathematical Patterns (These patters can be expanded)

The solver automatically recognizes and calculates the next item in a sequence based on these independent rulesets:

1. **Fibonacci / Lucas progressions**: Each term is evaluated as the pure sum of its trailing neighbors (\(x*n = x*{n-1} + x\_{n-2}\)).
2. **Alternating Multi-Track Operations**: Handles multi-layered interleaved cycles over alternating parity indices (e.g., `*3` then `-1`, `*4` then `-2`, or `/2` then `+1`).
3. **Difference Matrix Analysis**:
   - **Constant Delta steps**: Simple linear increments or decrements.
   - **Accelerating Delta steps**: Sequences where the change rate itself scales steadily (e.g., -2, -4, -6, -8).
   - **Exponential / Doubling Differences**: Compounding steps where delta changes exponentially.
   - **Alternating Sign Acceleration Leaps**: Complex shifting sign behaviors (e.g., +5, -15, +25 → -35).
4. **Factorial & Geometric Ratios**: Detects proportional growth and sequential factorial multiplication products.
5. **Progressive Shift Alternating Windows**: Advanced tracking where odd gaps remain fixed while even leaps scale linearly.
6. **Linear Recurrence Equations**: Solves recurrence relation limits mapping the linear form \(x*n = 2 \cdot x*{n-1} + C\).

---

## 📁 System Architecture & Directory Tree

```text
exercises/
│
├── exercise_solver.py      # Entry point / Main runtime executor
├── parser.py               # File tokenizer and token object mapper
├── analyzer.py             # Pattern recognition pipeline orchestrator
├── rules.py                # Central evaluation dictionary mapping for rules matrix
├── rule_utils.py           # Reusable mathematical and operational functions
├── helpers.py              # Log formatters (Input, Details, Summary pipelines)
│
├── data/
│   └── models.py           # Dataclass wrappers (Problem, RuleResult tokens)
│
├── tests/                  # 70+ Automated unit & E2E verification files
│   ├── test_analyzer.py
│   ├── test_e2e.py
│   ├── test_helpers.py
│   ├── test_parser.py
│   └── test_rules.py
│
├── problems/               # Local question database source sheets
│   ├── exercises_uno.txt
│   └── exercises_dos.txt
└── scripts/                # Automated environment toolchain scripts
    ├── clean-results.sh
    └── run-tests.sh
```

---

## 🛠️ Installation & Setup

1. Clone this repository locally into your environment:

   ```bash
   git clone https://github.com
   cd exercises
   ```

2. If you are developing locally and want to keep your global environment pristine, initialize a sandbox virtual environment:

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows Git Bash: source venv/Scripts/activate
   ```

3. Install testing dependencies to unlock coverage reporting:
   ```bash
   pip install coverage
   ```

---

## 📱 Running the Engine

To scan the text question source files, run the analyzer through the master executor script:

```bash
python exercise_solver.py
```

### Expected Console Output Sample:

```text

|------------------------------------------------------------|
|------------ Quiz solver contains 20 problems --------------|
|- Input file: problems/exercises_uno.txt with 20 exercises -|
|------------------------------------------------------------|

|------------------- Problem 1 -------------------|
Problem 1: 2, 4, 5, 10, 11, 22, ?
Possible answers: A) 23 B) 24 C) 44 D) 21
Correct solution: A) 23
Pattern: Alternating operations (*2, +1)

...

|------------------- Summary -------------------|
Total problems processed: 20
Successfully solved: 20 / 20
🎉 Excellent! All rules recognized and verified.

|-----------------------------------------------|
```

---

## 🧪 Automated Testing & Coverage

The repository enforces complete regression protection using automated tests and a coverage compiler toolchain.

### Clear transient results:

```bash
./scripts/clean-results.sh
```

### Run the test suite and compile HTML coverage maps:

```bash
./scripts/run-tests.sh
```

The script runs all unit assets, outputs terminal stats, and generates a graphic breakdown profile available locally under `htmlcov/index.html`.
