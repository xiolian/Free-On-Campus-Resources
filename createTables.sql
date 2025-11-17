
-- Create Student Supplies
DROP TABLE IF EXISTS supplies_raw;

CREATE TABLE supplies_raw (
    ResourceType TEXT,
    Item TEXT,
    Department TEXT,
    Building TEXT,
    Location TEXT,
    LimitInfo TEXT,
    Weekday TEXT,
    StartTime TEXT,
    EndTime TEXT,
    Notes TEXT
);

.mode csv
.import stusupp2.csv supplies_raw

DELETE FROM supplies_raw
WHERE ResourceType = 'ResourceType';


DROP TABLE IF EXISTS student_supplies;

CREATE TABLE student_supplies (
    supply_id      INTEGER PRIMARY KEY AUTOINCREMENT,  -- required by SQLite
    resource_type  VARCHAR(50) NOT NULL,
    item           VARCHAR(100) NOT NULL,
    department     VARCHAR(100),
    building       VARCHAR(50),
    location       VARCHAR(100),
    limit_info     VARCHAR(255),
    weekday        VARCHAR(50),
    start_time     TIME,
    end_time       TIME,
    notes          TEXT
);


INSERT INTO student_supplies (
    resource_type, item, department, building, location,
    limit_info, weekday, start_time, end_time, notes
)
SELECT
    ResourceType, Item, Department, Building, Location,
    LimitInfo, Weekday, StartTime, EndTime, Notes
FROM supplies_raw;



-- ##############################################################
-- Create Tutoring Table with Updated Schema
DROP TABLE IF EXISTS tutoring;

CREATE TABLE tutoring (
    resource_type TEXT,
    subject TEXT,
    department TEXT,
    building TEXT,
    location TEXT,
    weekday TEXT,
    start_time TEXT,
    end_time TEXT,
    notes TEXT
);

CREATE TABLE tutoring_clone (
    tutoring_id INT AUTO_INCREMENT PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    building VARCHAR(50),
    location VARCHAR(100),
    weekday VARCHAR(50),
    start_time TEXT,
    end_time TEXT,
    notes TEXT
);

INSERT INTO tutoring_clone (
    resource_type,
    subject,
    department,
    building,
    location,
    weekday,
    start_time,
    end_time,
    notes
)
SELECT
    resource_type,
    subject,
    department,
    building,
    location,
    weekday,
    start_time,
    end_time,
    notes
FROM tutoring;

DROP TABLE tutoring;

ALTER TABLE tutoring_clone RENAME TO tutoring;

ALTER TABLE tutoring RENAME TO tutoring_old;

CREATE TABLE tutoring (
    tutoring_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_type VARCHAR(50) NOT NULL,
    subject       VARCHAR(100) NOT NULL,
    department    VARCHAR(100),
    building      VARCHAR(50),
    location      VARCHAR(100),
    weekday       VARCHAR(50),
    start_time    TIME,
    end_time      TIME,
    notes         TEXT
);

INSERT INTO tutoring (
    resource_type,
    subject,
    department,
    building,
    location,
    weekday,
    start_time,
    end_time,
    notes
)
SELECT
    resource_type,
    subject,
    department,
    building,
    location,
    weekday,
    start_time,
    end_time,
    notes
FROM tutoring_old;

-- ##############################################################

-- DROP TABLE IF EXISTS health_services;

-- CREATE TABLE health_services (
--     health_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     health_category VARCHAR(100) NOT NULL,
--     service VARCHAR(255) NOT NULL,
--     location VARCHAR(255),
--     weekday VARCHAR(50),
--     start_time TEXT,   -- store HH:MM
--     end_time TEXT,     -- store HH:MM
--     link VARCHAR(255)
-- );

-- DROP TABLE IF EXISTS health_services;
DROP TABLE IF EXISTS health_services_raw;

CREATE TABLE health_services_raw (
    HealthCategory TEXT,
    Service        TEXT,
    Location       TEXT,
    WeekDay        TEXT,
    StartTime      TEXT,
    EndTime        TEXT,
    Link           TEXT
);

DELETE FROM health_services_raw
WHERE HealthCategory = 'HealthCategory'
  AND Service = 'Service';

DROP TABLE IF EXISTS health_services;

