# AWS Big Data Analytics Pipeline — Flight Delay Analysis

## Overview

This repository presents an end-to-end AWS-based big data analytics and machine learning workflow using U.S. flight delay data. The project was completed in two phases using AWS EMR, Amazon S3, Hive, SSH, Python, and Logistic Regression.

- **Phase 1:** Hive-based flight delay analysis for the year 2008.
- **Phase 2:** Random sample generation from Hive, Python-based data cleaning, Logistic Regression model training, evaluation, and prediction output.

## Project Objective

The objective of this project was to demonstrate how cloud-based big data tools can be used to store, process, query, analyze, and model large airline delay datasets. The workflow combines AWS infrastructure, Hive queries, dataset preparation, and machine learning evaluation.

## Tools & Technologies

- AWS EMR
- Amazon S3
- Apache Hive
- Hadoop
- SSH / SCP
- Python
- Pandas
- Scikit-learn
- Matplotlib
- Logistic Regression
- Excel / CSV output

## Phase 1 — Flight Delay Analysis Using AWS EMR and Hive

### Workflow

1. Downloaded and prepared the 2008 airline dataset.
2. Removed the original CSV header before loading into Hive.
3. Created an AWS EMR cluster with Hadoop and Hive.
4. Uploaded `2008_clean.csv`, `airports.csv`, and `carriers.csv` to Amazon S3.
5. Connected to the EMR primary node through SSH.
6. Created the Hive table `hritik_flights_2008`.
7. Loaded the cleaned 2008 dataset into Hive.
8. Validated the table using a 100-row sample query.
9. Calculated top airports, top carriers, and arrival-vs-departure delay totals.

### Phase 1 Results

| Analysis | Result |
|---|---:|
| Top Airport | ORD — 95,555.62 delay hours |
| Top Carrier | WN / Southwest — 164,150.83 delay hours |
| Arrival Delay Total | 601,104.65 hours |
| Departure Delay Total | 530,608.25 hours |
| Larger Delay Type | Arrival delays |

### Key Observation

The 2008 analysis shows that delay totals were concentrated around major U.S. hub airports and large national carriers. Chicago O'Hare International Airport had the highest airport delay burden, and Southwest Airlines had the highest carrier delay total.

## Phase 2 — Flight Delay Prediction Using Logistic Regression

### Workflow

1. Created and verified an AWS EMR cluster for Phase 2.
2. Used Hive to create a structured flight delay sample table.
3. Generated and validated an individual 50,000-row sample from the 2008 flight data.
4. Exported the sample file from EMR and downloaded it locally using SCP.
5. Combined four team member samples into one cleaned dataset.
6. Filtered valid years: 1995, 1997, 2004, and 2008.
7. Filtered valid delayed labels: `Y` and `N`.
8. Encoded categorical variables and prepared train/test data.
9. Trained a Logistic Regression model.
10. Evaluated the model using accuracy, precision, and confusion matrix.
11. Extracted the assigned 10 Group 5 target rows and generated final predictions.

### Phase 2 Model Results

| Metric | Value |
|---|---:|
| Model | Logistic Regression |
| Accuracy | 0.99475 |
| Precision | 0.99947 |
| Confusion Matrix | [[2092, 1], [20, 1887]] |
| Test Split | 20% test data |
| Final Output | Hritik_10_Predictions.xlsx |

## Repository Structure

```text
aws-big-data-analytics-pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md
│   ├── 2008_airport_delay_results.csv
│   ├── 2008_carrier_delay_results.csv
│   ├── arrival_departure_delay_comparison.csv
│   ├── phase2_logistic_regression_results.csv
│   └── final_10_predictions.csv
├── sql/
│   ├── phase1_hive_analysis.sql
│   └── phase2_sample_generation.sql
├── scripts/
│   ├── data_cleaning_commands.sh
│   └── phase2_logistic_regression_template.py
├── images/
│   └── README.md
├── report/
│   └── project_summary.md
└── docs/
    └── github_upload_checklist.md
```

## How to Use This Repository

1. Upload this full folder to the GitHub repository named `aws-big-data-analytics-pipeline`.
2. Add your real screenshots in the `images/` folder.
3. Add your original notebook, if available, to the root folder or a `notebooks/` folder.
4. Keep the CSV result files because they show the final project metrics.
5. Update the README only if you add more real files.

## Resume Summary

Designed and executed an AWS EMR and Hive-based big data analytics pipeline for 2008 U.S. flight delay data, identifying top delay contributors across airports, carriers, and delay types. Extended the workflow into a Logistic Regression prediction pipeline by generating a 50,000-row Hive sample, cleaning combined team datasets in Python, and achieving 99.48% model accuracy.
