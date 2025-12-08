BEGIN TRANSACTION;

-- StudentSuppliesRecord: keep studentID, studentName, supply_id
CREATE TABLE StudentSuppliesRecord_new (
    studentID   TEXT NOT NULL,
    studentName TEXT NOT NULL,
    supply_id   INTEGER NOT NULL
);
INSERT INTO StudentSuppliesRecord_new (studentID, studentName, supply_id)
SELECT studentID, studentName, supply_id
FROM StudentSuppliesRecord;
DROP TABLE StudentSuppliesRecord;
ALTER TABLE StudentSuppliesRecord_new RENAME TO StudentSuppliesRecord;

-- TutoringRecord: keep studentID, studentName, tutoring_id
CREATE TABLE TutoringRecord_new (
    studentID   TEXT NOT NULL,
    studentName TEXT NOT NULL,
    tutoring_id INTEGER NOT NULL
);
INSERT INTO TutoringRecord_new (studentID, studentName, tutoring_id)
SELECT studentID, studentName, tutoring_id
FROM TutoringRecord;
DROP TABLE TutoringRecord;
ALTER TABLE TutoringRecord_new RENAME TO TutoringRecord;

-- HealthRecord: keep studentID, studentName, health_id
CREATE TABLE HealthRecord_new (
    studentID   TEXT NOT NULL,
    studentName TEXT NOT NULL,
    health_id   INTEGER NOT NULL
);
INSERT INTO HealthRecord_new (studentID, studentName, health_id)
SELECT studentID, studentName, health_id
FROM HealthRecord;
DROP TABLE HealthRecord;
ALTER TABLE HealthRecord_new RENAME TO HealthRecord;

-- FundingRecord: keep studentID, studentName, funding_id
CREATE TABLE FundingRecord_new (
    studentID   TEXT NOT NULL,
    studentName TEXT NOT NULL,
    funding_id  INTEGER NOT NULL
);
INSERT INTO FundingRecord_new (studentID, studentName, funding_id)
SELECT studentID, studentName, funding_id
FROM FundingRecord;
DROP TABLE FundingRecord;
ALTER TABLE FundingRecord_new RENAME TO FundingRecord;

-- AcademicSupportRecord: keep studentID, studentName, support_id
CREATE TABLE AcademicSupportRecord_new (
    studentID   TEXT NOT NULL,
    studentName TEXT NOT NULL,
    support_id  INTEGER NOT NULL
);
INSERT INTO AcademicSupportRecord_new (studentID, studentName, support_id)
SELECT studentID, studentName, support_id
FROM AcademicSupportRecord;
DROP TABLE AcademicSupportRecord;
ALTER TABLE AcademicSupportRecord_new RENAME TO AcademicSupportRecord;

-- AdvisorRecord: keep studentID, studentName, advisor_id
CREATE TABLE AdvisorRecord_new (
    studentID   TEXT NOT NULL,
    studentName TEXT NOT NULL,
    advisor_id  INTEGER NOT NULL
);
INSERT INTO AdvisorRecord_new (studentID, studentName, advisor_id)
SELECT studentID, studentName, advisor_id
FROM AdvisorRecord;
DROP TABLE AdvisorRecord;
ALTER TABLE AdvisorRecord_new RENAME TO AdvisorRecord;

COMMIT;
