# Data Folder

This folder contains small result files that summarize the project outcomes.

Large raw datasets such as `2008.csv` or `2008_clean.csv` are not included because airline datasets can be large. In the original workflow, the cleaned 2008 dataset was loaded into Hive on AWS EMR and the sample file was exported from EMR.

## Included Files

- `2008_airport_delay_results.csv` — top 3 airports by delay hours.
- `2008_carrier_delay_results.csv` — top 3 carriers by delay hours.
- `arrival_departure_delay_comparison.csv` — arrival versus departure delay totals.
- `phase2_logistic_regression_results.csv` — model performance metrics.
- `final_10_predictions.csv` — final target-row prediction labels.
