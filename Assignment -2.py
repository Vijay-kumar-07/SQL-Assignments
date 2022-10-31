create schema accidents;
use accidents;

# Creating 3 Tables: accident, vehicle, vehicle_types
create table accident(
accident_index varchar(15),
accident_severity int);

create table vehicles(
accident_index varchar(15),
vehicle_type varchar(50));

create table vehicle_types(
vehicle_code int,
vehicle_type varchar(10));

# Loading Data

set session sql_mode = '';
SET GLOBAL local_infile=1;

LOAD DATA LOCAL INFILE 'C:/Vijay/Personal/SQL/Analyzing Road Safety in UK/Accidents_2015.csv'
INTO TABLE accident
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 rows
(@col1, @dummy, @dummy, @dummy, @dummy, @dummy, @col2, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy)
SET accident_index=@col1, accident_severity=@col2;

LOAD DATA LOCAL INFILE 'C:/Vijay/Personal/SQL/Analyzing Road Safety in UK/Vehicles_2015.csv'
INTO TABLE vehicles
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@col1, @dummy, @col2, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy)
SET accident_index=@col1, vehicle_type=@col2;

LOAD DATA LOCAL INFILE 'C:/Vijay/Personal/SQL/Analyzing Road Safety in UK/vehicle_types.csv'
INTO TABLE vehicle_types
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


select * from vehicle_types limit 5;

create table accidents_median(
vehicle_types varchar(100),
severity int);

select vehicle_type from vehicle_types where vehicle_type like '%torcycle%';

select * from accidents_median;

## Creating index on accident_index as it is using in both vehicles and accident tables and join clauses 
## using indexes will perform faster 
create index accident_index
on accident(accident_index);

create index accident_index
on vehicles(accident_index);

# 1. Evaluate the median severity value of accidents caused by various Motorcycles.
import sys
sys.path.insert(0,"c:\python310\lib\site-packages")
import pymysql

myConnection = pymysql.connect(
host = "localhost", user="root",password="mysql", db = "accidents")

cur = myConnection.cursor()
cur.execute("select vehicle_type from vehicle_types where vehicle_type like '%torcycle%';")
cycle_list = cur.fetchall()

selectSQL = ('''
SELECT vt.vehicle_type, a.accident_severity
FROM accident a
JOIN vehicles v ON a.accident_index = v.accident_index
JOIN vehicle_types vt ON v.vehicle_type = vt.vehicle_code
WHERE vt.vehicle_type LIKE %s
ORDER BY a.accident_severity;
''')
insert_SQL = ('''INSERT INTO accidents_median
VALUES(%s, %s);''')

for cycle in cycle_list:
    cur.execute(selectSQL, cycle[0])
    accidents = cur.fetchall()
    
    quotient, remainder = divmod(len(accidents), 2)
    if remainder:
        median_severity = accidents[quotient][1]
    else:
        median_severity = (accidents[quotient]
                           [1] + accidents[quotient + 2][1]) / 2
    print("finding Median Severity for ", cycle[0])
    cur.execute(insert_SQL, (cycle[0], median_severity))
    
myConnection.commit()
myConnection.close()





## 2. Evaluate Accident Severity and Total Accidents per Vehicle Type.
SELECT vt.vehicle_type AS 'Vehicle Type', a.accident_severity AS 'Severity', COUNT(vt.vehicle_type) AS 'Number of Accidents'
FROM accident a
JOIN vehicles v ON a.accident_index = v.accident_index
JOIN vehicle_types vt ON v.vehicle_type = vt.vehicle_code
GROUP BY 1
ORDER BY 2,3;


# 3. Calculate the Average Severity by vehicle type.
SELECT vt.vehicle_type AS 'Vehicle Type', AVG(a.accident_severity) AS 'Average Severity', COUNT(vt.vehicle_type) AS 'Number of Accidents'
FROM accident a
JOIN vehicles v ON a.accident_index = v.accident_index
JOIN vehicle_types vt ON v.vehicle_type = vt.vehicle_code
GROUP BY 1
ORDER BY 2,3;


# 4. Calculate the Average Severity and Total Accidents by Motorcycle.
SELECT vt.vehicle_type AS 'Vehicle Type', AVG(a.accident_severity) AS 'Average Severity', COUNT(vt.vehicle_type) AS 'Number of Accidents'
FROM accident a
JOIN vehicles v ON a.accident_index = v.accident_index
JOIN vehicle_types vt ON v.vehicle_type = vt.vehicle_code
WHERE vt.vehicle_type LIKE '%otorcycle%'
GROUP BY 1
ORDER BY 2,3;







