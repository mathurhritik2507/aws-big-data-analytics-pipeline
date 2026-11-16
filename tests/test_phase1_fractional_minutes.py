"""Fractional-minute Phase 1 aggregation regression using synthetic flights.

SQLite models documented positive-delay logic; this does not execute Hive.
"""
import sqlite3
import unittest


class FractionalDelayContractTests(unittest.TestCase):
    def test_fractional_minutes_are_not_truncated_before_hours_conversion(self):
        rows = [
            ("JFK", "LAX", "AA", 0.25, 0.5, 0, 0),
            ("LAX", "JFK", "AA", -0.75, 1.25, 0, 0),
            ("JFK", "LAX", "UA", None, 0.0, 0, 0),
            ("JFK", "LAX", "UA", 900.0, 900.0, 1, 0),
            ("JFK", "LAX", "UA", 900.0, 900.0, 0, 1),
        ]
        with sqlite3.connect(":memory:") as db:
            db.execute(
                "CREATE TABLE flights (Origin TEXT, Dest TEXT, UniqueCarrier TEXT, "
                "ArrDelay REAL, DepDelay REAL, Cancelled INTEGER, Diverted INTEGER)"
            )
            db.executemany("INSERT INTO flights VALUES (?,?,?,?,?,?,?)", rows)
            valid = "Cancelled = 0 AND Diverted = 0"
            arrivals, departures = db.execute(
                "SELECT SUM(CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END), "
                "SUM(CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END) "
                f"FROM flights WHERE {valid}"
            ).fetchone()
            carrier_minutes = dict(db.execute(
                "SELECT UniqueCarrier, "
                "SUM(CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END + "
                "CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END) "
                f"FROM flights WHERE {valid} GROUP BY UniqueCarrier"
            ))
            airport_minutes = dict(db.execute(
                "SELECT airport, SUM(minutes) FROM ("
                "SELECT Origin AS airport, CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END "
                f"AS minutes FROM flights WHERE {valid} UNION ALL "
                "SELECT Dest AS airport, CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END "
                f"AS minutes FROM flights WHERE {valid}) GROUP BY airport"
            ))
        self.assertEqual((arrivals, departures), (0.25, 1.75))
        self.assertEqual(carrier_minutes, {"AA": 2.0, "UA": 0.0})
        self.assertEqual(airport_minutes, {"JFK": 0.5, "LAX": 1.5})
        self.assertAlmostEqual(sum(airport_minutes.values()) / 60, 2 / 60)


if __name__ == "__main__":
    unittest.main()
