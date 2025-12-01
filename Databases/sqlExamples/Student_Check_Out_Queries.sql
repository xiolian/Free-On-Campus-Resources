-- All queries below are designed to simulate a student "checking out" or selecting
-- multiple services from multiple departments and locations.

-- 1. Basic Multi-Department Service Checkout for a Single Student
-- Goal: Retrieve the names of the specific Tutoring Subject and Academic Support Service
--       that a single student has "checked out" (i.e., has a record for).
SELECT
    s.studentID,
    s.studentName,
    t.subject AS CheckedOutTutoringSubject,
    a.service_name AS CheckedOutAcademicService
FROM
    Student s
-- Multiple Table Join Chain 1: Linking Student to Tutoring Service
JOIN
    TutoringRecord TR ON s.studentID = TR.studentID -- FK: studentID connects to the record
JOIN
    tutoring t ON TR.tutoring_id = t.tutoring_id      -- FK: tutoring_id connects to the service definition
-- Multiple Table Join Chain 2: Linking Student to Academic Support Service
JOIN
    AcademicSupportRecord ASR ON s.studentID = ASR.studentID -- FK: studentID connects to the record
JOIN
    academic_support A ON ASR.support_id = A.support_id       -- FK: support_id connects to the service definition
WHERE
    s.studentID = 'U100001'; -- Filter for the student checking out the services

-- 2. Multi-Department, Multi-Location Checkout Filter
-- Goal: Find all students who have checked out a Health service in the 'Clinic' AND
--       Tutoring in 'Room 205' AND received 'Grants' funding.
SELECT DISTINCT
    s.studentID,
    s.studentName,
    h.service AS HealthService,
    t.subject AS TutoringSubject,
    f.funding_type AS FundingReceived
FROM
    Student s
-- Multiple Table Join Chain 1: Linking Student to Health Service and filtering by location
JOIN HealthRecord HR ON s.studentID = HR.studentID
JOIN health_services h ON HR.health_id = h.health_id
-- Multiple Table Join Chain 2: Linking Student to Tutoring Service and filtering by location
JOIN TutoringRecord TR ON s.studentID = TR.studentID
JOIN tutoring t ON TR.tutoring_id = t.tutoring_id
-- Multiple Table Join Chain 3: Linking Student to Funding Service and filtering by type
JOIN FundingRecord FR ON s.studentID = FR.studentID
JOIN Funding f ON FR.funding_id = f.funding_id
WHERE
    -- Filtering on location and service details from multiple departments
    h.location = 'Clinic' AND
    t.location = 'Room 205' AND
    f.funding_type = 'Grants';

-- 3. Available Services List (The Pre-Checkout View)
-- Goal: Show a single student a list of ALL available services they could "check out,"
--       normalized by department and location, allowing them to select.
-- Note: This uses the UNION ALL structure to combine incompatible schemas into one view.
SELECT
    s.studentID,
    s.studentName,
    AvailableServices.Department,
    AvailableServices.ServiceName,
    AvailableServices.Location,
    AvailableServices.Building
FROM
    Student s
JOIN
    (
        -- Tutoring Services
        SELECT 'Tutoring' AS Department, subject AS ServiceName, location, building FROM tutoring
        UNION ALL
        -- Academic Support Services
        SELECT 'Academic Support' AS Department, service_name AS ServiceName, location, building FROM academic_support
        UNION ALL
        -- Student Supplies
        SELECT 'Supplies' AS Department, item AS ServiceName, location, building FROM student_supplies
    ) AS AvailableServices ON 1=1 -- Cartesian join to show *all* services for the single student
WHERE
    S.studentID = 'U100001'; -- Filter for the student viewing the available list
