-- schema.sql

-- Table for User Authentication
CREATE TABLE IF NOT EXISTS Student (
    studentID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentName TEXT UNIQUE NOT NULL,
    studentEmail TEXT UNIQUE NOT NULL,
    studentPassHash TEXT NOT NULL -- Store hashed password
);

-- Resource Tracking Tables
CREATE TABLE IF NOT EXISTS HealthRecord (
    HealthID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID INTEGER,
    Health_category TEXT,
    Service TEXT,
    Location TEXT, -- Expects a "Lat, Lng" string
    Weekday TEXT,
    Start_time TEXT,
    End_time TEXT,
    Link TEXT,
    FOREIGN KEY (studentID) REFERENCES Student(studentID)
);

CREATE TABLE IF NOT EXISTS AdvisorRecord (
    AdvisorID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID INTEGER,
    Name TEXT,
    Affiliation TEXT,
    Role TEXT,
    Building TEXT,
    Location TEXT, -- Expects a "Lat, Lng" string
    Link TEXT,
    FOREIGN KEY (studentID) REFERENCES Student(studentID)
);

CREATE TABLE IF NOT EXISTS AcademicSupportRecord (
    SupportID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID INTEGER,
    Aca_supp_service TEXT,
    Service_name TEXT,
    Department TEXT,
    Building TEXT,
    Location TEXT, -- Expects a "Lat, Lng" string
    Weekday TEXT,
    Start_time TEXT,
    End_time TEXT,
    Link TEXT,
    FOREIGN KEY (studentID) REFERENCES Student(studentID)
);

CREATE TABLE IF NOT EXISTS FundingRecord (
    FundingID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID INTEGER,
    Funding_type TEXT,
    Funding_name TEXT,
    Department TEXT,
    Building TEXT,
    Location TEXT, -- Expects a "Lat, Lng" string
    Weekday TEXT,
    Start_time TEXT,
    End_time TEXT,
    Link TEXT,
    FOREIGN KEY (studentID) REFERENCES Student(studentID)
);

CREATE TABLE IF NOT EXISTS TutoringRecord (
    TutoringID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID INTEGER,
    Resource_type TEXT,
    Subject TEXT,
    Department TEXT,
    Building TEXT,
    Location TEXT, -- Expects a "Lat, Lng" string
    Weekday TEXT,
    Start_time TEXT,
    End_time TEXT,
    Notes TEXT,
    FOREIGN KEY (studentID) REFERENCES Student(studentID)
);

CREATE TABLE IF NOT EXISTS StudentSuppliesRecord (
    SupplyID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID INTEGER,
    Resource_type TEXT,
    Item TEXT,
    Department TEXT,
    Building TEXT,
    Location TEXT, -- Expects a "Lat, Lng" string
    Limit_info TEXT,
    Weekday TEXT,
    Start_time TEXT,
    End_time TEXT,
    Notes TEXT,
    FOREIGN KEY (studentID) REFERENCES Student(studentID)
);

-- Example Complex Query for Reporting (Not a statement to run, but for reference)
-- This query aggregates distinct resource usage by student.
SELECT
    s.studentID,
    s.studentName,
    COUNT(DISTINCT a.AdvisorID) AS advisor_count,
    -- ... (and so on for all resource types)
    (COUNT(DISTINCT a.AdvisorID) + COUNT(DISTINCT t.TutoringID) + COUNT(DISTINCT sup.SupplyID) + COUNT(DISTINCT h.HealthID) + COUNT(DISTINCT asupp.SupportID) + COUNT(DISTINCT f.FundingID)) AS total_resource_count
FROM Student AS s
LEFT JOIN AdvisorRecord AS a ON a.studentID = s.studentID
-- ... (LEFT JOIN all other resource tables)
GROUP BY s.studentID, s.studentName;
