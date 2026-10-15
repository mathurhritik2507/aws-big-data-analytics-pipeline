import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'


class PublishedOutputChecks(unittest.TestCase):
    def test_prediction_count_and_labels(self):
        with (DATA / 'final_10_predictions.csv').open(newline='', encoding='utf-8') as stream:
            records = list(csv.DictReader(stream))
        self.assertEqual(len(records), 10)
        self.assertEqual([int(r['Record']) for r in records], list(range(10)))
        self.assertTrue(all(r['Predicted_Delayed'] in {'Y', 'N'} for r in records))


if __name__ == '__main__':
    unittest.main()
