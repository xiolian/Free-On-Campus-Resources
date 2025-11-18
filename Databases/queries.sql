
-- 10 tuples per table [Reported in Lecture] - will add more via user import
-- 3 tables - complex [AT LEAST]
-- 20 Queries 

-- Simple Queries + Single Table: 7
-- Join Queries: 7
-- Complex Join Queries: 6




-- ###################################################################################




-- 1. Simple Queries + Single Table



-- Tutoring (1)
SELECT tutoring_id, subject, building, location, weekday, start_time, end_time
FROM tutoring
WHERE subject LIKE 'CSE%';

-- Tutoring (2)
SELECT tutoring_id, subject, building, location, weekday, start_time, end_time
FROM tutoring
GROUP BY subject, building, location, weekday, start_time, end_time;

-- Student Supplies (3)
SELECT supply_id, resource_type, item, building, location
FROM student_supplies
WHERE resource_type = 'Food';

-- Health Services (4)
SELECT health_id, health_category, service, location, weekday
FROM health_services
WHERE health_category LIKE '%Counseling%';

-- Subjects offered in Tutoring + sessions greater than 1 (5, 6)
SELECT subject, COUNT(*) AS number_of_sessions
FROM tutoring
GROUP BY subject
HAVING COUNT(*) > 1
ORDER BY subject;

SELECT subject, COUNT(*) AS number_of_sessions
FROM tutoring
GROUP BY subject
ORDER BY subject;

-- Find how many want scholarship (7)
SELECT COUNT(*) AS number_wanting_scholarship
FROM FundingRecord
WHERE funding_type = 'Scholarships';



-- 2. Joins of Tables



-- Tutoring Record for a specific student (1)
SELECT s.studentName, t.subject, t.weekday, t.start_time, t.end_time
FROM Student s, TutoringRecord t
WHERE s.studentID = t.studentID
AND s.studentID = 'U100001';

-- Find all resources available on mondays for all tables (2)
SELECT
    h.health_id AS id,
    'Health Service' AS resource_type,
    h.service AS name,
    h.location,
    h.weekday
FROM health_services h
WHERE h.weekday LIKE 'Monday%'

UNION ALL

SELECT
    t.tutoring_id AS id,
    'Tutoring' AS resource_type,
    t.subject AS name,
    t.location,
    t.weekday
FROM tutoring t
WHERE t.weekday LIKE 'Monday%'

UNION ALL

SELECT
    asupp.support_id AS id,
    'Academic Support' AS resource_type,
    asupp.service_name AS name,
    asupp.location,
    asupp.weekday
FROM academic_support asupp
WHERE asupp.weekday LIKE 'Monday%'

UNION ALL

SELECT
    stu.supply_id AS id,
    'Student Supplies' AS resource_type,
    stu.item AS name,
    stu.location,
    stu.weekday
FROM student_supplies stu
WHERE stu.weekday LIKE 'Monday%';

-- Tuesday Resources (3)
SELECT
    h.health_id AS id,
    'Health Service' AS resource_type,
    h.service AS name,
    h.location,
    h.weekday
FROM health_services h
WHERE h.weekday LIKE '%Tuesday%' or h.weekday = 'Monday-Friday'

UNION ALL

SELECT
    t.tutoring_id AS id,
    'Tutoring' AS resource_type,
    t.subject AS name,
    t.location,
    t.weekday
FROM tutoring t
WHERE t.weekday LIKE '%Tuesday%' or t.weekday = 'Monday-Friday'

UNION ALL

SELECT
    asupp.support_id AS id,
    'Academic Support' AS resource_type,
    asupp.service_name AS name,
    asupp.location,
    asupp.weekday
FROM academic_support asupp
WHERE asupp.weekday LIKE '%Tuesday%' or asupp.weekday = 'Monday-Friday'

UNION ALL

SELECT
    stu.supply_id AS id,
    'Student Supplies' AS resource_type,
    stu.item AS name,
    stu.location,
    stu.weekday
FROM student_supplies stu
WHERE stu.weekday LIKE '%Tuesday%' or stu.weekday = 'Monday-Friday';

-- Wednesday Resources (4)
SELECT
    h.health_id AS id,
    'Health Service' AS resource_type,
    h.service AS name,
    h.location,
    h.weekday
