"""Synthetic edge-case regression for the documented Phase 1 delay rules.

SQLite mirrors the aggregation semantics; it does not execute Hive or AWS.
"""
import sqlite3
import unittest


class DelayBoundaryChecks(unittest.TestCase):
    def test_zero_delay_same_airport_and_excluded_flights(self):
        rows = [
            ("JFK", "JFK", "AA", 30.0, 0.0, 0, 0),
            ("JFK", "LAX", "AA", -4.0, 90.0, 0, 0),
            ("LAX", "JFK", "UA", None, None, 0, 0),
            ("JFK", "LAX", "AA", 1000.0, 1000.0, 1, 0),
            ("JFK", "LAX", "AA", 1000.0, 1000.0, 0, 1),
        ]
        with sqlite3.connect(":memory:") as db:
            db.execute(
                "CREATE TABLE flights (Origin TEXT, Dest TEXT, UniqueCarrier TEXT, "
                "ArrDelay REAL, DepDelay REAL, Cancelled INTEGER, Diverted INTEGER)"
            )
            db.executemany("INSERT INTO flights VALUES (?,?,?,?,?,?,?)", rows)
            airport_totals = dict(db.execute("""
                SELECT airport, SUM(delay_minutes) FROM (
                    SELECT Origin AS airport,
                           CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END AS delay_minutes
                    FROM flights WHERE Cancelled = 0 AND Diverted = 0
                    UNION ALL
                    SELECT Dest AS airport,
                           CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END AS delay_minutes
                    FROM flights WHERE Cancelled = 0 AND Diverted = 0
                ) GROUP BY airport
            """).fetchall())
            self.assertEqual(airport_totals, {"JFK": 120.0, "LAX": 0.0})
            # An airport appearing as both origin and destination must retain
            # both contributions; cancelled/diverted outliers must not count.
            self.assertEqual(sum(airport_totals.values()) / 60, 2.0)


if __name__ == "__main__":
    unittest.main()
