-- All queries below are filtered for a single student (studentID = 'U100001')
-- You must replace 'U100001' with the actual Student ID you wish to query.

-- 1. Student's Records (All combinations of resources)
-- Shows all individual records this student has across all major resource types.
SELECT
    s.studentID,
    s.studentName,
    a.advisor_id,
    t.tutoring_id,
    s.supply_id,
    h.health_id,
    ASR.support_id,
    f.funding_id
FROM
    Student AS s -- Primary table for the student
-- Multiple Table Joins: Linking Student (PK: studentID) to all Resource Record tables
JOIN AdvisorRecord AS AR ON s.studentID = AR.studentID
JOIN TutoringRecord AS TR ON s.studentID = TR.studentID
JOIN StudentSuppliesRecord AS SSR ON s.studentID = SSR.studentID
JOIN HealthRecord AS HR ON s.studentID = HR.studentID
JOIN FundingRecord AS FR ON s.studentID = FR.studentID
JOIN AcademicSupportRecord AS ASR ON s.studentID = ASR.studentID
WHERE
    s.studentID = 'U100001'; -- Filter for one specific student

-- 2. Count of Resources Obtained by the Student
-- Provides a summary count of how many distinct records the student has in each category.
SELECT
    s.studentID,
    s.studentName,
    COUNT(DISTINCT AR.advisor_id) AS advisor_count,
    COUNT(DISTINCT TR.tutoring_id) AS tutoring_count,
    COUNT(DISTINCT s.supply_id) AS supplies_count,
    COUNT(DISTINCT HR.health_id) AS health_count,
    COUNT(DISTINCT ASR.support_id) AS academic_support_count,
    COUNT(DISTINCT f.funding_id) AS funding_count,
    (
      COUNT(DISTINCT AR.advisor_id) +
      COUNT(DISTINCT t.tutoring_id) +
      COUNT(DISTINCT s.supply_id) +
      COUNT(DISTINCT HR.health_id) +
      COUNT(DISTINCT ASR.support_id) +
      COUNT(DISTINCT f.funding_id)
    ) AS total_resource_count
FROM
    Student AS s -- Primary table for the student
-- Multiple Table Joins: Linking Student (PK: studentID) to all Resource Record tables for counting
JOIN AdvisorRecord AS AR ON s.studentID = AR.studentID
JOIN TutoringRecord AS TR ON s.studentID = TR.studentID
JOIN StudentSuppliesRecord AS SSR ON s.studentID = SSR.studentID
JOIN HealthRecord AS HR ON s.studentID = HR.studentID
JOIN FundingRecord AS FR ON s.studentID = FR.studentID
JOIN AcademicSupportRecord AS ASR ON S.studentID = ASR.studentID
WHERE
    S.studentID = 'U100001' -- Filter for one specific student
GROUP BY
    s.studentID, s.studentName;

-- 3. Student's Funding & Advisor Information (Corrected to join to definition tables)
-- Lists the student's advisor and all associated funding records, retrieving names/types.
SELECT
    s.studentID,
    s.studentName,
    a.name AS advisor_name,
    f.funding_name,
    f.funding_type
FROM
    Student S -- Primary table
-- Multiple Table Joins: Linking Student to Advisor and Funding definitions (M:M chain)
JOIN AdvisorRecord AR ON s.studentID = AR.studentID    -- Link to Advisor Record (M:M linker)
JOIN Advisor A ON AR.advisor_id = a.advisor_id        -- Link to Advisor Definition
JOIN FundingRecord FR ON S.studentID = FR.studentID    -- Link to Funding Record (M:M linker)
JOIN Funding F ON FR.funding_id = f.funding_id        -- Link to Funding Definition
WHERE
    s.studentID = 'U100001' -- Filter for one specific student
ORDER BY
    s.studentID;

