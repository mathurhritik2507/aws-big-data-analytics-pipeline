"""Offline synthetic regression: Phase 1 aggregation is invariant to row order.

SQLite is an analogue of the documented Hive rules, not a Hive execution.
No real flight data, AWS resources, or third-party dependencies are used.
"""
import sqlite3
import unittest


ROWS = [
    ("JFK", "LAX", "AA", 12.0, 4.0, 0, 0),
    ("LAX", "JFK", "UA", 3.0, -2.0, 0, 0),
    ("JFK", "JFK", "AA", None, 7.0, 0, 0),
    ("LAX", "JFK", "UA", 500.0, 500.0, 1, 0),
    ("JFK", "LAX", "AA", 500.0, 500.0, 0, 1),
]


def aggregate(rows):
    with sqlite3.connect(":memory:") as db:
        db.execute(
            "CREATE TABLE flights (origin TEXT, dest TEXT, carrier TEXT, "
            "arr REAL, dep REAL, cancelled INTEGER, diverted INTEGER)"
        )
        db.executemany("INSERT INTO flights VALUES (?,?,?,?,?,?,?)", rows)
        eligible = "cancelled = 0 AND diverted = 0"
        airport = dict(db.execute(
            "SELECT airport, SUM(minutes) FROM ("
            "SELECT origin AS airport, CASE WHEN dep > 0 THEN dep ELSE 0 END "
            f"AS minutes FROM flights WHERE {eligible} UNION ALL "
            "SELECT dest AS airport, CASE WHEN arr > 0 THEN arr ELSE 0 END "
            f"AS minutes FROM flights WHERE {eligible}) GROUP BY airport"
        ))
        carrier = dict(db.execute(
            "SELECT carrier, SUM(CASE WHEN arr > 0 THEN arr ELSE 0 END + "
            "CASE WHEN dep > 0 THEN dep ELSE 0 END) FROM flights "
            f"WHERE {eligible} GROUP BY carrier"
        ))
        total = db.execute(
            "SELECT SUM(CASE WHEN arr > 0 THEN arr ELSE 0 END + "
            "CASE WHEN dep > 0 THEN dep ELSE 0 END) FROM flights "
            f"WHERE {eligible}"
        ).fetchone()[0]
        return airport, carrier, total


class Phase1OrderIndependenceTests(unittest.TestCase):
    def test_row_permutation_preserves_all_aggregates(self):
        expected = aggregate(ROWS)
        self.assertEqual(expected[0], {"JFK": 14.0, "LAX": 12.0})
        self.assertEqual(expected[1], {"AA": 23.0, "UA": 3.0})
        self.assertEqual(expected[2], 26.0)
        for permutation in (list(reversed(ROWS)), ROWS[2:] + ROWS[:2]):
            with self.subTest(permutation=permutation):
                self.assertEqual(aggregate(permutation), expected)
                self.assertEqual(sum(aggregate(permutation)[0].values()),
                                 aggregate(permutation)[2])


if __name__ == "__main__":
    unittest.main()
