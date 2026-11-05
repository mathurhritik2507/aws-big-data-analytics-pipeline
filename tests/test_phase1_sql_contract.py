"""Offline reference checks for Phase 1 Hive delay aggregation semantics.

SQLite exercises equivalent aggregations on tiny synthetic rows; this does NOT
execute Hive or validate EMR configuration.
"""
import sqlite3
import unittest


class FlightDelayAggregationContractTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute(
            "CREATE TABLE flights (Origin TEXT, Dest TEXT, UniqueCarrier TEXT, "
            "ArrDelay REAL, DepDelay REAL, Cancelled INTEGER, Diverted INTEGER)"
        )
        self.db.executemany(
            "INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                ("JFK", "LAX", "AA", 30, 60, 0, 0),
                ("JFK", "ORD", "AA", -10, 15, 0, 0),
                ("LAX", "JFK", "UA", None, -5, 0, 0),
                ("JFK", "LAX", "AA", 999, 999, 1, 0),
                ("ORD", "JFK", "UA", 999, 999, 0, 1),
            ],
        )

    def tearDown(self):
        self.db.close()

    def test_airport_origin_and_destination_are_counted_separately(self):
        rows = self.db.execute(
            """
            SELECT airport, SUM(minutes) FROM (
                SELECT Origin AS airport,
                    CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END AS minutes
                FROM flights WHERE Cancelled = 0 AND Diverted = 0
                UNION ALL
                SELECT Dest AS airport,
                    CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END AS minutes
                FROM flights WHERE Cancelled = 0 AND Diverted = 0
            ) GROUP BY airport
            """
        ).fetchall()
        self.assertEqual(dict(rows), {"JFK": 75.0, "LAX": 30.0, "ORD": 0.0})

    def test_carrier_aggregates_ignore_negative_null_cancelled_diverted(self):
        rows = self.db.execute(
            """
            SELECT UniqueCarrier,
                SUM(CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END +
                    CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END)
            FROM flights WHERE Cancelled = 0 AND Diverted = 0
            GROUP BY UniqueCarrier
            """
        ).fetchall()
        self.assertEqual(dict(rows), {"AA": 105.0, "UA": 0.0})

    def test_arrival_departure_reconcile_to_carrier_total(self):
        arrival, departure = self.db.execute(
            """
            SELECT SUM(CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END),
                   SUM(CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END)
            FROM flights WHERE Cancelled = 0 AND Diverted = 0
            """
        ).fetchone()
        self.assertEqual((arrival, departure), (30.0, 75.0))
        self.assertEqual(arrival + departure, 105.0)


if __name__ == "__main__":
    unittest.main()