FROM health_services h
WHERE h.weekday LIKE '%Wednesday%' or h.weekday = 'Monday-Friday'

UNION ALL

SELECT
    t.tutoring_id AS id,
    'Tutoring' AS resource_type,
    t.subject AS name,
    t.location,
    t.weekday
FROM tutoring t
WHERE t.weekday LIKE '%Wednesday%' or t.weekday = 'Monday-Friday'

UNION ALL

SELECT
    asupp.support_id AS id,
    'Academic Support' AS resource_type,
    asupp.service_name AS name,
    asupp.location,
    asupp.weekday
FROM academic_support asupp
WHERE asupp.weekday LIKE '%Wednesday%' or asupp.weekday = 'Monday-Friday'

UNION ALL

SELECT
    stu.supply_id AS id,
    'Student Supplies' AS resource_type,
    stu.item AS name,
    stu.location,
    stu.weekday
FROM student_supplies stu
WHERE stu.weekday LIKE '%Wednesday%' or stu.weekday = 'Monday-Friday';

-- Resources in the same building from Academic Support & Student Supplies (5)
SELECT
    s.building,
    s.location AS supplies_location,
    s.item AS supply_item,
    asupp.aca_supp_service,
    asupp.service_name
FROM student_supplies s, academic_support asupp
WHERE s.building = asupp.building
ORDER BY s.building, s.item;

-- Student Supplies & Tutoring (Same Location) (6)
SELECT
    s.item as StudentSupplies,
    s.location as SuppliesLocation,
    s.weekday as SuppliesDay,
    s.start_time as SuppliesStart,
    s.end_time as SuppliesEnd,
    t.subject as TutoringSubject,
    t.weekday as TutoringDay,
    t.start_time as TutoringStart,
    t.end_time as TutoringEnd
FROM student_supplies s, tutoring t
WHERE s.location = t.location;

-- Find Student, tutoring subject, and advisor based on advisors that are affiliated with CSE (7)
SELECT 
    s.studentID,
    s.studentName,
    t.subject AS tutoring_subject,
    a.name AS advisor_name,
    a.affiliation AS advisor_affiliation
FROM Student s, TutoringRecord t, AdvisorRecord a
WHERE s.studentID = t.studentID
AND s.studentID = a.studentID
AND a.affiliation LIKE '%CSE%';



-- 3. Complex Joins



-- Resources Obtained by all students (accross all tables) (1)
-- All combinations of students and their resources
SELECT
    s.studentID,
    s.studentName,
    a.advisor_id,
    t.tutoring_id,
    sup.supply_id,
    h.health_id,
    asupp.support_id,
    f.funding_id

FROM Student AS s, AdvisorRecord AS a, TutoringRecord AS t, StudentSuppliesRecord AS sup, HealthRecord AS h, FundingRecord AS f, AcademicSupportRecord AS asupp
WHERE a.studentID   = s.studentID
AND t.studentID   = s.studentID
AND sup.studentID = s.studentID
AND h.studentID   = s.studentID
AND asupp.studentID = s.studentID
AND f.studentID   = s.studentID;

-- Count of Resources Obtained by all students (2)
SELECT
    s.studentID,
    s.studentName,
    COUNT(DISTINCT a.advisor_id)        AS advisor_count,
    COUNT(DISTINCT t.tutoring_id)       AS tutoring_count,
    COUNT(DISTINCT sup.supply_id)       AS supplies_count,
    COUNT(DISTINCT h.health_id)         AS health_count,
    COUNT(DISTINCT asupp.support_id)    AS academic_support_count,
    COUNT(DISTINCT f.funding_id)        AS funding_count,
    (
      COUNT(DISTINCT a.advisor_id) +
      COUNT(DISTINCT t.tutoring_id) +
      COUNT(DISTINCT sup.supply_id) +
      COUNT(DISTINCT h.health_id) +
      COUNT(DISTINCT asupp.support_id) +
      COUNT(DISTINCT f.funding_id)
    ) AS total_resource_count

