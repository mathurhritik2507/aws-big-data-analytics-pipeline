# Flight-delay model evaluation audit (2026-10-18)

## Current status

The published Phase 2 metrics in `data/phase2_logistic_regression_results.csv`
(accuracy 0.99475; precision 0.99947) are **historical outputs**, not
validated evidence of a deployable advance prediction model. The four
source sample CSVs referenced by `scripts/phase2_logistic_regression_template.py`
are not included in this repository, so the training run cannot be reproduced
from the checked-in data alone.

## Confirmed target leakage risk

In `sql/phase2_sample_generation.sql`, the label is computed as:

```sql
CASE WHEN ArrDelay > 15 OR DepDelay > 15 THEN 'Y' ELSE 'N' END AS Delayed
```

The exported sample also includes `ArrDelay`, `DepDelay`, actual arrival
and departure times, elapsed/air times, and post-flight delay-cause fields.
The training template drops `Delayed`, `TailNum`, `FlightNum`, and
`Source`, but **does not exclude** the label-generating `ArrDelay` and
`DepDelay` columns. This can let the classifier reconstruct the label
instead of predicting future delays.

The template also fills missing values and one-hot encodes **before** the
random train/test split. That is not a train-only preprocessing workflow.
The split is random, so it does not test performance on later flights.

## Safer evaluation contract for a future PR

1. Specify the prediction point: **before scheduled departure**. Do not use
   `DepTime`, `ArrTime`, `ArrDelay`, `DepDelay`,
   `ActualElapsedTime`, `AirTime`, `TaxiIn`, `TaxiOut`,
   `CarrierDelay`, `WeatherDelay`, `NASDelay`,
   `SecurityDelay`, or `LateAircraftDelay` as model inputs.
   Exclude other fields that are only known after departure.
2. Retain scheduled calendar/time, origin/destination, carrier and other
   genuinely available predeparture features; document availability for each.
3. Create an actual flight-date key from `Year`, `Month`, `DayofMonth`.
   Sort chronologically; train on earlier flights, evaluate on later flights.
   Keep dates in the holdout distinct from training dates.
4. Fit imputers/encoders only on the training partition with a
   `sklearn.pipeline.Pipeline` and `ColumnTransformer`. Apply the fitted
   pipeline to the held-out data without refitting.
5. Compare against a majority-class baseline. Report holdout sample size,
   class balance, precision, recall, F1, confusion matrix, and PR-AUC where
   defined. Preserve random seeds and dependency versions.
6. Add unit tests that fail when forbidden post-event features enter the
   feature set, chronological boundaries overlap, or preprocessing is fitted
   on the full dataset.

## Reproducibility and safety

No AWS resources are required for the offline output test:
`python -m unittest discover -s tests -v` (Python standard library only).
Training cannot be rerun from this checkout until appropriately licensed,
non-sensitive source samples or a clearly labeled synthetic substitute are
provided. Do not commit credentials or private data.

**Portfolio disclosure:** The 99.48% historical accuracy should not be
advertised as prospective flight-delay forecasting accuracy until a
leakage-safe, chronological holdout has been run and documented.
