"""Offline consistency checks for the published summary CSV artifacts.

These tests verify internal consistency, not the original Hive queries or
prospective model quality. No AWS services or third-party packages are used.
"""

import ast
import csv
import unittest
from decimal import Decimal
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def read_rows(filename):
    with (DATA / filename).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


class PublishedAggregateChecks(unittest.TestCase):
    def test_airport_and_carrier_rankings(self):
        for filename, code_field in (
            ("2008_airport_delay_results.csv", "Airport_Code"),
            ("2008_carrier_delay_results.csv", "Carrier_Code"),
        ):
            with self.subTest(filename=filename):
                rows = read_rows(filename)
                self.assertGreater(len(rows), 0)
                self.assertEqual([int(r["Rank"]) for r in rows], list(range(1, len(rows) + 1)))
                self.assertEqual(len({r[code_field] for r in rows}), len(rows))
                delays = [Decimal(r["Delay_Hours"]) for r in rows]
                self.assertTrue(all(value >= 0 for value in delays))
                self.assertEqual(delays, sorted(delays, reverse=True))

    def test_arrival_departure_totals_reconcile(self):
        rows = read_rows("arrival_departure_delay_comparison.csv")
        values = {row["Delay_Type"]: Decimal(row["Total_Hours"]) for row in rows}
        self.assertEqual(len(rows), len(values))
        self.assertEqual(
            set(values),
            {"Arrival", "Departure", "Difference_Arrival_Minus_Departure"},
        )
        self.assertEqual(
            values["Arrival"] - values["Departure"],
            values["Difference_Arrival_Minus_Departure"],
        )

    def test_classification_metrics_match_confusion_matrix(self):
        rows = read_rows("phase2_logistic_regression_results.csv")
        self.assertEqual(len(rows), 1)
        row = rows[0]
        matrix = ast.literal_eval(row["Confusion_Matrix"])
        self.assertEqual(len(matrix), 2)
        self.assertTrue(all(isinstance(r, list) and len(r) == 2 for r in matrix))
        tn, fp = matrix[0]
        fn, tp = matrix[1]
        self.assertTrue(all(isinstance(x, int) and x >= 0 for x in (tn, fp, fn, tp)))
        total = tn + fp + fn + tp
        self.assertGreater(total, 0)
        self.assertGreater(tp + fp, 0)
        self.assertAlmostEqual(float(row["Accuracy"]), (tn + tp) / total, places=5)
        self.assertAlmostEqual(float(row["Precision"]), tp / (tp + fp), places=5)


if __name__ == "__main__":
    unittest.main()
