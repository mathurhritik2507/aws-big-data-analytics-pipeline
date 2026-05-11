# Project Summary — AWS Big Data Analytics Pipeline

## Project Name

AWS Big Data Analytics Pipeline — Flight Delay Analysis and Prediction

## Student

Hritik Mathur

## Course Context

CS673 Scalable Databases

## Summary

This project demonstrates an end-to-end big data workflow using AWS EMR, Amazon S3, Hive, Python, and Logistic Regression. The project used 2008 U.S. flight delay data for Hive-based analysis and later extended the workflow into a machine learning pipeline for flight delay prediction.

## Phase 1 Summary

The first phase focused on analyzing the 2008 flight delay dataset using Hive on AWS EMR. The dataset was cleaned by removing the CSV header, uploaded to S3, copied to EMR, loaded into Hive, and validated using sample queries.

### Phase 1 Results

- Top airport by delay hours: ORD — 95,555.62 hours
- Top carrier by delay hours: WN / Southwest — 164,150.83 hours
- Arrival delay total: 601,104.65 hours
- Departure delay total: 530,608.25 hours
- Arrival delays were higher by 70,496.40 hours

## Phase 2 Summary

The second phase focused on prediction. A 50,000-row sample was generated from Hive and exported. Team samples were combined and cleaned in Python. A Logistic Regression model was trained after encoding categorical variables and splitting the dataset into train and test sets.

### Phase 2 Results

- Model: Logistic Regression
- Accuracy: 0.99475
- Precision: 0.99947
- Confusion matrix: [[2092, 1], [20, 1887]]
- Final output: 10 assigned prediction rows saved to Excel

## Key Learnings

- AWS EMR cluster setup and Hive execution
- S3-based cloud storage for big data files
- SSH/SCP workflow for remote data handling
- Hive table creation and analytical SQL queries
- Large dataset sampling and validation
- Python-based data cleaning and model training
- Logistic Regression evaluation using accuracy, precision, and confusion matrix

## Future Improvements

- Automate the pipeline using AWS Lambda or Step Functions
- Use AWS Glue or EMR Spark for scalable processing
- Add model tracking and experiment comparison
- Deploy prediction results through a dashboard
- Compare Logistic Regression with Random Forest, XGBoost, and Spark MLlib
