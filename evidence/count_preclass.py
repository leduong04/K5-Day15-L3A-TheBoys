"""Reproduce aggregate pre-class practice-answer counts without printing learner IDs.

Run from the repository root:
    python evidence/count_preclass.py [path/to/preclass]

The default path points to the BTC dataset beside this repository. Raw source
files remain outside the repository and are never copied by this script.
"""

import csv
import os
import sys
from collections import Counter, defaultdict


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else os.path.join("..", "data", "preclass")
    answers = read_csv(os.path.join(base, "answers.csv"))
    practice = [row for row in answers if row.get("nguon") == "thuc_hanh"]
    graded = [row for row in practice if row.get("was_correct", "").lower() in {"true", "false"}]

    # Use the pseudonymous learner key only for grouping; never print it.
    by_learner_item = defaultdict(list)
    for row in practice:
        key = (row.get("hv", ""), row.get("lesson_id", ""), row.get("ref", ""))
        by_learner_item[key].append(row)

    repeated = []
    for (_, lesson, ref), rows in by_learner_item.items():
        if len(rows) >= 2:
            incorrect = sum(row.get("was_correct", "").lower() == "false" for row in rows)
            repeated.append((lesson, ref, len(rows), incorrect))

    incorrect_count = sum(row.get("was_correct", "").lower() == "false" for row in graded)
    repeated_with_incorrect = sum(item[3] > 0 for item in repeated)
    print(f"Thuc hanh answer rows with a True/False grade: {len(graded)}")
    print(f"Incorrect graded rows: {incorrect_count} ({incorrect_count / len(graded):.1%})")
    print(f"Distinct pseudonymous learner-item pairs: {len(by_learner_item)}")
    print(f"Pairs with 2+ answer rows: {len(repeated)} ({len(repeated) / len(by_learner_item):.1%})")
    print(f"Repeated pairs with at least one incorrect row: {repeated_with_incorrect}")

    # Aggregate by lesson and item so that no learner-level identifier appears.
    examples = Counter((lesson, ref, attempts, wrong) for lesson, ref, attempts, wrong in repeated)
    print("Representative repeated-answer item patterns (aggregated; no learner IDs):")
    for index, ((lesson, ref, attempts, wrong), pair_count) in enumerate(sorted(examples.items())[:5], 1):
        print(f"E{index:02d}: {lesson} / {ref}; {attempts} rows, {wrong} incorrect; {pair_count} learner-item pair(s)")


if __name__ == "__main__":
    main()
