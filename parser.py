import re
from data.models import Problem

def parse_file(filename):
  with open(filename, "r", encoding="utf-8") as file:
      lines = [line.strip() for line in file if line.strip()]

  problems = []
  problem_indices = [
      idx
      for idx, line in enumerate(lines)
      if line.startswith("Problem")
  ]

  for start_idx in problem_indices:
      try:
          header = lines[start_idx]
          sequence_line = lines[start_idx + 1]
          options_line = lines[start_idx + 2]
      except IndexError:
          continue

      sequence = [
          int(n)
          for n in re.findall(r"-?\d+", sequence_line)
      ]

      options = [
          (letter, int(value))
          for letter, value in re.findall(
              r"([A-D])\)\s*(-?\d+)",
              options_line,
          )
      ]

      problems.append(
          Problem(
              header=header.replace('.',':'),
              sequence_line=sequence_line,
              options_line=options_line,
              sequence=sequence,
              options=options,
          )
      )

  return problems