-- 4. Student's Monday Resources Summary (Aggregated Count)
-- Counts the number of distinct resources this student is scheduled to use on a Monday.
WITH student_monday_resources AS (
    -- Collect all distinct Monday resources for this specific student
    SELECT 'Tutoring' AS resource_category, tutoring_id AS resource_id
    FROM TutoringRecord
    WHERE studentID = 'U100001' AND weekday LIKE '%Monday%'
    UNION ALL
    SELECT 'Supplies' AS resource_category, supply_id AS resource_id
    FROM StudentSuppliesRecord
    WHERE studentID = 'U100001' AND weekday LIKE '%Monday%'
    UNION ALL
    SELECT 'Health' AS resource_category, health_id AS resource_id
    FROM HealthRecord
    WHERE studentID = 'U100001' AND weekday LIKE '%Monday%'
    UNION ALL
    SELECT 'Academic Support' AS resource_category, support_id AS resource_id
    FROM AcademicSupportRecord
    WHERE studentID = 'U100001' AND weekday LIKE '%Monday%'
    UNION ALL
    SELECT 'Funding' AS resource_category, funding_id AS resource_id
    FROM FundingRecord
    WHERE studentID = 'U100001' AND weekday LIKE '%Monday%'
)
SELECT
    s.studentID,
    s.studentName,
    COUNT(DISTINCT SMR.resource_id) AS total_monday_resources,
    COUNT(DISTINCT CASE WHEN SMR.resource_category = 'Tutoring' THEN SMR.resource_id END) AS monday_tutoring_count,
    COUNT(DISTINCT CASE WHEN SMR.resource_category = 'Supplies' THEN SMR.resource_id END) AS monday_supplies_count,
    COUNT(DISTINCT CASE WHEN SMR.resource_category = 'Health' THEN SMR.resource_id END) AS monday_health_count,
    COUNT(DISTINCT CASE WHEN SMR.resource_category = 'Academic Support' THEN SMR.resource_id END) AS monday_academic_support_count,
    COUNT(DISTINCT CASE WHEN SMR.resource_category = 'Funding' THEN SMR.resource_id END) AS monday_funding_count
FROM
    Student AS s
LEFT JOIN
    student_monday_resources AS SMR ON 1=1 -- Join ensures we get one row for the student even if they have no resources
WHERE
    s.studentID = 'U100001' -- Ensure we only return the specific student's record
GROUP BY
    s.studentID, S.studentName;

-- 5. Student's Resources Available on Wednesdays
-- Shows the specific tutoring, academic support, and health services this student uses that are active on Wednesdays.
SELECT DISTINCT
    s.studentID,
    s.studentName,
    a.service_name AS AcaSuppName,
    t.subject AS TutoringSubject,
    h.service AS HealthService
FROM
    Student s
-- Multiple Table Joins: Linking Student to Academic Support, Tutoring, and Health definitions (M:M chains)
JOIN AcademicSupportRecord ASR ON s.studentID = ASR.studentID
JOIN academic_support A ON ASR.support_id = A.support_id
JOIN TutoringRecord TR ON s.studentID = TR.studentID
JOIN tutoring T ON TR.tutoring_id = T.tutoring_id
JOIN HealthRecord HR ON s.studentID = HR.studentID
JOIN health_services H ON HR.health_id = H.health_id
WHERE
    S.studentID = 'U100001' -- Filter for one specific student
    AND (a.weekday LIKE '%Wednesday%' OR A.weekday LIKE 'Monday-Friday%')
    AND (t.weekday LIKE '%Wednesday%' OR T.weekday LIKE 'Monday-Friday%')
    AND (h.weekday LIKE '%Wednesday%' OR H.weekday LIKE 'Monday-Friday%');


-- 6. Check if the Student Has All Resource Records
-- Returns the student's ID and name ONLY if they have at least one record in all five specified resource tables.
SELECT
    s.studentID,
    s.studentName
FROM
    Student s
WHERE
    S.studentID = 'U100001' -- Filter for one specific student
    AND s.studentID IN (SELECT studentID FROM TutoringRecord)
    AND s.studentID IN (SELECT studentID FROM StudentSuppliesRecord)
    AND s.studentID IN (SELECT studentID FROM HealthRecord)
    AND s.studentID IN (SELECT studentID FROM AdvisorRecord)
    AND s.studentID IN (SELECT studentID FROM FundingRecord);

-- 7. Student's Filtered Resource Records (MATH Tutoring & UROC Advisor)
-- Finds the specific Tutoring and Advisor IDs for the student, filtered by specific resource attributes.
SELECT DISTINCT
    s.studentID,
    t.tutoring_id AS TutoringID,
    a.advisor_id AS AdvisorID
FROM
    Student S
-- Multiple Table Joins: Linking Student to Tutoring and Advisor definitions (M:M chains)
JOIN TutoringRecord TR ON s.studentID = TR.studentID
JOIN tutoring T ON TR.tutoring_id = T.tutoring_id
JOIN AdvisorRecord AR ON s.studentID = AR.studentID
JOIN Advisor A ON AR.advisor_id = A.advisor_id
WHERE
    s.studentID = 'U100001' -- Filter for one specific student
    AND t.subject LIKE 'MATH%' -- Filter: Tutoring subject starts with 'MATH'
    AND a.affiliation = 'UROC'; -- Filter: Advisor affiliation is 'UROC'
