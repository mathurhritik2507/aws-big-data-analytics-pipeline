-- Phase 2: Hive Sample Generation for Flight Delay Prediction
-- Goal: create a 50,000-row random sample with a Delayed target label.

-- Create sample table structure.
-- Adjust column definitions if your original table schema has additional columns.
CREATE TABLE IF NOT EXISTS hritik_sample AS
SELECT
    Year,
    Month,
    DayofMonth,
    DayOfWeek,
    DepTime,
    CRSDepTime,
    ArrTime,
    CRSArrTime,
    UniqueCarrier,
    FlightNum,
    TailNum,
    ActualElapsedTime,
    CRSElapsedTime,
    AirTime,
    ArrDelay,
    DepDelay,
    Origin,
    Dest,
    Distance,
    TaxiIn,
    TaxiOut,
    Cancelled,
    Diverted,
    CarrierDelay,
    WeatherDelay,
    NASDelay,
    SecurityDelay,
    LateAircraftDelay,
    CASE
        WHEN ArrDelay > 15 OR DepDelay > 15 THEN 'Y'
        ELSE 'N'
    END AS Delayed
FROM hritik_flights_2008
WHERE Cancelled = 0 AND Diverted = 0
DISTRIBUTE BY RAND()
SORT BY RAND()
LIMIT 50000;

-- Validate sample size.
SELECT COUNT(*) FROM hritik_sample;

-- Preview sampled records.
SELECT * FROM hritik_sample LIMIT 20;

-- Export process used on EMR after Hive output generation:
-- cat * > hritik_sample_2008.csv