CREATE TABLE health_services (
    health_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    health_category VARCHAR(100) NOT NULL,
    service         VARCHAR(255) NOT NULL,
    location        VARCHAR(255),
    weekday         VARCHAR(50),
    start_time      TEXT,
    end_time        TEXT,
    link            VARCHAR(255)
);

INSERT INTO health_services (
    health_category,
    service,
    location,
    weekday,
    start_time,
    end_time,
    link
)
SELECT
    HealthCategory,
    Service,
    Location,
    WeekDay,
    StartTime,
    EndTime,
    Link
FROM health_services_raw;

DROP TABLE health_services_raw;
SELECT COUNT(*) FROM health_services;
SELECT * FROM health_services LIMIT 3;
-- ##############################################################

DROP TABLE IF EXISTS academic_advising_raw;

CREATE TABLE academic_advising_raw (
    Name TEXT,
    Affiliation TEXT,
    Role TEXT,
    Building TEXT,
    Location TEXT,
    Link TEXT
);

.mode csv
.import academic_advising.csv academic_advising_raw

DELETE FROM academic_advising_raw
WHERE Name = 'Name';

DROP TABLE IF EXISTS academic_advising;

CREATE TABLE academic_advising (
    advisor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    affiliation TEXT,
    role VARCHAR(100),
    building VARCHAR(50),
    location VARCHAR(255),
    link VARCHAR(255)
);

INSERT INTO academic_advising (
    name, affiliation, role, building, location, link
)
SELECT
    Name, Affiliation, Role, Building, Location, Link
FROM academic_advising_raw;
-- ##############################################################

DROP TABLE IF EXISTS academic_support_raw;

CREATE TABLE academic_support_raw (
    AcaSuppService TEXT,
    ServiceName    TEXT,
    Department     TEXT,
    Building       TEXT,
    Location       TEXT,
    Weekday        TEXT,
    StartTime      TEXT,
    EndTime        TEXT,
    Link           TEXT
);

.mode csv
.import academic_support.csv academic_support_raw

DELETE FROM academic_support_raw
WHERE AcaSuppService = 'AcaSuppService';

DROP TABLE IF EXISTS academic_support;

CREATE TABLE academic_support (
    support_id INTEGER PRIMARY KEY AUTOINCREMENT,
    aca_supp_service VARCHAR(100) NOT NULL,
    service_name VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    building VARCHAR(50),
    location VARCHAR(255),
    weekday VARCHAR(50),
    start_time TIME,
    end_time TIME,
    link VARCHAR(255)
);

INSERT INTO academic_support (
    aca_supp_service,
    service_name,
    department,
    building,
    location,
    weekday,
    start_time,
    end_time,
    link
)
SELECT
    AcaSuppService,
    ServiceName,
    Department,
    Building,
    Location,
    Weekday,
    StartTime,
    EndTime,
    Link
FROM academic_support_raw;
-- ##############################################################

DROP TABLE IF EXISTS funding_raw;
CREATE TABLE funding_raw (
    FundingType TEXT,
    Department  TEXT,
    Building    TEXT,
    Location    TEXT,
    Weekday     TEXT,
    StartTime   TEXT,
    EndTime     TEXT,
    Link        TEXT
);

.mode csv
.import funding.csv funding_raw

DELETE FROM funding_raw
WHERE FundingType = 'FundingType';

DROP TABLE IF EXISTS funding;
CREATE TABLE funding (
    funding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_type VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    building VARCHAR(50),
    location VARCHAR(255),
    weekday VARCHAR(50),
    start_time TIME,
    end_time TIME,
    link VARCHAR(255)
);

INSERT INTO funding (
    funding_type,
    department,
    building,
    location,
    weekday,
    start_time,
    end_time,
    link
)
SELECT
    FundingType,
    Department,
    Building,
    Location,
    Weekday,
    StartTime,
    EndTime,
    Link
FROM funding_raw;
-- ##############################################################

DROP TABLE IF EXISTS academic_advising_raw;
DROP TABLE IF EXISTS academic_support_raw;
DROP TABLE IF EXISTS funding_raw;
DROP TABLE IF EXISTS supplies_raw;
DROP TABLE IF EXISTS tutoring_old;
DROP TABLE IF EXISTS health_service_raw;