FROM Student AS s, AdvisorRecord AS a, TutoringRecord AS t, StudentSuppliesRecord AS sup, HealthRecord AS h, FundingRecord AS f, AcademicSupportRecord AS asupp
WHERE a.studentID   = s.studentID
AND t.studentID   = s.studentID
AND sup.studentID = s.studentID
AND h.studentID   = s.studentID
AND asupp.studentID = s.studentID
AND f.studentID   = s.studentID
GROUP BY s.studentID, s.studentName;


-- Funding & Advisor for all students (3)
SELECT
    s.studentID,
    s.studentName,
    a.name AS advisor_name,
    f.funding_name,
    f.funding_type
FROM Student s, AdvisorRecord a, FundingRecord f
WHERE a.studentID = s.studentID
AND f.studentID = s.studentID
ORDER BY s.studentID;

-- Monday Resources Summary for all students (4)
WITH monday_resources AS (
    SELECT
        studentID,
        studentName,
        'Tutoring' AS resource_category,
        tutoring_id AS resource_id
    FROM TutoringRecord
    WHERE weekday LIKE '%Monday%'

    UNION ALL

    SELECT
        studentID,
        studentName,
        'Supplies' AS resource_category,
        supply_id AS resource_id
    FROM StudentSuppliesRecord
    WHERE weekday LIKE '%Monday%'

    UNION ALL

    SELECT
        studentID,
        studentName,
        'Health' AS resource_category,
        health_id AS resource_id
    FROM HealthRecord
    WHERE weekday LIKE '%Monday%'

    UNION ALL

    SELECT
        studentID,
        studentName,
        'Academic Support' AS resource_category,
        support_id AS resource_id
    FROM AcademicSupportRecord
    WHERE weekday LIKE '%Monday%'

    UNION ALL

    SELECT
        studentID,
        studentName,
        'Funding' AS resource_category,
        funding_id AS resource_id
    FROM FundingRecord
    WHERE weekday LIKE '%Monday%'
)

SELECT
    s.studentID,
    s.studentName,
    COUNT(DISTINCT mr.resource_id) AS total_monday_resources,
    COUNT(DISTINCT CASE WHEN mr.resource_category = 'Tutoring' THEN mr.resource_id END) AS monday_tutoring_count,
    COUNT(DISTINCT CASE WHEN mr.resource_category = 'Supplies' THEN mr.resource_id END) AS monday_supplies_count,
    COUNT(DISTINCT CASE WHEN mr.resource_category = 'Health' THEN mr.resource_id END) AS monday_health_count,
    COUNT(DISTINCT CASE WHEN mr.resource_category = 'Academic Support' THEN mr.resource_id END) AS monday_academic_support_count,
    COUNT(DISTINCT CASE WHEN mr.resource_category = 'Funding' THEN mr.resource_id END) AS monday_funding_count

FROM Student AS s, monday_resources AS mr
WHERE mr.studentID = s.studentID
GROUP BY s.studentID, s.studentName
HAVING total_monday_resources > 0
ORDER BY total_monday_resources DESC, s.studentID;

-- Find students who want resources available on Wednesdays (5)
SELECT s.studentID, s.studentName, asr.service_name AS AcaSuppName, t.subject AS TutoringSubject, h.service AS HealthService
FROM Student s, AcademicSupportRecord asr, TutoringRecord t, HealthRecord h
WHERE s.studentID = asr.studentID
AND s.studentID = t.studentID
AND s.studentID = h.studentID
AND (asr.weekday LIKE '%Wednesday%' OR asr.weekday LIKE 'Monday-Friday%')
AND (t.weekday LIKE '%Wednesday%' OR t.weekday LIKE 'Monday-Friday%')
AND (h.weekday LIKE '%Wednesday%' OR h.weekday LIKE 'Monday-Friday%')
GROUP BY s.studentID, s.studentName, asr.service_name, t.subject, h.service;

-- Find students who have all resources (6)
SELECT s.studentID, s.studentName
FROM Student s
WHERE s.studentID IN (SELECT studentID FROM TutoringRecord)
AND s.studentID IN (SELECT studentID FROM StudentSuppliesRecord)
AND s.studentID IN (SELECT studentID FROM HealthRecord)
AND s.studentID IN (SELECT studentID FROM AdvisorRecord)
AND s.studentID IN (SELECT studentID FROM FundingRecord);