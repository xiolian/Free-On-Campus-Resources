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


DROP TABLE IF EXISTS tutoring_raw;
CREATE TABLE tutoring_raw (
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

.mode csv
.import tutoring.csv tutoring_raw

DELETE FROM tutoring_raw
WHERE resource_type = 'ResourceType';

DROP TABLE IF EXISTS tutoring;
CREATE TABLE tutoring (
    tutoring_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

INSERT INTO tutoring (
    resource_type, subject, department, building,
    location, weekday, start_time, end_time, notes
)
SELECT
    resource_type, subject, department, building,
    location, weekday, start_time, end_time, notes
FROM tutoring_raw;

DROP TABLE tutoring_raw;

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
WHERE AcaSuppService = 'acaSuppService';

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
    FundingName TEXT,
    Department  TEXT,
    Building    TEXT,
    Location    TEXT,
    Weekday     TEXT,
    StartTime   TEXT,
    EndTime     TEXT,
    Link        TEXT
);

.mode csv
.import fundingnew.csv funding_raw

DELETE FROM funding_raw
WHERE FundingType = 'FundingType';

DROP TABLE IF EXISTS funding;
CREATE TABLE funding (
    funding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_type VARCHAR(100) NOT NULL,
    funding_name VARCHAR(100) NOT NULL,
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
    funding_name,
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
    FundingName,
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


-- ==============================================================

DROP TABLE IF EXISTS Student;

CREATE TABLE Student (
    studentID   VARCHAR(50) PRIMARY KEY,
    studentName VARCHAR(100) NOT NULL,
    studentPass VARCHAR(50) NOT NULL
);

.mode csv
.import student.csv Student

DELETE FROM Student
WHERE studentID = 'studentID';

DROP TABLE IF EXISTS TutoringRecord;

CREATE TABLE TutoringRecord (
    studentID   VARCHAR(50) NOT NULL,
    studentName VARCHAR(100) NOT NULL,
    tutoring_id INTEGER NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    subject      VARCHAR(100) NOT NULL,
    department   VARCHAR(100),
    building     VARCHAR(50),
    location     VARCHAR(100),
    weekday      VARCHAR(50),
    start_time   TEXT,
    end_time     TEXT
);

.mode csv
.import TutoringRecord.csv TutoringRecord

DELETE FROM TutoringRecord
WHERE studentID = 'studentID';

-- ==============================================================

DROP TABLE IF EXISTS StudentSuppliesRecord;

CREATE TABLE StudentSuppliesRecord (
    studentID    VARCHAR(50) NOT NULL,
    studentName  VARCHAR(100) NOT NULL,
    supply_id    INTEGER NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    item         VARCHAR(100) NOT NULL,
    department    VARCHAR(100),
    building     VARCHAR(50),
    location     VARCHAR(100),
    weekday      VARCHAR(50),
    start_time   TEXT,
    end_time     TEXT
);

.mode csv
.import StudentSuppliesRecord.csv StudentSuppliesRecord

DELETE FROM StudentSuppliesRecord
WHERE studentID = 'studentID';

DROP TABLE IF EXISTS HealthRecord;

CREATE TABLE HealthRecord (
    studentID    VARCHAR(50) NOT NULL,
    studentName  VARCHAR(100) NOT NULL,
    health_id    INTEGER NOT NULL,
    health_category VARCHAR(100) NOT NULL,
    service      VARCHAR(255) NOT NULL,
    location     VARCHAR(255),
    weekday      VARCHAR(50),
    start_time   TEXT,
    end_time     TEXT,
    link        VARCHAR(255)
);

.mode csv
.import HealthRecord.csv HealthRecord

DELETE FROM HealthRecord
WHERE studentID = 'studentID';

-- ==============================================================

DROP TABLE IF EXISTS AcademicSupportRecord;

CREATE TABLE AcademicSupportRecord (
    studentID     VARCHAR(50) NOT NULL,
    studentName   VARCHAR(100) NOT NULL,
    support_id    INTEGER NOT NULL,
    aca_supp_service VARCHAR(100) NOT NULL,
    service_name  VARCHAR(255) NOT NULL,
    department    VARCHAR(100),
    building      VARCHAR(50),
    location      VARCHAR(255),
    weekday       VARCHAR(50),
    start_time    TEXT,
    end_time      TEXT,
    link         VARCHAR(255)
);

.mode csv
.import AcademicSupportRecord.csv AcademicSupportRecord

DELETE FROM AcademicSupportRecord
WHERE studentID = 'studentID';

-- ==============================================================

DROP TABLE IF EXISTS AdvisorRecord;

CREATE TABLE AdvisorRecord (
    studentID    VARCHAR(50) NOT NULL,
    studentName  VARCHAR(100) NOT NULL,
    advisor_id   INTEGER NOT NULL,
    name         VARCHAR(100) NOT NULL,
    affiliation  TEXT,
    role         VARCHAR(100),
    building     VARCHAR(50),
    location     VARCHAR(255),
    link         VARCHAR(255)
);

.mode csv
.import AdvisorRecord.csv AdvisorRecord

DELETE FROM AdvisorRecord
WHERE studentID = 'studentID';

-- ##############################################################

DROP TABLE IF EXISTS FundingRecord;

CREATE TABLE FundingRecord (
    studentID    VARCHAR(50) NOT NULL,
    studentName  VARCHAR(100) NOT NULL,
    funding_id   INTEGER NOT NULL,
    funding_type VARCHAR(100) NOT NULL,
    funding_name VARCHAR(100) NOT NULL,
    department   VARCHAR(100),
    building     VARCHAR(50),
    location     VARCHAR(255),
    weekday      VARCHAR(50),
    start_time   TEXT,
    end_time     TEXT,
    link         VARCHAR(255)
);

.mode csv
.import FundingRecord.csv FundingRecord

DELETE FROM FundingRecord
WHERE studentID = 'studentID';