-- Phase 1: AWS EMR + Hive Flight Delay Analysis
-- Project: 2008 Flight Delay Analysis
-- Student table: hritik_flights_2008

-- 1. Create main Hive table
CREATE TABLE IF NOT EXISTS hritik_flights_2008 (
    Year INT,
    Month INT,
    DayofMonth INT,
    DayOfWeek INT,
    DepTime STRING,
    CRSDepTime STRING,
    ArrTime STRING,
    CRSArrTime STRING,
    UniqueCarrier STRING,
    FlightNum STRING,
    TailNum STRING,
    ActualElapsedTime STRING,
    CRSElapsedTime STRING,
    AirTime STRING,
    ArrDelay DOUBLE,
    DepDelay DOUBLE,
    Origin STRING,
    Dest STRING,
    Distance DOUBLE,
    TaxiIn STRING,
    TaxiOut STRING,
    Cancelled INT,
    CancellationCode STRING,
    Diverted INT,
    CarrierDelay DOUBLE,
    WeatherDelay DOUBLE,
    NASDelay DOUBLE,
    SecurityDelay DOUBLE,
    LateAircraftDelay DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 2. Load cleaned CSV from local EMR node
LOAD DATA LOCAL INPATH '/home/hadoop/2008_clean.csv'
INTO TABLE hritik_flights_2008;

-- 3. Validate loaded data
SELECT * FROM hritik_flights_2008 LIMIT 100;

-- 4. Top 3 airports by total delay hours
-- Combines origin departure delay and destination arrival delay.
SELECT airport_code, ROUND(SUM(delay_minutes)/60, 2) AS delay_hours
FROM (
    SELECT Origin AS airport_code,
           CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END AS delay_minutes
    FROM hritik_flights_2008
    WHERE Cancelled = 0 AND Diverted = 0

    UNION ALL

    SELECT Dest AS airport_code,
           CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END AS delay_minutes
    FROM hritik_flights_2008
    WHERE Cancelled = 0 AND Diverted = 0
) airport_delays
GROUP BY airport_code
ORDER BY delay_hours DESC
LIMIT 3;

-- Expected top results:
-- ORD: 95,555.62 hours
-- ATL: 67,122.05 hours
-- DFW: 45,073.57 hours

-- 5. Top 3 carriers by total delay hours
SELECT UniqueCarrier AS carrier_code,
       ROUND(SUM(
           CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END +
           CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END
       )/60, 2) AS delay_hours
FROM hritik_flights_2008
WHERE Cancelled = 0 AND Diverted = 0
GROUP BY UniqueCarrier
ORDER BY delay_hours DESC
LIMIT 3;

-- Expected top results:
-- WN: 164,150.83 hours
-- AA: 122,445.80 hours
-- UA: 94,358.58 hours

-- 6. Arrival vs departure delay comparison
SELECT 'Arrival' AS delay_type,
       ROUND(SUM(CASE WHEN ArrDelay > 0 THEN ArrDelay ELSE 0 END)/60, 2) AS total_hours
FROM hritik_flights_2008
WHERE Cancelled = 0 AND Diverted = 0

UNION ALL

SELECT 'Departure' AS delay_type,
       ROUND(SUM(CASE WHEN DepDelay > 0 THEN DepDelay ELSE 0 END)/60, 2) AS total_hours
FROM hritik_flights_2008
WHERE Cancelled = 0 AND Diverted = 0;

-- Expected results:
-- Arrival: 601,104.65 hours
-- Departure: 530,608.25 hours
